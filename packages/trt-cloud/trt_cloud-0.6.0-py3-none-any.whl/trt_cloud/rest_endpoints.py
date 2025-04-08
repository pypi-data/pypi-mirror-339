# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import json
import logging
import os
from typing import Any, Dict, Tuple, Union

import requests

from trt_cloud import constants
from trt_cloud.state import TRTCloudConfig

ORCHESTRATOR_URL = "https://api.ngc.nvidia.com"
CUSTOM_URL_VAR_NAME = "TRTC_ORCHESTRATOR_URL"
DEFAULT_TIMEOUT = 30  # seconds per request


class EndpointException(Exception):
    pass


def make_request(
    method: str,
    endpoint: str,
    headers: Dict[str, Any] = None,
    params: Dict[str, Any] = None,
    _json: Dict[str, Any] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict:
    try:
        params = {k: v for k, v in (params or {}).items() if v is not None}
        logging.debug(f"Making request to {endpoint} with method {method}")
        # if _json:
        #     logging.debug(f"Request body:\n{json.dumps(_json, indent=2)}")
        response = requests.request(method, endpoint, headers=headers, params=params, json=_json, timeout=timeout)
        response_json = response.json()

        # logging.debug(f"Response:\n{json.dumps(response_json, indent=2)}")
        if response.ok:
            return response_json

        if response.status_code == 422:
            # for pydantic validation errors
            # https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/#handling-validation-errors
            raise EndpointException(f"Payload Validation Failed: {response_json['detail']}")

        if response.status_code in (401, 403):
            message = "Invalid nvapi key. Please use 'trt-cloud login' to update your nvapi key."
            if response.text:
                message += f"\nDetails: {response.text}"
            raise EndpointException(message)

        # catch-all for all errors thrown by orchestrator and executor
        # making assumption human-readable error is in message field due to use of http errors
        # https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/#raising-http-errors
        message = response_json.get("message", response.text) or "Unknown error"
        raise EndpointException(f"TRT-Cloud failed: {message}")
    except requests.exceptions.JSONDecodeError:
        # assuming response can be decoded using response.json()
        # rely on executor providing responses as dicts
        # https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/#response-auto-serialization
        raise EndpointException("Response content is not valid JSON.")

    except requests.exceptions.RequestException as e:
        # catches if request itself fails due to network or other issue
        raise EndpointException(f"TRT-Cloud failed: {e!s}")


# TODO(nsantos): refactor the orchestrator to not return a nested body json inside the response json!
def parse_json_response(output: Dict, key: str = None) -> Union[str, Dict[str, Any]]:
    try:
        return output[key] if key else output
    except (KeyError, json.JSONDecodeError) as e:
        logging.debug(output)
        raise EndpointException(f"Error parsing response from TRT-Cloud: {e!s}")


def get_creds(config: TRTCloudConfig) -> Tuple[str, str, str]:
    def _get_nvapi_key() -> str:
        return config.get_credential("login", "nvapi_key")

    def _get_org_and_team_id() -> Tuple[str, str]:
        return config.read_ngc_info()

    return _get_nvapi_key(), *_get_org_and_team_id()


def build_orchestrator_request(config: TRTCloudConfig, subcommand: str) -> Tuple[str, Dict[str, Any]]:
    nvapi_key, ngc_org_id, ngc_team_id = get_creds(config)
    orchestrator_url = os.getenv(CUSTOM_URL_VAR_NAME, ORCHESTRATOR_URL)
    headers = {"Authorization": f"Bearer {nvapi_key}"}

    org_id_component = f"/orgs/{ngc_org_id}"
    team_id_component = f"/teams/{ngc_team_id}" if ngc_team_id and ngc_team_id != constants.NGC_NO_TEAM else ""
    orchestrator_endpoint = f"{orchestrator_url}/v1/trtc" + org_id_component + team_id_component + f"/{subcommand}"

    return orchestrator_endpoint, headers
