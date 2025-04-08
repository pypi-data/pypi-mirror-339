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
import getpass
import logging
from argparse import ArgumentParser
from textwrap import dedent
from typing import List

from trt_cloud import constants
from trt_cloud.ngc_utils import NGCOrg, NVApiKeyScopes
from trt_cloud.state import CONFIG_FILE, TRTCloudConfig
from trt_cloud.subcommands.base_subcommand import Subcommand


class LoginSubcommand(Subcommand):
    def __init__(self):
        super().__init__(prompt_license=True)

    @staticmethod
    def add_subparser(subparsers: argparse._SubParsersAction, subcommand_name: str) -> ArgumentParser:
        """
        Adds the 'login' subcommand to the main CLI argument parser.
        """
        login_subcommand = subparsers.add_parser(
            subcommand_name,
            help="Provide credentials for using TRT-Cloud.",
            description="""
            Provide credentials for using TRT-Cloud.
            Specifying no arguments will start an interactive mode.
            """,
        )
        login_subcommand.add_argument(
            "--nvapi-key",
            help="""nvapi key with the 'TRT Cloud' and 'Private Registry' services enabled.
                    The key can be created at https://org.ngc.nvidia.com/setup/api-keys.""",
        )
        login_subcommand.add_argument("--ngc-team", help="NGC Team tied to the NGC Organization")

        return login_subcommand

    def _complete_login(self, nvapi_key, ngc_org_name, ngc_team):
        trtcloud_config = TRTCloudConfig()
        trtcloud_config.save_ngc_info(ngc_org_id=ngc_org_name, ngc_team_id=ngc_team)
        trtcloud_config.save_login(nvapi_key)
        logging.info("Saved nvapi key, NGC org, and NGC team to %s.", CONFIG_FILE)
        logging.info("Login succeeded.")

    def run(self, args):
        """
        Execute the 'login' subcommand with the given args.

        The following usages are valid:
        - Specifying --nvapi-key
        - Specifying --ngc-team, if nvapi key was previously provided
        - Specifying --nvapi-key and --ngc-team
        - Empty args (this triggers an interactive login).

        Raises ValueError if args are invalid.
        """

        # Credentials provided in command-line arguments.
        if args.ngc_team or args.nvapi_key:
            nvapi_key = args.nvapi_key
            if not nvapi_key:
                nvapi_key = TRTCloudConfig().read_saved_login()
                if not nvapi_key:
                    raise ValueError("nvapi key not found in config file. Please also pass in --nvapi-key")

            scopes = NVApiKeyScopes.from_nvapi_key(nvapi_key)
            ngc_org = scopes.org
            if args.ngc_team and args.ngc_team not in ngc_org.teams:
                raise ValueError(
                    "The given NGC team does not match any NGC teams associated with the given NGC org. "
                    f"Valid team names are: {ngc_org.teams}"
                )

            ngc_team = args.ngc_team
            if not ngc_team:
                ngc_team = ""
                logging.info("No NGC team provided, will use org-wide APIs.")

            self._complete_login(
                args.nvapi_key,
                ngc_org.name,
                args.ngc_team or "",  # "" means no team, use org-wide APIs.
            )
            return

        # Interactive Mode
        nvapi_key = getpass.getpass(
            dedent("""\
                TensorRT-Cloud Login using nvapi key:
                The key can be created at https://org.ngc.nvidia.com/setup/api-keys.
                Please make sure that the "TensorRT Cloud" and "Private Registry" service are enabled for your key.

                Please enter nvapi key (input masked): """)
        )

        scopes = NVApiKeyScopes.from_nvapi_key(nvapi_key)
        scopes.check_access()

        def select_value(name: str, values: List[str]) -> str:
            """
            Prompt user input to select a value from a list of values.
            """
            default_value = values[0]
            prompt = f"\nSelect {name}. Choices: "
            for i, value in enumerate(values):
                prompt += f"\n{i}. {value}"
                if value == default_value:
                    prompt += " (default)"
            prompt += "\nPlease enter your choice (default 0): "
            selected_value = input(prompt).strip() or default_value
            if selected_value not in values:
                # Also allow selecting index in list
                if selected_value.isdigit():
                    selected_idx = int(selected_value)
                    if not (0 <= selected_idx < len(values)):
                        raise ValueError(f"Selected choice must be between 0 and {len(values) - 1}")
                    selected_value = values[selected_idx]
                else:
                    raise ValueError(
                        f"Selected {name} {selected_value} not in the list of available {name}s ({values})"
                    )
            logging.info("Selected %s: %s", name, selected_value)
            return selected_value

        # No need to select NGC org as there is only 1 associated with an nvapi key.
        ngc_org: NGCOrg = scopes.org
        logging.info("Logging in to NGC org %s (%s)", ngc_org.display_name, ngc_org.name)

        # Select NGC team
        if not ngc_org.teams:
            ngc_team = ""
            logging.info("No NGC teams available. Will use org-wide APIs.")
        else:
            NO_TEAM = "None"
            teams = [NO_TEAM] + ngc_org.teams
            ngc_team = select_value("NGC team", teams)
            if ngc_team == NO_TEAM:
                ngc_team = constants.NGC_NO_TEAM

        self._complete_login(nvapi_key, ngc_org.name, ngc_team)
