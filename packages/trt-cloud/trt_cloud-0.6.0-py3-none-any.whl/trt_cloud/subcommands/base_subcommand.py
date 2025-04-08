# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import abc
import argparse
import json
import logging
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional

from trt_cloud import utils
from trt_cloud.build_spec.build_input_source import (
    BuildInput,
    BuildInputFileType,
    HFRepoInputSource,
    NGCPrivateRegistryInputSource,
    URLInputSource,
    weight_stripped_onnx_source,
    weight_stripped_trtllm_checkpoint_source,
)
from trt_cloud.build_spec.build_options import TRTLLMBuildReturnType
from trt_cloud.state import TRTCloudConfig
from trt_cloud.sweeper import (
    TERMINAL_SWEEP_STATES,
    NGCPrivateRegistryBuildOutput,
    SweeperClient,
    WorkloadType,
)

SRC_TYPES = frozenset(["huggingface_checkpoint", "trtllm_checkpoint"])


class Subcommand(abc.ABC):
    def __init__(self, prompt_license: bool = False):
        self.prompt_license = prompt_license

    @staticmethod
    @abc.abstractmethod
    def add_subparser(subparsers: argparse._SubParsersAction, subcommand_name: str) -> ArgumentParser:
        """
        Adds this subcommand's parser and arguments to the main CLI argument parser.
        """

    @abc.abstractmethod
    def run(self, args):
        """
        Run this subcommand with the parsed CLI arguments.
        """

    @staticmethod
    def _add_build_results_options(parser: argparse.ArgumentParser):
        parser.add_argument(
            "-o",
            "--dst-path",
            "--output",
            type=Path,
            help="Path to a directory where the build output will be downloaded. This can only be used if the build "
            "output was uploaded to the NGC Private Registry.",
            required=False,
        )
        parser.add_argument(
            "--dst-token",
            type=str,
            help="NGC access token to download the build output from the NGC Private Registry. This is usually only "
            "necessary if you provided a custom --dst-token when starting the build. If not provided, your "
            "saved TRT Cloud access token is used automatically.",
            required=False,
        )

    @staticmethod
    def add_src_options_to_parser(parser: argparse.ArgumentParser) -> argparse._MutuallyExclusiveGroup:
        """
        These input options are shared across sweeps, TRT-LLM single engine builds, and ONNX single engine builds.
        """
        input_group = parser.add_mutually_exclusive_group()
        input_group.add_argument(
            "--src-path",
            help="Path to a local directory or file containing the input model. If provided, this will automatically "
            "upload the input model to your organization's NGC Private Registry and use it for the build/sweep. "
            "By default, your saved TRT Cloud access token will be used to upload the model unless you provide a "
            "custom --src-token. Mutually exclusive with --src-url and --src-ngc.",
        )
        input_group.add_argument(
            "--src-url",
            help="URL containing the input model. The URL must be publicly accessible. Mutually exclusive with "
            "--src-path and --src-ngc.",
        )
        input_group.add_argument(
            "--src-ngc",
            help="Input model location in NGC Private Registry using org/[team/]name[:version] format. If an NGC API "
            "key is not provided with --src-token, your saved TRT Cloud access token will be used automatically. "
            "Mutually exclusive with --src-path and --src-url.",
        )
        parser.add_argument(
            "--src-token",
            help="Either a Hugging Face token needed to access the input model on Hugging Face Hub, or an NGC API key "
            "needed to access the input model in NGC Private Registry.",
        )
        parser.add_argument(
            "--strip-weights",
            action="store_true",
            help="This will prune weights from the model locally before uploading and build a weight-stripped TensorRT "
            "engine. Weight stripping is currently only supported for ONNX models and TRT LLM checkpoints."
            "This option cannot be used with --return-type checkpoint_only.",
        )
        return input_group

    @staticmethod
    def add_trtllm_src_options_to_parser(parser: argparse.ArgumentParser):
        """
        These input options are specific to sweeps and TRT-LLM single engine builds.
        """
        input_group = Subcommand.add_src_options_to_parser(parser)
        input_group.add_argument(
            "--src-hf-repo",
            help="Hugging Face Repo ID of the input model. Mutually exclusive with --src-path, --src-url, and "
            "--src-ngc.",
        )

        parser.add_argument(
            "--src-type",
            help="Type of the input model. This option is only required if the input model is provided via "
            "--src-path, --src-url, or --src-ngc.",
            choices=SRC_TYPES,
        )
        parser.add_argument(
            "--model-family",
            type=str,
            help="The model family (llama, gemma, phi, etc.). This option is only required if the input model is "
            "provided via --src-path, --src-url, or --src-ngc.",
        )
        parser.add_argument(
            "--weightless",
            action="store_true",
            help="If provided, the model will be retrieved without weights from Hugging Face Hub, and fake weights "
            "will be used instead. This can significantly speed up the build process. This option can only be used "
            "with a Hugging Face model provided via --src-hf-repo.",
        )

        tokenizer_input_group = parser.add_mutually_exclusive_group()
        tokenizer_input_group.add_argument(
            "--tokenizer-hf-repo",
            help="Hugging Face Repo ID of the model which will be used to retrieve the model's tokenizer. "
            "Mutually exclusive with --tokenizer-path.",
        )
        tokenizer_input_group.add_argument(
            "--tokenizer-path",
            help="Path to a local directory or file containing a tokenizer. If provided, this will automatically "
            "upload the tokenizer to your organization's NGC Private Registry and use it for the build/sweep. By "
            "default, your saved TRT Cloud access token will be used to upload the tokenizer unless you provide a "
            "custom --src-token. Mutually exclusive with --tokenizer-hf-repo.",
        )

    @staticmethod
    def _get_src_ngc_token(args):
        if args.src_token:
            nvapi_token = args.src_token
        else:
            logging.warning(
                "No NGC access token was provided with --src-token. Attempting to use your saved TRT Cloud access "
                "token to access the input on NGC Private Registry."
            )
            nvapi_token = TRTCloudConfig().read_saved_login()
        return nvapi_token

    @staticmethod
    def _create_tokenizer_source(args: argparse.Namespace):
        tokenizer_source = None
        if args.tokenizer_path:
            tokenizer_source = NGCPrivateRegistryInputSource.from_local_path(
                path=args.tokenizer_path, allowed_extensions=[".model", ".json", ".model.v3", ".zip"]
            )
        elif args.tokenizer_hf_repo:
            tokenizer_source = HFRepoInputSource(id=args.tokenizer_hf_repo)
        return tokenizer_source

    @staticmethod
    def _create_build_input_source(args: argparse.Namespace, build_input_type: BuildInputFileType):
        if args.strip_weights:
            if args.src_path:
                if build_input_type == BuildInputFileType.TRTLLM_CHECKPOINT:
                    return weight_stripped_trtllm_checkpoint_source(args.src_path)
                elif build_input_type == BuildInputFileType.ONNX:
                    return weight_stripped_onnx_source(args.src_path)
                else:
                    raise ValueError("--strip-weights is only supported with TRT LLM checkpoints and ONNX models.")
            else:
                raise ValueError("--strip-weights can only be used with --src-path.")
        elif args.src_path:
            allowed_extensions = [".zip"]
            if build_input_type == BuildInputFileType.ONNX:
                allowed_extensions.append(".onnx")
            return NGCPrivateRegistryInputSource.from_local_path(
                path=args.src_path, allowed_extensions=allowed_extensions
            )
        elif args.src_url:
            return URLInputSource(url=args.src_url)
        elif args.src_ngc:
            nvapi_token = Subcommand._get_src_ngc_token(args)
            return NGCPrivateRegistryInputSource(target=args.src_ngc, nvapi_token=nvapi_token)
        else:
            raise ValueError("Must specify --src-path, --src-url, or --src-ngc.")

    @staticmethod
    def _create_trtllm_build_inputs(args: argparse.Namespace, requires_tokenizer: bool):
        build_inputs = []

        if args.strip_weights:
            if args.return_type == TRTLLMBuildReturnType.CHECKPOINT_ONLY:
                raise ValueError(
                    "--strip-weights cannot be used with --return-type checkpoint_only as no engine will be produced."
                )
            elif args.return_type == TRTLLMBuildReturnType.METRICS_ONLY:
                raise ValueError(
                    "--strip-weights cannot be used with --return-type metrics_only as no engine will be produced."
                )

        if args.src_hf_repo:
            if args.weightless:
                build_input_type = BuildInputFileType.HF_CHECKPOINT_WEIGHTLESS
            else:
                build_input_type = BuildInputFileType.HF_CHECKPOINT
            input_source = HFRepoInputSource(id=args.src_hf_repo, token=args.src_token)
            build_inputs.append(BuildInput(type=build_input_type, source=input_source))
        elif args.src_type:
            build_input_type = BuildInputFileType(args.src_type)
            input_source = Subcommand._create_build_input_source(args, build_input_type)
            build_inputs.append(BuildInput(type=build_input_type, source=input_source))
        elif any((args.src_path, args.src_url, args.src_ngc)):
            raise ValueError(
                f"Must specify --src-type when using --src-path, --src-url, or --src-ngc. Choose from {set(SRC_TYPES)}."
            )
        else:
            raise ValueError("Must specify at least one of --src-hf-repo, --src-path, --src-url, or --src-ngc.")

        # Handle tokenizer if needed
        requires_tokenizer = requires_tokenizer and build_input_type == BuildInputFileType.TRTLLM_CHECKPOINT
        tokenizer_source = Subcommand._create_tokenizer_source(args)
        if requires_tokenizer:
            if tokenizer_source:
                build_inputs.append(BuildInput(type=BuildInputFileType.TOKENIZER, source=tokenizer_source))
            else:
                raise ValueError(
                    "Builds from TRT LLM checkpoints cannot produce metrics without a tokenizer. "
                    "Please provide a tokenizer via --tokenizer-path or --tokenizer-hf-repo."
                )
        elif tokenizer_source:
            raise ValueError("Providing a tokenizer is only allowed when the input model is a TRT-LLM Checkpoint.")

        return build_inputs

    @staticmethod
    def _get_build_output(args):
        if args.dst_token:
            nvapi_token = args.dst_token
        else:
            logging.warning(
                "No NGC access token was provided with --dst-token. Attempting to use your saved TRT Cloud access "
                "token to upload the build output to NGC."
            )
            nvapi_token = TRTCloudConfig().read_saved_login()
        return NGCPrivateRegistryBuildOutput(target=args.dst_ngc, nvapi_token=nvapi_token)

    @staticmethod
    def _add_build_output_options(parser: argparse.ArgumentParser):
        output_group = parser.add_mutually_exclusive_group(required=False)
        output_group.add_argument(
            "--dst-ngc",
            type=str,
            help=(
                "NGC Private Registry target in the format org/[team/]name[:version] where build output will be "
                "uploaded. If --dst-ngc is not provided, the build output will be uploaded to your organization's "
                "NGC Private Registry with the name 'trt-cloud-build-result-<build ID>'."
            ),
            required=False,
        )
        parser.add_argument(
            "--dst-token",
            type=str,
            help=(
                "NGC access token which will be used to upload build output to the NGC Private Registry. This option "
                "can only be used if --dst-ngc is also provided. If not provided, your default TRT Cloud access token "
                "is used automatically."
            ),
            required=False,
        )

    @staticmethod
    def _add_prompt_skip_option(parser: argparse.ArgumentParser):
        parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation prompt.")

    @staticmethod
    def _credits_confirmation_prompt(workload_type: WorkloadType, gpu: str, max_trials: int, skip_prompt: bool = False):
        client = SweeperClient()
        available_credits, credits_per_cycle, reserved_credits_per_trial, gpu_type = client.get_credits_for_gpu(gpu)
        reserved_credits = reserved_credits_per_trial * max_trials
        workload_name = workload_type.display_name.lower()

        if available_credits < reserved_credits:
            raise ValueError(
                f"Insufficient credits to start this {workload_name}. You have {available_credits:.1f} available "
                f"minutes of usage for GPU type '{gpu_type}', but at least {reserved_credits:.0f} minutes are "
                f"required. Your credits will be refilled to {credits_per_cycle:.0f} minutes each day; please try "
                "again later."
            )
        elif reserved_credits == 0:
            logging.info(f"Your org is exempt from usage credits. This {workload_name} will not consume any credits.")
        else:
            gpu_credits_description = (
                "which can be used with any GPU" if gpu_type == "any" else f"for the {gpu_type} GPU"
            )
            logging.info(
                f"You currently have {available_credits:.1f} available GPU minutes {gpu_credits_description}.\n\n"
                f"{reserved_credits:.0f} GPU minutes will be reserved up front for this {workload_name}. If the "
                f"{workload_name} ends up using more than {reserved_credits:.0f} GPU minutes, the extra usage beyond "
                f"this reserved amount will be further deducted from your balance. If the {workload_name} ends up "
                f"using less than {reserved_credits:.0f} GPU minutes, the unused reserved GPU minutes will be "
                "refunded to your balance.\n"
            )
        if skip_prompt:
            return True
        else:
            proceed = input(f"Would you like to proceed? [y/N]: ").strip().lower()
            return proceed == "y"

    @staticmethod
    def _get_model_family(args):
        if args.model_family:
            return args.model_family
        elif args.src_hf_repo is not None:
            # We can attempt to infer the model family if the input is a HF repo
            return None
        else:
            raise ValueError("Must specify --model-family when using --src-path, --src-url, or --src-ngc.")


def _check_status(
    display: utils.Display,
    user_command: str,
    client: SweeperClient,
    sweep_id: str,
    trial_id: Optional[str] = None,
    show_trials: bool = False,
    workload_type: WorkloadType | None = None,
):
    # Make the request _before_ printing the top bar to avoid partial draws
    status, sweep, trials = client.get_status(sweep_id=sweep_id, trial_id=trial_id, workload_type=workload_type)
    workload_name = "Build" if workload_type == WorkloadType.SINGLE_ENGINE else "Sweep"
    sweep_status = sweep.get("status")  # will be used to check if the sweep is terminal
    display.reset()
    display.print_top_bar()
    display.print(user_command, heading="User Command")
    # Keep the status message intact as it's important and actionable.
    display.print(status, truncate=False)
    end_timestamp = (
        "N/A"
        if "end_timestamp" not in sweep or sweep["end_timestamp"] == "1969-12-31T23:59:59"
        else sweep["end_timestamp"]
    )

    if workload_type != WorkloadType.SINGLE_ENGINE:
        sweep_info = "Total Trials: {}, Start: {}, End: {}, Tags: {}".format(
            len(trials),
            sweep["timestamp"],
            end_timestamp,
            # display.print will automatically truncate long lines so no need to truncate tags
            json.dumps(sweep["tags"]),
        )
        display.print(sweep_info)

    t_status = None
    if show_trials or trial_id:
        if not trials:
            display.print(
                f"{workload_name} does not have any {'trials' if workload_type == WorkloadType.SWEEP else 'engines'}."
            )
        else:
            for t in trials:
                t_id = t.get("id", "-1")
                t_status = t.get("status", "UNKNOWN")
                t_duration = t.get("duration", "0")
                if workload_type == WorkloadType.SINGLE_ENGINE:
                    display.print(f"    {t_duration} min")
                else:
                    if t_status == "PENDING":
                        display.print(f"    Trial {t_id} - {t_status}")
                    else:
                        display.print(f"    Trial {t_id} - {t_status} - {t_duration} min")
                if trial_id:
                    t_status_message = t.get("status_message", "")
                    display.print_middle_bar()
                    num_lines = t_status_message.count("\n")
                    display.print(f"Latest {num_lines} lines of trial log:")
                    for line in t_status_message.splitlines():
                        line = line.rstrip("\n")
                        display.print(f"    {line}")

    display.print_bottom_bar()
    if trial_id:
        return t_status not in TERMINAL_SWEEP_STATES
    else:
        return sweep_status not in TERMINAL_SWEEP_STATES
