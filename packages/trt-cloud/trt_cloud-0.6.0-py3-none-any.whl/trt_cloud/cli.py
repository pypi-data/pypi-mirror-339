# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

"""
Entrypoint for TRT Cloud CLI.
"""

import argparse
import logging
import os
import sys
from typing import List, Optional

import requests
from packaging.version import Version

import trt_cloud.subcommands
from trt_cloud.client import BuilderFunctionException
from trt_cloud.constants import ENGINE_LICENSE_PATH, LICENSE_PATH
from trt_cloud.state import TRTCloudConfig
from trt_cloud.utils import add_verbose_flag_to_parser, check_and_display_eula
from trt_cloud.rest_endpoints import EndpointException

DISABLE_LICENSE_CHECK = os.getenv("TRTC_AGREE_TO_LICENSE") == "true"
DISABLE_VERSION_CHECK = os.getenv("TRTC_DISABLE_VERSION_CHECK") is not None


def make_parser(subcommands):
    parser = argparse.ArgumentParser(description="TensorRT Cloud CLI", allow_abbrev=False)
    parser.add_argument("--version", action="version", version=trt_cloud.__version__)
    add_verbose_flag_to_parser(parser)

    command_names = [command for command in subcommands.keys()]
    all_commands_str = "{" + ",".join(command_names) + "}"

    # Create a subparsers object to handle subcommands
    subparsers = parser.add_subparsers(
        title="Subcommands",
        dest="subcommand",
        metavar=all_commands_str,
        required=True,
    )

    for subcommand_name, subcommand in subcommands.items():
        subparser = subcommand.add_subparser(subparsers, subcommand_name)
        add_verbose_flag_to_parser(subparser)

    return parser


def should_do_license_check(args, trtc_config, subcommand) -> bool:
    if DISABLE_LICENSE_CHECK:
        return False
    elif trtc_config.agreed_to_license(trt_cloud.__version__):
        return False
    else:
        return subcommand.prompt_license


def should_do_engine_license_check(args, trtc_config, subcommand) -> bool:
    if not isinstance(subcommand, trt_cloud.subcommands.CatalogSubcommand):
        return False
    elif DISABLE_LICENSE_CHECK:
        return False
    elif trtc_config.agreed_to_engine_license(trt_cloud.__version__):
        return False
    else:
        return True


def get_latest_version() -> Version:
    pypi_url = os.getenv("TRT_CLOUD_PYPI_URL", "https://pypi.org/pypi")
    response = requests.get(f"{pypi_url}/trt-cloud/json")
    return Version(response.json()["info"]["version"])


def check_for_updates():
    """
    Check if there is a newer CLI version available on pypi and print ask the user to update to it.
    """
    try:
        latest_version: Version = get_latest_version()
    except Exception as e:
        # Sometimes connection to pypi fails.
        # Don't emit a warning since it's not critical and it can happen frequently.
        return

    if Version(trt_cloud.__version__) < latest_version:
        logging.warning(
            "New version of trt-cloud is available: %s. Please update with 'python3 -m pip install -U trt-cloud'",
            latest_version,
        )


def main(run_opts: Optional[List[str]] = None):
    logging.basicConfig(format="[%(levelname).1s] %(message)s", level=logging.INFO)
    trtc_config = TRTCloudConfig()

    subcommands = {
        "catalog": trt_cloud.subcommands.CatalogSubcommand,
        "login": trt_cloud.subcommands.LoginSubcommand,
        "info": trt_cloud.subcommands.InfoSubcommand,
        "build": trt_cloud.subcommands.BuildSubcommand,
        "sweep": trt_cloud.subcommands.SweepSubcommand,
        "refit": trt_cloud.subcommands.RefitSubcommand,
        "credits": trt_cloud.subcommands.CreditsSubcommand,
    }

    parser = make_parser(subcommands)
    if run_opts is not None:
        args = parser.parse_args(run_opts)
    else:
        args = parser.parse_args()

    if hasattr(args, "verbose") and args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    if not DISABLE_VERSION_CHECK:
        check_for_updates()

    try:
        subcommand = subcommands[args.subcommand]()

        if should_do_license_check(args, trtc_config, subcommand):
            if check_and_display_eula(LICENSE_PATH, eula_name="TRT Cloud EULA") and check_and_display_eula(
                ENGINE_LICENSE_PATH, eula_name="TRT Cloud Engine EULA"
            ):
                trtc_config.save_agreed_to_license(trt_cloud.__version__)

        if should_do_engine_license_check(args, trtc_config, subcommand):
            if check_and_display_eula(ENGINE_LICENSE_PATH, eula_name="TRT Cloud Engine EULA"):
                trtc_config.save_agreed_to_engine_license(trt_cloud.__version__)

        subcommand.run(args)
    except ValueError as e:
        logging.error(str(e))
        sys.exit(1)
    except BuilderFunctionException as e:
        logging.error(str(e))
        sys.exit(2)
    except EndpointException as e:
        logging.error(str(e))
        sys.exit(3)
    except RuntimeError as e:
        logging.error(str(e))
        sys.exit(4)
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
        sys.exit(130)
