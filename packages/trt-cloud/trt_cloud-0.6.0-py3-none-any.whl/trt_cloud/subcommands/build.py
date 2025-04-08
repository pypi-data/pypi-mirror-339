# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import argparse
import contextlib
import functools
import io
import logging
import os
import re
import shutil
from tempfile import TemporaryDirectory
import time
import sys
import json
from typing import List

from trt_cloud import constants, utils
from trt_cloud.build_spec.build_input_source import BuildInput, BuildInputFileType, HFRepoInputSource
from trt_cloud.build_spec.build_options import (
    BuildType,
    TRTLLMBuildReturnType,
    TRTLLMDtype,
    TRTLLMKVQuantizationType,
    TRTLLMQuantizationType,
)
from trt_cloud.build_spec.build_recipe import TRTLLMRecipe
from trt_cloud.client import TRTCloud
from trt_cloud.state import TRTCloudConfig
from trt_cloud.subcommands.base_subcommand import Subcommand, _check_status
from trt_cloud.subcommands.utils import run_list_common, validate_tags
from trt_cloud.sweeper import (
    TERMINAL_SWEEP_STATES,
    BuildConfig,
    ONNXBuildConfig,
    SweeperClient,
    TRTLLMBuildConfig,
    WorkloadResult,
    WorkloadStatus,
    WorkloadType,
)
from trt_cloud.types import StringEnum


class BuildSubCommands(StringEnum):
    STATUS = "status"
    RESULTS = "results"
    LIST = "list"
    CANCEL = "cancel"
    # Build types (from BuildType)
    ONNX = BuildType.ONNX.value
    TRT_LLM = BuildType.TRT_LLM.value


def _check_build_status(
    display: utils.Display,
    user_command: str,
    client: SweeperClient,
    build_id: str,
):
    # Make the request _before_ printing the top bar to avoid partial draws
    status, build, trials = client.get_status(sweep_id=build_id, trial_id="0", workload_type=WorkloadType.SINGLE_ENGINE)
    build_status = build.get("status")  # will be used to check if the sweep is terminal
    display.reset()
    display.print_top_bar()
    display.print(user_command, heading="User Command")
    # Keep the status message intact as it's important and actionable.
    display.print(status, truncate=False)
    end_timestamp = (
        "N/A"
        if "end_timestamp" not in build or build["end_timestamp"] == "1969-12-31T23:59:59"
        else build["end_timestamp"]
    )
    build_info = "Start: {}, End: {}, Tags: {}".format(
        build["timestamp"],
        end_timestamp,
        # display.print will automatically truncate long lines so no need to truncate tags
        json.dumps(build["tags"]),
    )
    display.print(build_info)
    if trials:
        for t in trials:
            t_status_message = t.get("status_message", "")
            display.print_middle_bar()
            lines = t_status_message.splitlines()
            display.print(f"Latest {len(lines)} lines of build log:")
            for line in lines:
                line = line.rstrip("\n")
                display.print(f"    {line}")
    display.print_bottom_bar()
    return build_status not in TERMINAL_SWEEP_STATES


class BuildSubcommand(Subcommand):
    @staticmethod
    def _add_common_onnx_and_llm_options(parser: argparse.ArgumentParser):
        # Valid for both 'onnx' and 'llm' commands
        parser.add_argument("--gpu", help="GPU model to build engine for", required=True)
        parser.add_argument("--os", help="OS to build engine for", choices=["linux", "windows"], required=True)
        parser.add_argument(
            "-t",
            "--tags",
            nargs="+",
            help="Tags to associate with the build.",
            default=[],
            required=False,
        )
        # TODO: local refit can't be supplied in the initial build command because build results are obtained separately
        # parser.add_argument(
        #     "--local-refit",
        #     action="store_true",
        #     help="If set, will locally refit a weight-stripped engine after build. "
        #     "Please make sure that your python environment has the TensorRT "
        #     "version corresponding to the engine built.",
        # )
        BuildSubcommand._add_build_output_options(parser)
        BuildSubcommand._add_prompt_skip_option(parser)

    @staticmethod
    def _add_onnx_build_options_to_parser(parser: argparse.ArgumentParser):
        # Valid for 'build onnx' commands
        parser.add_argument(
            "--trt-version",
            default="latest",
            help="TRT Version to build the engine for. "
            'May be "latest", "default", or a numeric version such as "10.0". '
            "Only applicable for ONNX builds.",
        )
        parser.add_argument("--trtexec-args", type=str, help="Args to pass to trtexec")
        BuildSubcommand.add_src_options_to_parser(parser)
        BuildSubcommand._add_common_onnx_and_llm_options(parser)

    @staticmethod
    def _add_trtllm_build_options_to_parser(parser: argparse.ArgumentParser):
        # Valid for 'build trtllm' commands
        parser.add_argument(
            "--return-type",
            type=TRTLLMBuildReturnType,
            help="Return type from build. "
            "(checkpoint_only): Returns only a quantized checkpoint. "
            "(engine_only): Returns only an engine and timing cache. "
            "(metrics_only): Returns only performance metrics. "
            "(engine_and_metrics): Returns an engine, metrics, and timing cache.",
            choices=list(TRTLLMBuildReturnType),
            default=TRTLLMBuildReturnType.ENGINE_AND_METRICS,
        )

        parser.add_argument(
            "--trtllm-version",
            default="latest",
            help="TRT LLM Version to build the engine for. "
            'May be "latest" or a numeric version such as "0.12.0". '
            "Only applicable for TRT LLM builds.",
        )
        parser.add_argument(
            "--dtype",
            type=TRTLLMDtype,
            choices=list(TRTLLMDtype),
            help="Specifies the model data type (for activations and non-quantized weights).",
        )
        parser.add_argument(
            "--quantization",
            type=TRTLLMQuantizationType,
            choices=list(TRTLLMQuantizationType),
            default=TRTLLMQuantizationType.FULL_PREC,
            help="Quantization mode.",
        )
        parser.add_argument(
            "--quantize-kv-cache",
            action="store_true",
            help="If specified, quantizes the KV cache. "
            "The quantization type is picked automatically "
            "based on the model and quantization.",
        )
        parser.add_argument("--max-input-len", type=int, default=None)
        parser.add_argument(
            "--max-batch-size",
            type=int,
            default=None,
            help="The maximum number of requests that the engine can handle.",
        )
        parser.add_argument(
            "--max-seq-len",
            type=int,
            default=None,
            help="Maximum sequence length of a single request.",
        )
        parser.add_argument(
            "--max-num-tokens",
            type=int,
            default=None,
            help="Maximum number of batched input tokens after padding is removed in each batch.",
        )
        parser.add_argument(
            "--tp-size",
            type=int,
            default=1,
            choices=[1, 2, 4, 8],
            help="Specifies the number of GPUs for tensor-parallelism "
            "during inference. (Only supported for Linux builds)",
        )
        parser.add_argument(
            "--pp-size",
            type=int,
            default=1,
            choices=[1, 2, 4, 8],
            help="Specifies the number of GPUs for pipeline-parallelism "
            "during inference. (Only supported for Linux builds)",
        )

        BuildSubcommand.add_trtllm_src_options_to_parser(parser)
        BuildSubcommand._add_common_onnx_and_llm_options(parser)

    @staticmethod
    def _add_build_id_options_to_parser(parser: argparse.ArgumentParser):
        parser.add_argument(
            "build_id",
            help="""
            Build ID of a previously-started build.
        """,
        )

    @staticmethod
    def _add_list_build_options_to_parser(parser: argparse.ArgumentParser):
        parser.add_argument("--me", action="store_true", help="Filter by current user.")
        parser.add_argument("--since", type=str, help="Show builds since this timestamp (format: YYYY-MM-DDTHH:MM:SS).")
        parser.add_argument("--until", type=str, help="Show builds until this timestamp (format: YYYY-MM-DDTHH:MM:SS).")
        parser.add_argument(
            "--limit", type=int, default=None, help="Limit the number of builds shown."
        )  # Set's default to 25 if value is None, allows us to detect when the user didn't provide a value

    @staticmethod
    def add_subparser(subparsers: argparse._SubParsersAction, subcommand_name: str) -> argparse.ArgumentParser:
        """
        Adds the 'build' subcommand to the main CLI argument parser.
        """
        build_subcommand = subparsers.add_parser(subcommand_name, help="Build a TRT engine on the cloud.")
        build_type = build_subcommand.add_subparsers(help="Types of builds", dest="build_type", required=True)

        # Add a formatter that shows default values in the help text
        add_parser_show_defaults = functools.partial(
            build_type.add_parser, formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        onnx_subparser = add_parser_show_defaults(
            BuildSubCommands.ONNX.value, help="Build a TRT Engine from an onnx model."
        )
        BuildSubcommand._add_onnx_build_options_to_parser(onnx_subparser)

        trtllm_subparser = add_parser_show_defaults(BuildSubCommands.TRT_LLM.value, help="Build a TRT-LLM Engine.")
        BuildSubcommand._add_trtllm_build_options_to_parser(trtllm_subparser)

        status_subparser = add_parser_show_defaults(BuildSubCommands.STATUS.value, help="Check the status of a build.")
        status_subparser.add_argument("-w", "--watch", action="store_true", help="Continually run the status check.")
        BuildSubcommand._add_build_id_options_to_parser(status_subparser)

        results_subparser = add_parser_show_defaults(BuildSubCommands.RESULTS.value, help="Get the results of a build.")
        BuildSubcommand._add_build_id_options_to_parser(results_subparser)
        BuildSubcommand._add_build_results_options(results_subparser)
        results_subparser.add_argument(
            "--wait", action="store_true", help="Poll for results if they are not yet ready."
        )

        list_subparser = add_parser_show_defaults(BuildSubCommands.LIST.value, help="List builds.")
        BuildSubcommand._add_list_build_options_to_parser(list_subparser)

        cancel_subparser = add_parser_show_defaults(BuildSubCommands.CANCEL.value, help="Cancel a build.")
        BuildSubcommand._add_build_id_options_to_parser(cancel_subparser)

        return build_subcommand

    def run_build_status(self, trtcloud_client: TRTCloud, build_id: str, watch: bool = False):
        display = utils.Display()

        with (
            utils.PrintMessageOnCtrlC(
                msg=f"Caught KeyboardInterrupt. Build status may be queried using build ID {build_id}."
            ),
            utils.PrintNewlineOnExit(),
        ):
            user_command = " ".join(sys.argv[1:])
            check_status = functools.partial(
                _check_build_status,
                display=display,
                user_command=user_command,
                client=trtcloud_client.sweeper_client,
                build_id=build_id,
            )

            if watch:
                while check_status():
                    time.sleep(5)
            else:
                check_status()

            build_result = trtcloud_client.get_workload_result(build_id=build_id)

            self._assert_build_status(build_result.status)

            if build_result.ready and build_result.engines:
                BuildSubcommand._print_build_output(build_id, build_result, print_results_command=True)

    def run_build_results(self, trtcloud_client: TRTCloud, args: argparse.Namespace):
        """
        Query the results of a build.

        First query the status of the build workload to ensure it's done.

        Args:
            trtcloud_client: The TRTCloud client.
            build_id: The ID of the build to query.
            wait_for_completion: If True, wait for the build to complete and return the results.
                If False, return immediately and do not wait for the build to complete.
        """
        # Query the build status until it's done
        build_id = args.build_id
        if args.wait:
            build = trtcloud_client.poll_workload_status(
                build_id,
                wait_for_status=TERMINAL_SWEEP_STATES,
                interrupt_msg=f"Results may be queried with 'trt-cloud build results {build_id}'",
                workload_type=WorkloadType.SINGLE_ENGINE,
            )
            self._assert_build_status(build.status)

            logging.info(f"Build {build_id} completed with status: {build.status}")

        build_result = trtcloud_client.get_workload_result(build_id=build_id)

        self._assert_build_status(build_result.status)

        if not build_result:
            logging.error(f"Build results not found for build id: {build_id}")

        if not build_result.ready:
            logging.info(f"Results are not yet ready (build status: {build_result.status}).")
            return

        if not build_result.engines:
            logging.error(f"No engines found for build id: {build_id}")
            return

        BuildSubcommand._print_build_output(build_id, build_result)
        BuildSubcommand._maybe_download_build_output_from_ngc_registry(build_result.engines[0].url, args)

    @staticmethod
    def _assert_build_status(status: WorkloadStatus):
        if status == WorkloadStatus.CANCELLED:
            raise ValueError("Build cancelled")

    @staticmethod
    def _print_build_output(build_id: str, build_result: WorkloadResult, print_results_command: bool = False):
        # There should only ever be one engine in the build result because we no longer
        # support multiple engines per build.
        engine = build_result.engines[0]
        if not engine.url:
            raise ValueError("The build result was not successfully uploaded.")
        elif engine.url.startswith("https://registry.ngc.nvidia.com"):
            logging.info(f"Build output was uploaded to NGC Private Registry: {engine.url}")
            # Results can only be downloaded automatically if the build was uploaded to NGC Private Registry
            if print_results_command:
                logging.info("To download the build output, run:")
                logging.info(f"trt-cloud build results {build_id}")
        else:
            raise ValueError(
                f"Build result URL '{engine.url}' is not valid. The results may not have been uploaded to the NGC "
                "Private Registry."
            )

    @staticmethod
    def _maybe_download_build_output_from_ngc_registry(url: str, args):
        if not url.startswith("https://registry.ngc.nvidia.com"):
            return

        # TODO: ideally the results endpoint should return the components of the NGC target so that we don't have to
        # parse the URL here.
        pattern = (
            r"https://registry\.ngc\.nvidia\.com/orgs/([^/]+)(?:/teams/([^/]+))?/models/([^/]+)/files/?\?version=(.+)"
        )
        match = re.match(pattern, url)
        if not match:
            logging.error(f"Failed to parse NGC Registry URL: {url}")
            return
        org, team, name, version = match.groups()

        import ngcsdk

        ngc_client = ngcsdk.Client()
        nvapi_key = args.dst_token or TRTCloudConfig().read_saved_login()
        try:
            team = team or constants.NGC_NO_TEAM
            ngc_client.configure(org_name=org, team_name=team, api_key=nvapi_key)
        except Exception:
            team_str = f" and team {team}" if team else ""
            logging.error(
                f"Failed to configure NGC client for org {org}{team_str}. Please check if the "
                "NGC access token is valid to access the build result."
            )
            return

        target = f"{org}/"
        if team:
            target += f"{team}/"
        target += f"{name}:{version}"

        total_size = 0
        files = ngc_client.registry.model.get_version_files(target, org, team)
        for file in files:
            total_size += file.sizeInBytes
        use_mb = total_size < 1024**3
        if use_mb:
            size_in_mb = total_size / (1024**2)
            logging.info(f"Total size of build result: {size_in_mb:.3f} MB")
        else:
            size_in_gb = total_size / (1024**3)
            logging.info(f"Total size of build result: {size_in_gb:.3f} GB")

        if args.dst_path:
            output_dir = os.path.abspath(args.dst_path)
        elif input("Would you like to download the build result? [y/N]: ").strip().lower() == "y":
            output_dir = os.path.join(os.getcwd(), name)
        else:
            return

        if os.path.exists(output_dir):
            logging.error(
                f"Output directory {output_dir} already exists. Please remove it or specify a "
                "different output directory using the --output flag."
            )
            return

        logging.info(f"Downloading build result to '{output_dir}'...")

        with TemporaryDirectory() as temp_dir:
            # Hide debug logs from ngcsdk
            with contextlib.redirect_stdout(io.StringIO()):
                ngc_client.registry.model.download_version(target, destination=temp_dir)
            downloaded_artifact_dir = os.path.join(temp_dir, f"{name}_v{version}")
            utils.fix_broken_ngc_windows_directory_structure(downloaded_artifact_dir)
            build_result_dir = os.path.join(downloaded_artifact_dir, "build_result")
            shutil.move(build_result_dir, output_dir)

        logging.info("Download complete.")

    def run_build_cancel(self, trtcloud_client: TRTCloud, build_id: str):
        """
        Cancel a build.

        First query the status of the build workload to ensure it's done.

        Args:
            trtcloud_client: The TRTCloud client.
            build_id: The ID of the build to cancel.
        """
        trtcloud_client.sweeper_client.put_cancel(build_id)
        logging.info(f"Cancelled build session with build_id: {build_id} ")

    def run_build_list(self, trtcloud_client: TRTCloud, args):
        """
        Executes list subcommand.
        """
        client = trtcloud_client.sweeper_client

        run_list_common(
            client=client,
            user_mode=args.me,
            since=args.since,
            until=args.until,
            limit=args.limit,
            verbose=args.verbose,
            default_limit=25,
            workload_type=WorkloadType.SINGLE_ENGINE,
            id_column_name="Build ID",
            show_trials_column=False,
        )

    def run_build(self, trtcloud_client, build_type, args):
        # TODO: move validation to the build config
        if (
            build_type is BuildType.TRT_LLM
            and args.os.lower().strip() == "windows"
            and (args.tp_size > 1 or args.pp_size > 1)
        ):
            raise ValueError("Tensor/Pipeline parallelism for inference is unsupported on Windows.")

        # TODO: local refit does not currently work
        # if args.local_refit and not args.strip_weights:
        #     raise ValueError("--local-refit is only applicable for builds with --strip-weights")

        if args.tags:
            validate_tags(args.tags)

        build_id = None
        build_config: BuildConfig | None = None
        if build_type is BuildType.ONNX:
            build_config = self.create_onnx_build_config(trtcloud_client, args)

        elif build_type is BuildType.TRT_LLM:
            build_config = self.create_trtllm_build_config(trtcloud_client, args)

        else:
            raise NotImplementedError(f"Build type {build_type} is not implemented")

        if not BuildSubcommand._credits_confirmation_prompt(
            workload_type=WorkloadType.SINGLE_ENGINE,
            gpu=args.gpu,
            max_trials=1,
            skip_prompt=args.yes,
        ):
            return

        # Submit build to orchestrator
        build_id = None
        with utils.PrintMessageOnCtrlC(
            "Interrupting the function invocation may result in the build being started without a request ID.",
            level=logging.WARNING,
        ):
            build_id = trtcloud_client.submit_build_in_orchestrator(build_config, args.tags)

        if not build_id:
            raise RuntimeError("Failed to start build: Unknown error")

        logging.info(f"Build session with build_id: {build_id} started.")
        logging.info("To check the status of the build, run:")
        logging.info(f"trt-cloud build status {build_id}")

    def create_onnx_build_config(self, trtcloud_client: TRTCloud, args: argparse.Namespace) -> ONNXBuildConfig:
        """
        Create Build Config for a TRT Engine from an ONNX model on the cloud.
        """
        input_source = BuildSubcommand._create_build_input_source(args, BuildInputFileType.ONNX)
        build_input = BuildInput(type=BuildInputFileType.ONNX, source=input_source)

        trtexec_args: List[str] = [arg for arg in (args.trtexec_args or "").split(" ") if arg]
        build_output = BuildSubcommand._get_build_output(args)
        # Start a new ONNX build
        return trtcloud_client.create_onnx_build_config(
            build_input=build_input,
            gpu=args.gpu,
            os_name=args.os,
            trt_version=args.trt_version,
            strip_weights=args.strip_weights,
            # TODO: local refit is currently broken
            local_refit=False,
            trtexec_args=trtexec_args,
            build_output=build_output,
        )

    def create_trtllm_build_config(self, trtcloud_client: TRTCloud, args: argparse.Namespace) -> TRTLLMBuildConfig:
        """
        Create Build Config for a TRT Engine from a TRT LLM model on the cloud.
        """
        requires_tokenizer = args.return_type in [
            TRTLLMBuildReturnType.ENGINE_AND_METRICS,
            TRTLLMBuildReturnType.METRICS_ONLY,
        ]
        build_inputs = BuildSubcommand._create_trtllm_build_inputs(args, requires_tokenizer)
        build_output = BuildSubcommand._get_build_output(args)
        model_family = BuildSubcommand._get_model_family(args)

        kv_quantization_type = None
        if args.quantize_kv_cache:
            is_input_model_gemma = False
            for build_input in build_inputs:
                source = build_input.source
                if isinstance(source, HFRepoInputSource) and source.id.lower().startswith("google/gemma"):
                    is_input_model_gemma = True
                    break
            if not args.quantization:
                raise ValueError("A quantization type (--quantization) is required when using --quantize-kv-cache.")
            if args.quantization is TRTLLMQuantizationType.INT4_AWQ:
                kv_quantization_type = TRTLLMKVQuantizationType.INT8
            elif args.quantization is TRTLLMQuantizationType.FP8:
                kv_quantization_type = TRTLLMKVQuantizationType.FP8
            elif args.quantization is TRTLLMQuantizationType.FULL_PREC and is_input_model_gemma:
                logging.warning("Using FP8 KV quantization for Gemma models because full precision is not supported.")
                kv_quantization_type = TRTLLMKVQuantizationType.FP8
            else:
                raise ValueError(
                    f"--quantize-kv-cache is unsupported for the input"
                    f" model and quantization type {args.quantization.value}"
                )

        if kv_quantization_type is not None:
            logging.info(
                f"Will use KV quantization type: {kv_quantization_type.value}. "
                f"Please Note: fp8 requires SM89 or higher, and is not supported on all GPUs."
            )

        trtllm_recipe = TRTLLMRecipe(
            data_type=args.dtype,
            quantization_type=args.quantization,
            kv_quantization_type=kv_quantization_type,
            max_input_len=args.max_input_len,
            max_seq_len=args.max_seq_len,
            max_batch_size=args.max_batch_size,
            max_num_tokens=args.max_num_tokens,
            tp_size=args.tp_size,
            pp_size=args.pp_size,
            trtllm_version=args.trtllm_version,
            strip_plan=args.strip_weights,
            trtllm_model_family=model_family,
        )

        return trtcloud_client.create_trtllm_build_config(
            gpu=args.gpu,
            os_name=args.os,
            trtllm_version=args.trtllm_version,
            build_inputs=build_inputs,
            trtllm_build_recipe=trtllm_recipe,
            build_return_type=args.return_type,
            build_output=build_output,
        )

    def run(self, args):
        """
        Execute the 'build' subcommand with the given args.

        The 'build' subcommand is used to start a new engine build, or to resume
        a previously-started build.

        Raises ValueError if args are invalid.
        """
        trtcloud_client = TRTCloud()
        subcommand = BuildSubCommands(args.build_type)

        if subcommand is BuildSubCommands.STATUS:
            return self.run_build_status(trtcloud_client, args.build_id, watch=args.watch)

        elif subcommand is BuildSubCommands.RESULTS:
            return self.run_build_results(trtcloud_client, args)

        elif subcommand is BuildSubCommands.LIST:
            return self.run_build_list(trtcloud_client, args)

        elif subcommand is BuildSubCommands.CANCEL:
            return self.run_build_cancel(trtcloud_client, args.build_id)

        elif subcommand is BuildSubCommands.ONNX:
            return self.run_build(trtcloud_client, BuildType.ONNX, args)

        elif subcommand is BuildSubCommands.TRT_LLM:
            return self.run_build(trtcloud_client, BuildType.TRT_LLM, args)

        logging.error(f"Unknown build subcommand {subcommand}.")
