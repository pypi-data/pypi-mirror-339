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
import dataclasses
import logging
from argparse import ArgumentParser
from typing import Any, Dict, List

from trt_cloud.client import TRTCloud
from trt_cloud import rest_endpoints
from trt_cloud.state import TRTCloudConfig
from trt_cloud.subcommands.base_subcommand import Subcommand
from trt_cloud.types import SupportMatrix
from trt_cloud.utils import find_parameters_to_identify_function, tabulate


class InfoSubcommand(Subcommand):
    @staticmethod
    def add_subparser(subparsers: argparse._SubParsersAction, subcommand_name: str) -> ArgumentParser:
        """
        Adds the 'info' subcommand to the main CLI argument parser.
        """
        info_subcommand = subparsers.add_parser(subcommand_name, help="Get the list of available GPUs.")
        return info_subcommand

    def get_support_matrix(self, config: TRTCloudConfig) -> SupportMatrix | None:
        request_url, request_headers = rest_endpoints.build_orchestrator_request(
            config=config, subcommand="support-matrix"
        )
        params = {
            "show_allowed_models": True,
        }
        response = rest_endpoints.make_request("GET", request_url, headers=request_headers, params=params, timeout=60)
        return SupportMatrix.from_dict(response)

    def run(self, args):
        """
        Execute the 'info' subcommand. It does not have any args.
        """
        trtcloud = TRTCloud()
        support_matrix = self.get_support_matrix(config=trtcloud.config)
        if not support_matrix or not support_matrix.functions:
            logging.warning("No builders currently available on TRT Cloud")
            return

        funcs = support_matrix.functions
        available_models = support_matrix.allowed_models
        funcs.sort(
            key=lambda f: (
                f.os,
                f.gpu,
                f.trt_versions,
                f.trtllm_versions,
            )
        )

        table_headers_short = [
            "OS",
            "GPU",
            "TRT Versions (for ONNX builds)",
            "TRT-LLM Versions",
            "Command",
        ]
        table_data_short = []
        table_data_verbose = []

        # Try these parameters (in order) until we find a unique combination that identifies the function
        func_parameters = ["os", "gpu", "trt_versions", "trtllm_versions"]
        for func in funcs:
            unique_command_items = find_parameters_to_identify_function(func, funcs, func_parameters)

            # `--tag env=STAGE` always needs to be specified, even if we don't need it to identify the function
            if func.is_stage and not any(parameter_name == "is_stage" for parameter_name, _ in unique_command_items):
                unique_command_items.append(("is_stage", True))

            command = ""
            for command_name, command_value in unique_command_items:
                if command_name == "is_stage":
                    if command_value:
                        command_name = "tag"
                        command_value = "env=STAGE"
                    else:
                        continue
                elif command_name == "tags":
                    command_name = "tag"
                else:
                    # Replace `trt_versions` and `trtllm_versions` with `...-version`
                    command_name = command_name.replace("_versions", "-version")

                command += f"--{command_name}={command_value} "

            func_trt_versions = ", ".join(sorted(func.trt_versions)) or "None"
            func_trtllm_versions = ", ".join(sorted(func.trtllm_versions)) or "None"
            row_short = [
                func.os.capitalize(),
                func.gpu,
                func_trt_versions,
                func_trtllm_versions,
                command,
            ]
            table_data_short.append(row_short)

            table_data_verbose.append(
                [
                    [f"{func.os.capitalize()} + {func.gpu}", ""],
                    ["OS", func.os],
                    ["GPU", func.gpu],
                    ["TRT Versions (for ONNX builds)", func_trt_versions],
                    ["TRT LLM Versions:", func_trtllm_versions],
                    ["Tags:", " ".join(func.tags)],
                    ["Command:", command],
                    # ["Created At:", func.created_at.astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")],
                    # ["Function ID:", func.func_id],
                    # ["Version ID:", func.version_id],
                ]
            )

        if args.verbose:
            table_str = "\n".join(tabulate(rows, headers="firstrow") for rows in table_data_verbose)
        else:
            table_str = tabulate(
                table_data_short,
                headers=table_headers_short,
            )

        logging.info("Available runners:\n" + table_str)

        if available_models:
            logging.info("Available TRT-LLM Models:\n" + "\n".join(available_models))
