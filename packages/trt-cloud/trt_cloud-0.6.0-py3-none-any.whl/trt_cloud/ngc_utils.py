# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import dataclasses
import logging
import os
from typing import List

import requests

DEFAULT_NGC_ENDPOINT = "https://api.ngc.nvidia.com"
DEFAULT_AUTH_ENDPOINT = "https://authn.nvidia.com/token"


def get_ngc_endpoint() -> str:
    return os.environ.get("NGC_ENDPOINT", None) or DEFAULT_NGC_ENDPOINT


def get_auth_endpoint() -> str:
    return os.environ.get("NGC_AUTH_ENDPOINT", None) or DEFAULT_AUTH_ENDPOINT


def add_response_info_to_message(err_str, response=None):
    if response is not None:
        err_str += f"\n    Response status code: {response.status_code}"
        err_str += f"\n    Response text: {response.text or '(empty response body)'}"
    return err_str


class NGCException(Exception):
    """Class for raising an NGC exception."""

    def __init__(self, message, response=None):
        err_str = add_response_info_to_message(message, response)
        super().__init__(err_str)


class InvalidNVApiKeyError(ValueError):
    # When thrown, the CLI catches it and pretty-prints the error instead
    # of showing a stacktrace like with NGCException.
    def __init__(
        self, message="Invalid nvapi key. Please use 'trt-cloud login' to update your nvapi key.", response=None
    ):
        err_str = add_response_info_to_message(message, response)
        super().__init__(err_str)


@dataclasses.dataclass
class NGCOrg:
    """
    Information about an NGC org and teams within that org.
    """

    name: str
    display_name: str

    # Could be a subset of teams in the org. Doesn't have to be all of them.
    teams: List[str]


@dataclasses.dataclass
class NVApiKeyScopes:
    """
    Describes what an nvapi key is scoped to.
    Each nvapi key is scoped to call certain APIs in a particular NGC org.

    Does not include the actual nvapi key.
    """

    # Org associated with this nvapi key.
    org: NGCOrg

    # Whether the key is scoped to access 'TensorRT Cloud' service APIs
    has_trtc_access: bool

    # Whether the key is scoped to access 'Private Registry' service APIs
    has_private_registry_access: bool

    @staticmethod
    def from_nvapi_key(nvapi_key):
        url = f"{get_ngc_endpoint()}/v3/keys/get-caller-info"
        headers = {
            "Authorization": f"Bearer {nvapi_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = f"credentials={nvapi_key}"
        response = requests.post(url, headers=headers, data=data)

        if not response.ok:
            raise InvalidNVApiKeyError(response=response)

        resp_body = response.json()

        org_name = resp_body["orgName"]
        org_display_name = None
        teams = list()

        for role in resp_body["user"]["roles"]:
            if role["org"]["name"] != org_name:
                logging.warning("Found unexpected org name in list of token scopes: %s", role["org"]["name"])
                continue

            if org_display_name is None:
                org_display_name = role["org"]["displayName"]

            if "team" in role:
                team = role["team"]["name"]
                teams.append(team)

        if org_display_name is None:
            org_display_name = org_name
            logging.error("Failed to extract display name of NGC org %s", org_name)

        enabled_products = resp_body.get("products", [])

        ngc_org = NGCOrg(name=org_name, display_name=org_display_name, teams=teams)

        return NVApiKeyScopes(
            org=ngc_org,
            has_trtc_access="trtc" in enabled_products,
            has_private_registry_access="private-registry" in enabled_products,
        )

    def check_access(self):
        if not self.has_private_registry_access:
            raise ValueError(
                "nvapi-key does not have Private Registry access. "
                "Please make sure your nvapi key has the 'Private Registry' service enabled."
            )

        if not self.has_trtc_access:
            raise ValueError(
                "nvapi-key does not have TRT Cloud access. "
                "Please make sure your nvapi key has the 'NVIDIA TensorRT Cloud' service enabled."
            )
