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
import datetime
import functools
import json
import logging
import os
import shutil
from tempfile import TemporaryDirectory
import zipfile
import requests
import sys
import time
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict

import yaml

from trt_cloud import rest_endpoints, utils
from trt_cloud.build_spec.build_options import StringEnum
from trt_cloud.client import TRTCloud
from trt_cloud.subcommands.base_subcommand import Subcommand, _check_status
from trt_cloud.subcommands.utils import run_list_common, validate_tags
from trt_cloud.sweeper import TERMINAL_SWEEP_STATES, BenchmarkProfile, SweeperClient, WorkloadType

DEFAULT_MAX_TRIALS = 32
DEFAULT_OPTIMIZATION_OBJECTIVE = "throughput"
DEFAULT_TRTLLM_VERSION = "latest"
DEFAULT_CONCURRENCY = [5, 25, 50, 100]


class SweepSubCommands(StringEnum):
    STATUS = "status"
    LIST = "list"
    CANCEL = "cancel"
    RESULTS = "results"
    BUILD = "build"
    RETRY = "retry"
    SWEEP = None  # when there is no subcommand, sweep is selected


class SweepSubcommand(Subcommand):
    def __init__(self):
        self.trt_cloud = TRTCloud()
        super().__init__()

    @staticmethod
    def _add_sweep_id_argument(parser: argparse.ArgumentParser):
        parser.add_argument(
            "sweep_id",
            help="ID of the sweep for the action.",
        )

    @staticmethod
    def _add_sweep_id_flag(parser: argparse.ArgumentParser):
        parser.add_argument("-s", "--sweep-id", type=str, required=True, help="ID of the sweep for action.")

    @staticmethod
    def _add_launch_skip_options(parser: argparse.ArgumentParser):
        parser.add_argument(
            "-y",
            "--generate-overview-and-ask",
            action="store_true",
            help="Generate overview and decide whether to launch sweep after overview.",
        )
        parser.add_argument(
            "-yy",
            "--generate-overview-and-launch-sweep",
            action="store_true",
            help="Generate overview and launch sweep.",
        )
        parser.add_argument(
            "-ny",
            "--skip-overview-and-launch-sweep",
            action="store_true",
            help="Skip overview and launch sweep.",
        )

    @staticmethod
    def _add_generate_sweep_config_params(parser: argparse.ArgumentParser):
        SweepSubcommand.add_trtllm_src_options_to_parser(parser)
        parser.add_argument("--gpu", type=str, help="Target GPU")
        parser.add_argument("--os", type=str, help="linux(default) or windows", choices=["linux", "windows"])
        parser.add_argument(
            "--trtllm-version",
            type=str,
            help=f"Target TRT LLM version (default: {DEFAULT_TRTLLM_VERSION!r}).",
        )
        parser.add_argument(
            "--max-trials",
            type=int,
            help=f"The max number of trials (engine builds) to run in this sweep. (default: {DEFAULT_MAX_TRIALS})",
        )
        parser.add_argument(
            "--optimization-objective",
            required=False,
            choices=["throughput", "latency"],
            type=str,
            help=f"The objective to optimize for (default: {DEFAULT_OPTIMIZATION_OBJECTIVE!r}).",
        )
        parser.add_argument(
            "--concurrency",
            required=False,
            type=int,
            nargs="*",
            action="extend",
            help=(
                f"Concurrency to optimize for. Specify multiple times to optimize "
                f"for multiple runtime profiles (default: {DEFAULT_CONCURRENCY!r})."
            ),
        )
        parser.add_argument(
            "--input-sequence-length",
            "--isl",
            type=int,
            nargs="+",
            action="extend",
            help=(
                "Average input sequence length to optimize for. "
                "Specify multiple times to optimize for multiple runtime profiles."
            ),
        )
        parser.add_argument(
            "--output-sequence-length",
            "--osl",
            type=int,
            nargs="+",
            action="extend",
            help=(
                "Average output sequence length to optimize for. "
                "Specify multiple times to optimize for multiple runtime profiles."
            ),
        )
        parser.add_argument(
            "--save-config",
            type=Path,
            metavar="SAVE_CONFIG_FILE",
            help="File to save the sweep config to (Use either .yaml or .json extension).",
        )
        parser.add_argument(
            "--save-config-only",
            action="store_true",
            help="Save the sweep config file, but don't launch a sweep.",
        )
        parser.add_argument(
            "--save-config-with-token",
            action="store_true",
            help="Save the sweep config file with the token provided. If not set, it will be removed",
        )

    @staticmethod
    def _add_trtllm_sweep_options_to_parser(parser: argparse.ArgumentParser):
        parser.add_argument(
            "-c",
            "--config",
            help="Config file in yaml or json format to start the sweep.",
        )
        parser.add_argument(
            "-t",
            "--tags",
            nargs="+",
            help="Tags to associate to the sweep.",
            default=[],
            required=False,
        )
        SweepSubcommand._add_generate_sweep_config_params(parser)
        SweepSubcommand._add_launch_skip_options(parser)

    @staticmethod
    def _add_sweep_user_options_to_parser(parser: argparse.ArgumentParser):
        parser.add_argument("--me", action="store_true", help="Set current user.")
        parser.add_argument("--since", type=str, help="Show sweeps since this timestamp (format: YYYY-MM-DDTHH:MM:SS)")
        parser.add_argument("--until", type=str, help="Show sweeps until this timestamp (format: YYYY-MM-DDTHH:MM:SS)")
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Maximum number of sweeps to return when no time range is specified (default: 25)",
        )

    @staticmethod
    def add_subparser(subparsers: argparse._SubParsersAction, subcommand_name: str) -> ArgumentParser:
        """
        Adds the 'sweep' subcommand to the main CLI argument parser.
        """
        sweep_subcommand = subparsers.add_parser(
            subcommand_name,
            help="Sweep a TRT engine in the cloud.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        SweepSubcommand._add_trtllm_sweep_options_to_parser(sweep_subcommand)

        sweep_type = sweep_subcommand.add_subparsers(
            help="Types of model to sweep.", dest="sweep_subcommands", required=False
        )

        # Add a formatter that shows default values in the help text
        add_parser_show_defaults = functools.partial(
            sweep_type.add_parser, formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        status_subparser = add_parser_show_defaults(SweepSubCommands.STATUS.value, help="Get Status.")
        SweepSubcommand._add_sweep_id_argument(status_subparser)
        status_subparser.add_argument("-w", "--watch", action="store_true", help="Continually run the status check.")
        status_subparser.add_argument(
            "--show-trials",
            action="store_true",
            help=(
                "Shows the list of attempted trials for a specific sweep ID. "
                "Will have no effect if --trial-id is also provided."
            ),
        )
        status_subparser.add_argument(
            "-i", "--trial-id", type=str, help="ID of the trial to monitor with latest log lines."
        )

        list_subparser = add_parser_show_defaults(SweepSubCommands.LIST.value, help="List sweeps.")
        SweepSubcommand._add_sweep_user_options_to_parser(list_subparser)

        cancel_subparser = add_parser_show_defaults(SweepSubCommands.CANCEL.value, help="Cancel a running sweep.")
        SweepSubcommand._add_sweep_id_argument(cancel_subparser)

        results_subparser = add_parser_show_defaults(SweepSubCommands.RESULTS.value, help="Get results of the sweep.")
        SweepSubcommand._add_sweep_id_argument(results_subparser)
        results_subparser.add_argument(
            "-o",
            "--dst-path",
            "--output",
            type=Path,
            help="Path to a directory where the sweep output will be downloaded.",
            required=False,
        )

        build_subparser = add_parser_show_defaults(
            SweepSubCommands.BUILD.value, help="Pick and build the optimal engine of a sweep."
        )
        SweepSubcommand._add_prompt_skip_option(build_subparser)
        SweepSubcommand._add_sweep_id_argument(build_subparser)
        build_subparser.add_argument("-i", "--trial-id", type=str, help="ID of the trial to build.")
        build_subparser.add_argument(
            "-t",
            "--tags",
            nargs="+",
            help="Tags to associate with the build.",
            default=[],
            required=False,
        )
        SweepSubcommand._add_build_output_options(build_subparser)

        retry_subparser = add_parser_show_defaults(SweepSubCommands.RETRY.value, help="Retry failed builds in a sweep.")
        SweepSubcommand._add_sweep_id_argument(retry_subparser)
        SweepSubcommand._add_prompt_skip_option(retry_subparser)

        retry_subparser.add_argument(
            "-i",
            "--trial-id",
            type=lambda s: [int(item.strip()) for item in s.split(",") if item.strip()],
            help="Comma-separated list of trial IDs to retry. (e.g., 0,4,19)",
        )

        return sweep_subcommand

    @staticmethod
    def _confirmation_prompt(message: str = "", force_confirm: bool = False):
        """
        Prompt the user for confirmation before continuing.
        """
        if message:
            logging.info(message)
        if force_confirm:
            logging.info("Do you want to proceed? [y/N]: y")
            return True

        proceed = input("Do you want to proceed? [y/N]: ").strip().lower()
        return proceed == "y"

    @staticmethod
    def _launch_confirmation_prompt(args, client: SweeperClient, config: Dict[str, Any]):
        """
        Prompt the user for confirmation before continuing with a sweep job.
        """
        overview_prompt = "Generate sweep overview (could take a few minutes)?"

        if args.generate_overview_and_ask or args.generate_overview_and_launch_sweep:
            logging.info(f"{overview_prompt} [y/N]: y")
            proceed_overview = "y"
        elif args.skip_overview_and_launch_sweep:
            logging.info(f"{overview_prompt} [y/N]: N")
            proceed_overview = "N"
        else:
            proceed_overview = input(f"{overview_prompt} [y/N]: ").strip().lower()

        if proceed_overview == "y":
            # generate sweep overview
            overview = client.post_sweep_overview_and_wait_result(config)
            logging.info(overview)

        gpu = config.get("sweep_config", {}).get("hardware", {}).get("gpu")
        if gpu is None:
            raise ValueError('config["sweep_config"]["hardware"]["gpu"] must be set in the config file.')
        max_trials = config.get("sweep_config", {}).get("search_strategy", {}).get("max_trials", DEFAULT_MAX_TRIALS)
        skip_prompt = args.generate_overview_and_launch_sweep or args.skip_overview_and_launch_sweep
        return SweepSubcommand._credits_confirmation_prompt(
            workload_type=WorkloadType.SWEEP,
            gpu=gpu,
            max_trials=max_trials,
            skip_prompt=skip_prompt,
        )

    @staticmethod
    def _validate_token(config: Dict[str, Any]) -> bool:
        """
        Validate that the token in the given sweep_config is not masked or empty.
        """
        sweep_config = config.get("sweep_config", {})
        build_inputs = sweep_config.get("build_inputs", [])

        for build_input in build_inputs:
            source = build_input.get("source", {})
            token = source.get("token")

            if token is not None and (not token or all(letter == "*" for letter in token)):
                raise ValueError("sweep_config/build_inputs/source/token is either empty or masked.")
        return True

    @staticmethod
    def _check_config(config: Dict[str, Any]):
        """
        Check if the config file is valid.
        """
        if not config:
            raise ValueError("Config file is empty.")

        if "sweep_config" not in config:
            raise ValueError("Config file does not contain 'sweep_config' key.")

        if "hardware" not in config["sweep_config"]:
            raise ValueError("Config file does not contain 'hardware' key in 'sweep_config'.")

        if "gpu" not in config["sweep_config"]["hardware"]:
            raise ValueError("Config file does not contain 'gpu' key in 'hardware'.")

        SweepSubcommand._validate_token(config)

    def run_sweep(self, args):
        """
        Executes sweep subcommand and starts a sweep job on TRTC.
        """
        client = self.trt_cloud.sweeper_client

        # Set default OS to linux if not provided
        if args.config is None and args.os is None:
            args.os = "linux"

        if args.save_config_only and not args.save_config:
            raise ValueError("Must provide --save-config with --save-config-only.")

        if args.save_config_with_token and not args.src_token:
            args.save_config_with_token = False
            logging.warning("Token is not provided, --save-config-with-token will be ignored")

        if args.save_config_with_token and not args.save_config:
            raise ValueError("Must provide --save-config with --save-config-with-token.")

        if args.config and args.save_config:
            raise ValueError("Cannot provide --save-config together with --config")

        config = SweepSubcommand._get_config_for_run_sweep(client, args)

        if not config:
            raise SystemExit("Failed to generate the sweep config")

        if args.save_config and not args.save_config_with_token:
            # Save the config to local without token injected
            _save_config(config, args.save_config)
            logging.info(f"Saved generated sweep config to {args.save_config}.")
            if args.save_config_only:
                return

        if args.src_token:
            # Inject the token to the config
            build_inputs = config["sweep_config"]["build_inputs"]
            for build_input in build_inputs:
                source = build_input["source"]
                if source["source_type"] == "huggingface_repo":
                    source["token"] = args.src_token
                if source["source_type"] == "ngc_private_registry":
                    source["nvapi_token"] = args.src_token

            if args.save_config_with_token:
                # Save the config with token injected
                _save_config(config, args.save_config)
                logging.info(f"Saved generated sweep config to {args.save_config}.")
                if args.save_config_only:
                    return

        if SweepSubcommand._launch_confirmation_prompt(args, client, config):
            sweep_id = client.post_sweep(config)
            logging.info(f"Sweep session with sweep_id: {sweep_id} started.")
            logging.info("To check the status of the sweep, use:")
            logging.info(f"trt-cloud sweep status {sweep_id}")
        else:
            logging.info("Operation cancelled.")

    def run_status(self, args):
        """
        Executes run subcommand.
        """
        client = self.trt_cloud.sweeper_client
        display = utils.Display()

        with (
            utils.PrintMessageOnCtrlC(
                msg=f"Caught KeyboardInterrupt. Build status may be queried using sweep ID {args.sweep_id}."
            ),
            utils.PrintNewlineOnExit(),
        ):
            user_command = " ".join(sys.argv[1:])
            check_status = functools.partial(
                _check_status,
                display=display,
                user_command=user_command,
                client=client,
                sweep_id=args.sweep_id,
                trial_id=args.trial_id,
                show_trials=args.show_trials,
            )

            if args.watch:
                while check_status():
                    time.sleep(5)
            else:
                check_status()

    def run_list(self, args):
        """
        Executes list subcommand.
        """
        client = self.trt_cloud.sweeper_client

        run_list_common(
            client=client,
            user_mode=args.me,
            since=args.since,
            until=args.until,
            limit=args.limit,
            verbose=args.verbose,
            default_limit=25,
            workload_type=None,
            id_column_name="Sweep ID",
            show_trials_column=True,
        )

    def run_cancel(self, args):
        """
        Placeholder for executing cancel subcommand.
        """
        client = self.trt_cloud.sweeper_client
        client.put_cancel(args.sweep_id)
        logging.info(f"Cancelled sweep session with sweep_id: {args.sweep_id} ")

    def run_results(self, args):
        """
        Placeholder for executing results subcommand.
        """
        client = self.trt_cloud.sweeper_client
        response = client.get_results(args.sweep_id)

        ready, status = response["ready"], response["status"]
        if not ready:
            logging.info(f"Results are not ready (sweep status: {status}).")
            return

        results = response["results"]
        if url := results["url"]:
            remaining_validity = datetime.timedelta(seconds=results["remaining_validity_seconds"])
            logging.info(f"Benchmark results (valid for {remaining_validity}): {url}")

            output_path: str | None = None
            if args.dst_path:
                output_path = os.path.abspath(args.dst_path)
            elif input("Would you like to download the benchmark results? [y/N]: ").strip().lower() == "y":
                output_path = os.path.join(os.getcwd(), "trt-cloud-sweep-results-" + args.sweep_id)

            # Download results from presigned URL to destination path
            if output_path:
                logging.info(f"Downloading results to: {output_path}")

                if os.path.exists(output_path):
                    raise ValueError(f"Destination path {output_path} already exists")

                # Create parent directories if they don't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                try:
                    response = requests.get(url, stream=True)
                    response.raise_for_status()

                    with TemporaryDirectory() as tmpdir:
                        temp_file = os.path.join(tmpdir, "results.zip")
                        with open(temp_file, "wb") as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)

                        if output_path.endswith(".zip"):
                            shutil.move(temp_file, output_path)
                        else:
                            with zipfile.ZipFile(temp_file, "r") as zip:
                                zip.extractall(tmpdir)
                            shutil.move(os.path.join(tmpdir, args.sweep_id), output_path)
                except requests.exceptions.RequestException as e:
                    raise RuntimeError(f"Failed to download results: {e}")
        else:
            logging.info(
                "The sweep does not contain benchmark results, likely failing before any trials "
                "were attempted. For more details on its status, use the status subcommand."
            )

    def run_build(self, args):
        """
        Executes build subcommand.
        """
        client = self.trt_cloud.sweeper_client
        build_output = SweepSubcommand._get_build_output(args)
        sweeps_rows = client.get_sweeps(sweep_id=args.sweep_id, workload_type=WorkloadType.SWEEP)
        if not sweeps_rows:
            logging.error(f"Sweep {args.sweep_id} is not found.")
            return
        sweep = sweeps_rows[0]

        trial_ids = []
        if args.trial_id:
            engine_build_rows = client.get_engine_builds(sweep_id=args.sweep_id, build_id=args.trial_id)
            if not engine_build_rows:
                logging.error(f"Trial {args.trial_id} is not found.")
                return
            build_description = f"Building engine for trial {args.trial_id}"
            trial_ids.append((build_description, args.trial_id))
        else:
            if sweep["status"] not in TERMINAL_SWEEP_STATES:
                logging.error("Sweep is not done yet. Please wait for the sweep to finish, or provide a trial ID.")
                return

            engine_picks = client.get_engine_picks(args.sweep_id)
            for trial in engine_picks:
                build_description = (
                    f"Building optimized engine for {trial['profile']} (trial {trial['engine_build_id']})"
                )
                trial_ids.append((build_description, trial["engine_build_id"]))

        if not trial_ids:
            logging.error("Did not find any engines to build.")
            return

        for build_description, trial_id in trial_ids:
            confirmed = SweepSubcommand._credits_confirmation_prompt(
                workload_type=WorkloadType.SINGLE_ENGINE,
                gpu=sweep["inputs"]["hardware"]["gpu"],
                max_trials=1,
                skip_prompt=args.yes,
            )
            if confirmed:
                build_id = client.post_build_sweep(args.sweep_id, trial_id, build_output.to_dict(), args.tags)
                logging.info(f"{build_description} started. Build ID: {build_id}.")
                logging.info(f"trt-cloud build status {build_id}")

    def run_retry(self, args):
        """
        Executes retry subcommand.
        """
        client = self.trt_cloud.sweeper_client
        if self._confirmation_prompt(force_confirm=args.yes):
            trial_ids = args.trial_id if args.trial_id else None
            sweep_id = client.post_retry(args.sweep_id, trial_ids)

            if trial_ids:
                logging.info(f"Retrying builds {trial_ids} for sweep_id: {sweep_id} started.")
            else:
                logging.info(f"Retrying all failed builds for sweep_id: {sweep_id} started.")
        else:
            logging.info("Operation cancelled.")

    @staticmethod
    def _get_config_for_run_sweep(client, args):
        if args.config:
            bad_args = [
                "src_hf_repo",
                "src_ngc",
                "src_path",
                "src_url",
                "src_token",
                "src_type",
                "tokenizer_path",
                "tokenizer_hf_repo",
                "strip_weights",
                "weightless",
                "model_family",
                "gpu",
                "os",
                "trtllm_version",
                "max_trials",
                "optimization_objective",
                "concurrency",
                "input_sequence_length",
                "output_sequence_length",
                "save_config",
                "save_config_only",
                "save_config_with_token",
            ]
            for bad_arg in bad_args:
                if getattr(args, bad_arg):
                    raise ValueError(f"Cannot use --{bad_arg.replace('_', '-')} with -c/--config.")
            config = _get_config(args.config, args.tags)
            SweepSubcommand._check_config(config)
        else:
            logging.info("Generating sweep config file using the provided arguments.")
            config = SweepSubcommand._get_default_sweep_config(client, args)
        return config

    @staticmethod
    def _get_default_sweep_config(client: SweeperClient, args):
        build_inputs = SweepSubcommand._create_trtllm_build_inputs(args, requires_tokenizer=True)
        # Check other required args
        required_args = [
            "gpu",
            "input_sequence_length",
            "output_sequence_length",
        ]
        for required_arg in required_args:
            if getattr(args, required_arg, None) is None:
                raise ValueError(f"Missing required arg: --{required_arg.replace('_', '-')}.")

        isl = args.input_sequence_length
        osl = args.output_sequence_length
        concurrency = args.concurrency or DEFAULT_CONCURRENCY
        if len(isl) == 1 and len(osl) == 1 and len(concurrency) > 1:
            # repeat isl/osl settings to number of concurrency benchmarks
            # isl and osl are lists of length 1
            isl = isl * len(concurrency)
            osl = osl * len(concurrency)
        if len(isl) != len(osl) or len(isl) != len(concurrency):
            # check that benchmark is configured properly
            raise ValueError("Must provide an equal number of values to --isl, --osl, and --concurrency")

        benchmark_params = [
            BenchmarkProfile(
                input_tokens_mean=isl[i],
                output_tokens_mean=osl[i],
                concurrency=concurrency[i],
            )
            for i in range(len(concurrency))
        ]

        for apply_heuristics in [True, False]:
            try:
                config = client.get_default_sweep_config(
                    build_inputs=[build_input.to_dict() for build_input in build_inputs],
                    build_output=None,
                    model_family=SweepSubcommand._get_model_family(args),
                    gpu=args.gpu,
                    os=args.os,
                    benchmark_params=benchmark_params,
                    max_trials=args.max_trials or DEFAULT_MAX_TRIALS,
                    trtllm_version=args.trtllm_version or DEFAULT_TRTLLM_VERSION,
                    optimization_objective=args.optimization_objective or DEFAULT_OPTIMIZATION_OBJECTIVE,
                    apply_heuristics=apply_heuristics,
                )

                validate_tags(args.tags)
                if args.tags:
                    config["tags"] = args.tags

                return config
            except rest_endpoints.EndpointException as e:
                if "Heuristics for this configuration are unsupported" in str(e):
                    if SweepSubcommand._confirmation_prompt(
                        message=f"No information about {args.src_hf_repo} on {args.gpu}, sweeping without heuristics.",
                        force_confirm=False,
                    ):
                        continue
                raise

    def run(self, args):
        """
        Execute the sweep subcommand and the other commands nested beneath which include:
            {status, list, cancel, results}
        """
        sweep_subcommands = SweepSubCommands(args.sweep_subcommands)

        select_subfunction = {
            SweepSubCommands.SWEEP: self.run_sweep,
            SweepSubCommands.STATUS: self.run_status,
            SweepSubCommands.LIST: self.run_list,
            SweepSubCommands.CANCEL: self.run_cancel,
            SweepSubCommands.RESULTS: self.run_results,
            SweepSubCommands.BUILD: self.run_build,
            SweepSubCommands.RETRY: self.run_retry,
        }
        select_subfunction[sweep_subcommands](args)


def _get_config(config_path, tags) -> Dict[str, Any]:
    if config_path is None:
        raise ValueError(
            'Must provide the -c, --config flag when calling trt-cloud sweep. For example: trt-cloud \
                            sweep -c "config.json"'
        )
    validate_tags(tags)

    config_path = Path(config_path)
    if not config_path.exists() or not config_path.is_file():
        raise FileNotFoundError(f"Config file {config_path} does not exist or is not a file")

    with open(config_path, "r") as file:
        if config_path.suffix == ".json":
            config = json.load(file)

        elif config_path.suffix in [".yaml", ".yml"]:
            config = yaml.safe_load(file)
        else:
            raise ValueError(f"Unsupported file type: {config_path.suffix}. Only .json and .yaml are supported.")
    if tags:
        config["tags"] = tags
    return config


def _save_config(config: Dict[str, Any], config_path: Path):
    with open(config_path, "w") as file:
        if config_path.suffix == ".json":
            json.dump(config, file, sort_keys=True, indent=4)
        elif config_path.suffix in [".yaml", ".yml"]:
            yaml.dump(config, file)
        else:
            raise ValueError(f"Unsupported file type: {config_path.suffix}. Only .json and .yaml are supported.")
