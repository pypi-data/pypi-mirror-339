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
import logging
from argparse import ArgumentParser

from trt_cloud import utils
from trt_cloud.client import TRTCloud
from trt_cloud.subcommands.base_subcommand import Subcommand


class CreditsSubcommand(Subcommand):
    @staticmethod
    def add_subparser(subparsers: argparse._SubParsersAction, subcommand_name: str) -> ArgumentParser:
        """
        Adds the 'credits' subcommand to the main CLI argument parser.
        """
        credits_subcommand = subparsers.add_parser(
            subcommand_name, help="View your available usage credit balance for builds and sweeps."
        )

        return credits_subcommand

    def run(self, args):
        """
        Execute the 'credits' subcommand with the given args.
        """
        client = TRTCloud()
        all_credits = client.sweeper_client.get_credits_summary()

        display = utils.Display()
        display.print_top_bar()

        for i, credits_info in enumerate(all_credits):
            if credits_info["gpu_type"] == "any":
                if len(all_credits) > 1:
                    gpu = (
                        "Any (these credits can be used with any GPU except the others listed here, which have their "
                        "own credit balances)"
                    )
                else:
                    gpu = "Any (these credits can be used with any GPU)"
            else:
                gpu = credits_info["gpu_type"]
            display.print(gpu, heading="GPU")
            display.print(f"{credits_info['available_credits']:.1f} GPU minutes", heading="Available Credits")
            display.print(f"{credits_info['credits_per_cycle']:.1f} GPU minutes", heading="Credits per Day")
            if i != len(all_credits) - 1:
                display.print_middle_bar()
        display.print_bottom_bar()
        logging.info("The table above shows your available usage credit balance for builds and sweeps.")
