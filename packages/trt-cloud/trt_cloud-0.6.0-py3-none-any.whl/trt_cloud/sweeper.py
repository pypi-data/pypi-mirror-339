# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import dataclasses
import datetime
import os
import time
from typing import Any, Dict, Iterable, List, Literal, Optional, Tuple

from trt_cloud import rest_endpoints, utils
from trt_cloud.build_spec.build_input_source import BuildInput
from trt_cloud.build_spec.build_recipe import BuildRecipeSpec
from trt_cloud.ngc_registry import NGCRegistryClient
from trt_cloud.state import TRTCloudConfig
from trt_cloud.types import Base, StringEnum, SupportMatrix

# TODO: update alias in monorepo and remove from this file.
CUSTOM_URL_VAR_NAME = rest_endpoints.CUSTOM_URL_VAR_NAME

IDLE_SWEEP_STATES = frozenset({"PENDING", "QUEUED"})
RUNNING_SWEEP_STATES = frozenset({"IN_PROGRESS"})
ACTIVE_SWEEP_STATES = IDLE_SWEEP_STATES | RUNNING_SWEEP_STATES
TERMINAL_SWEEP_STATES = frozenset({"CANCELLED", "ERROR", "DONE"})


class WorkloadStatus(StringEnum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    CANCELLED = "CANCELLED"
    ERROR = "ERROR"
    DONE = "DONE"
    UNKNOWN = "UNKNOWN"


class WorkloadRequest(Base):
    pass


class SweeperRequest(WorkloadRequest):
    pass


@dataclasses.dataclass
class BuildConfigHardware(Base):
    gpu: str
    os: str = "linux"


@dataclasses.dataclass
class NGCPrivateRegistryBuildOutput(Base):
    nvapi_token: str
    target: str | None = None
    type: str = "ngc_private_registry"


BuildOutput = NGCPrivateRegistryBuildOutput


@dataclasses.dataclass
class BuildConfig(WorkloadRequest):
    """
    A generic build config, can be used for ONNX, TRTLLM, etc.
    """

    hardware: BuildConfigHardware
    build_output: BuildOutput
    inputs: List[BuildInput] = dataclasses.field(default_factory=list)
    recipes: List[BuildRecipeSpec] = dataclasses.field(default_factory=list)
    outputs: List[str] = dataclasses.field(default_factory=list)
    tags: List[str] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        # Convert dicts to their dataclass equivalents
        if self.hardware and isinstance(self.hardware, dict):
            self.hardware = BuildConfigHardware.from_dict(self.hardware)
        for i, input_spec in enumerate(self.inputs or []):
            if isinstance(input_spec, dict):
                self.inputs[i] = BuildInput.from_dict(input_spec)
        for i, recipe in enumerate(self.recipes or []):
            if isinstance(recipe, dict):
                self.recipes[i] = BuildRecipeSpec.from_dict(recipe)


@dataclasses.dataclass
class ONNXBuildConfig(BuildConfig):
    pass


@dataclasses.dataclass
class TRTLLMBuildConfig(BuildConfig):
    pass


@dataclasses.dataclass
class BuildRequest(WorkloadRequest):
    build_config: BuildConfig
    tags: List[str] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if self.build_config and isinstance(self.build_config, dict):
            self.build_config = BuildConfig.from_dict(self.build_config)

    @classmethod
    def from_onnx_dict(cls, onnx_config_dict: Dict[str, Any]) -> "BuildRequest":
        return cls(build_config=ONNXBuildConfig.from_dict(onnx_config_dict))

    @classmethod
    def from_trtllm_dict(cls, trtllm_config_dict: Dict[str, Any]) -> "BuildRequest":
        return cls(build_config=TRTLLMBuildConfig.from_dict(trtllm_config_dict))


class WorkloadType(StringEnum):
    SWEEP = "SWEEP"
    SINGLE_ENGINE = "SINGLE_ENGINE"

    @property
    def display_name(self) -> str:
        return "Engine Build" if self is WorkloadType.SINGLE_ENGINE else "Sweep"


@dataclasses.dataclass
class EngineBuildResult(Base):
    url: str | None = None
    remaining_validity_seconds: int | None = None


@dataclasses.dataclass
class WorkloadResult(Base):
    workload_id: str
    ready: bool = False
    type: WorkloadType = WorkloadType.SWEEP
    status: WorkloadStatus = WorkloadStatus.UNKNOWN
    engines: List[EngineBuildResult] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if self.engines:
            self.engines = [EngineBuildResult.from_dict(e) for e in self.engines]
        if isinstance(self.status, str):
            self.status = WorkloadStatus(self.status)


@dataclasses.dataclass
class Workload(Base):
    id: str
    user_id: str | None = None
    org_id: str | None = None
    team_id: str | None = None
    nca_id: str | None = None
    result_url: str | None = None
    inputs: Dict[str, Any] | None = None
    status: WorkloadStatus = WorkloadStatus.UNKNOWN
    status_message: str | None = None
    type: WorkloadType = WorkloadType.SWEEP
    timestamp: str | None = None
    end_timestamp: str | None = None
    tags: List[str] | None = None

    def __post_init__(self):
        if self.status:
            self.status = WorkloadStatus(self.status)
        if self.type:
            self.type = WorkloadType(self.type)

    def is_terminal(self) -> bool:
        return self.status in TERMINAL_SWEEP_STATES

    def is_active(self) -> bool:
        return self.status in ACTIVE_SWEEP_STATES

    def is_idle(self) -> bool:
        return self.status in IDLE_SWEEP_STATES

    def is_running(self) -> bool:
        return self.status in RUNNING_SWEEP_STATES


@dataclasses.dataclass
class BenchmarkProfile:
    """
    Used to specify ISL/OSL/concurrency to optimize for when getting the
    default/suggested sweep config.
    """

    # Field names must be a subset of CustomRequestsProfile (part of Sweep Config).
    concurrency: int
    input_tokens_mean: int
    output_tokens_mean: int


class SweeperClient:
    def __init__(self):
        self.config = TRTCloudConfig()

    def parse_timestamp(self, timestamp: str) -> float:
        try:
            return (
                datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
                .replace(tzinfo=datetime.timezone.utc)
                .timestamp()
            )
        except ValueError:
            raise ValueError(f"Invalid timestamp format: {timestamp}. Please use YYYY-MM-DDTHH:MM:SS format.")

    def _get_workloads(
        self,
        user_id: str | List[str] = None,
        workload_id: str | List[str] = None,
        workload_type: WorkloadType = None,
        since: str = None,
        until: str = None,
        additional_attributes: Iterable[str] = None,
    ) -> List[Dict[str, Any]]:
        url, headers = rest_endpoints.build_orchestrator_request(self.config, "sweeps")
        # Convert timestamp strings to Unix timestamps
        start_ts = None
        end_ts = None

        if since:
            start_ts = self.parse_timestamp(since)
        if until:
            end_ts = self.parse_timestamp(until)

        params = {
            "user_id": user_id,
            "sweep_id": workload_id,
            "start_ts": start_ts,
            "end_ts": end_ts,
        }
        if workload_type:
            params["workload_type"] = workload_type.value
        if additional_attributes:
            params["additional_attributes"] = list(additional_attributes)

        output = rest_endpoints.make_request("GET", url, headers=headers, params=params, timeout=60)
        return output

    def get_workloads(
        self,
        workload_id: str | List[str] | None = None,
        user_id: str | List[str] | None = None,
        workload_type: WorkloadType | None = None,
        since: str | None = None,
        until: str | None = None,
    ) -> List[Workload]:
        """
        Retrieve one or more workloads.

        Equivalent to `_get_workloads()` but returns typed `Workload` objects.
        TODO: using this one for get_sweeps()

        Args:
            workload_id (str | List[str] | None): The ID of the workload to retrieve.
            user_id (str | List[str] | None): The ID of the user to retrieve workloads for.
            workload_type (WorkloadType | None): The type of workload to retrieve.

        Returns:
            A list of workloads.
        """
        workload_rows = self._get_workloads(
            user_id=user_id, workload_id=workload_id, workload_type=workload_type, since=since, until=until
        )
        return [Workload.from_dict(w) for w in workload_rows]

    def get_sweeps(
        self,
        user_id: List[str] = None,
        sweep_id: List[str] = None,
        workload_type: WorkloadType | None = None,
        since: str | None = None,
        until: str | None = None,
    ) -> List[Dict[str, Any]]:
        return self._get_workloads(
            user_id=user_id,
            workload_id=sweep_id,
            workload_type=workload_type,
            since=since,
            until=until,
            additional_attributes=["status_message", "inputs"],
        )  # by default returns only sweeps

    def get_single_engine_builds(
        self, user_id: str | List[str] = None, build_id: str | List[str] = None
    ) -> List[Workload]:
        """
        Retrieve workloads of type `SINGLE_ENGINE`.
        """
        return self.get_workloads(user_id=user_id, workload_id=build_id, workload_type=WorkloadType.SINGLE_ENGINE)

    def get_engine_builds(self, sweep_id: str, build_id: str = None) -> List[Dict[str, Any]]:
        url, headers = rest_endpoints.build_orchestrator_request(self.config, f"sweeps/{sweep_id}/engine-builds")
        params = {
            "build_id": build_id,
        }
        output = rest_endpoints.make_request("GET", url, headers=headers, params=params, timeout=60)
        return output

    def get_status(
        self, sweep_id: str, trial_id: Optional[str] = None, workload_type: WorkloadType | None = None
    ) -> Tuple[str, List[str]]:
        sweeps_rows = self.get_sweeps(sweep_id=sweep_id, workload_type=workload_type)
        if not sweeps_rows or len(sweeps_rows) == 0:
            if workload_type == WorkloadType.SINGLE_ENGINE:
                raise rest_endpoints.EndpointException(f"Could not find the build ID: {sweep_id}")
            else:
                raise rest_endpoints.EndpointException(f"Could not find the sweep ID: {sweep_id}")
        sweep = sweeps_rows[0]
        try:
            status = sweep["status"]
            timestamp = utils.convert_str_to_int_timestamp(sweep["timestamp"])
            end_timestamp = utils.convert_str_to_int_timestamp(sweep["end_timestamp"])
            status_message = sweep.get("status_message", "")
            status_message_response = utils.get_status_message_response(
                status, status_message, timestamp, end_timestamp
            )
        except Exception as e:
            raise rest_endpoints.EndpointException(f"Failed to get & parse the sweep status: {e!s}")

        engine_build_rows = self.get_engine_builds(sweep_id=sweep_id, build_id=trial_id)
        trials = utils.get_build_info(engine_build_rows=engine_build_rows, trial_id=trial_id)
        return status_message_response, sweep, trials

    def get_engine_picks(self, sweep_id: str) -> List[Dict[str, Any]]:
        url, headers = rest_endpoints.build_orchestrator_request(self.config, f"sweeps/{sweep_id}/engine-picks")
        output = rest_endpoints.make_request("GET", url, headers=headers, timeout=60)
        return output

    def post_sweep(self, config: Dict[str, Any]) -> str:
        url, headers = rest_endpoints.build_orchestrator_request(self.config, "sweeps")
        output = rest_endpoints.make_request("POST", url, headers=headers, _json=config, timeout=60)
        return rest_endpoints.parse_json_response(output, "sweep_id")

    def post_single_engine_build(self, build_request: BuildRequest) -> str:
        """
        Trigger a single-engine build.

        Despite returning `sweep_id`, it's actually the workload ID.

        Args:
            build_request (BuildRequest): The build request to trigger.

        Returns:
            The ID of the workload.
        """
        url, headers = rest_endpoints.build_orchestrator_request(self.config, "single_engine_builds")
        request_body = build_request.to_dict()
        output = rest_endpoints.make_request("POST", url, headers=headers, _json=request_body, timeout=60)
        return rest_endpoints.parse_json_response(output, "sweep_id")

    def get_credits_for_gpu(self, gpu_name: str) -> Tuple[float, float, float, str]:
        url, headers = rest_endpoints.build_orchestrator_request(self.config, f"credits/{gpu_name}")
        output = rest_endpoints.make_request("GET", url, headers=headers, timeout=10)

        return (
            output["available_credits"],
            output["credits_per_cycle"],
            output["reserved_credits_per_trial"],
            output["gpu_type"],
        )

    def get_credits_summary(self) -> Tuple[float, float, float, str]:
        url, headers = rest_endpoints.build_orchestrator_request(self.config, "credits")
        output = rest_endpoints.make_request("GET", url, headers=headers, timeout=10)
        return output["credits"]

    def post_sweep_overview_and_wait_result(self, config: Dict[str, Any], async_timeout=600, pull_interval=2) -> str:
        start_time = time.time()

        url, headers = rest_endpoints.build_orchestrator_request(self.config, "sweeps/overview")
        output = rest_endpoints.make_request("POST", url, headers=headers, _json=config, timeout=60)
        sweep_overview_id = output["sweep_overview_id"]

        while time.time() - start_time < async_timeout:
            try:
                overview = self.get_overview(sweep_overview_id)
                if overview != "!to be generated!":
                    return overview
            except Exception as e:
                print(f"Failed to check overview status due to {e}, retrying...")
            time.sleep(pull_interval)

        failed_overview = "No overview is available. However, sweep may still be launched."
        return failed_overview

    def post_build_sweep(
        self, sweep_id: str, trial_id: str, build_output: Dict[str, Any], tags: List[str] = None
    ) -> str:
        """
        Trigger a build for a specific trial in a sweep.

        Args:
            sweep_id (str): The ID of the sweep.
            trial_id (str): The ID of the trial to build.
            build_output (Dict[str, Any]): The build output configuration.
            tags (List[str], optional): Tags to associate with the build. Defaults to None.

        Returns:
            The ID of the build.
        """
        url, headers = rest_endpoints.build_orchestrator_request(self.config, f"sweeps/{sweep_id}/build")
        params = {"trial_id": trial_id}
        payload = {"build_output": build_output}
        payload["tags"] = tags
        output = rest_endpoints.make_request("POST", url, headers=headers, params=params, _json=payload)
        return rest_endpoints.parse_json_response(output, "sweep_id")

    def post_retry(self, sweep_id: str, trial_ids: Optional[List[int]] = None) -> str:
        url, headers = rest_endpoints.build_orchestrator_request(self.config, f"sweeps/{sweep_id}/retry")
        payload = {"retry_build_ids": trial_ids} if trial_ids else None
        output = rest_endpoints.make_request("POST", url, headers=headers, _json=payload)
        return rest_endpoints.parse_json_response(output, "sweep_id")

    def _process_sweep_item(self, sweep_item: Dict[str, Any], workload_type: WorkloadType | None = None):
        sweep_id = sweep_item["id"]
        status = sweep_item["status"]
        total_trials = int(sweep_item.get("engine_builds_count", 0))
        timestamp = utils.convert_str_to_int_timestamp(sweep_item["timestamp"])
        start = int(timestamp.timestamp())
        tags = sweep_item.get("tags", [])

        end_timestamp = utils.convert_str_to_int_timestamp(sweep_item["end_timestamp"])
        duration_mins = utils.calculate_duration(start, int(end_timestamp.timestamp()), format_string=True)

        res = {
            "Status": status,
            "Start": start,
            "Duration": duration_mins,
            "Tags": tags,
        }

        if not workload_type or workload_type is WorkloadType.SWEEP:
            res["Sweep ID"] = sweep_id
            res["Total Trials"] = total_trials
        else:
            res["Build ID"] = sweep_id
        return res

    def _transform_sweep_list(self, sweeps_list):
        # Sort and format Start timestamp
        sweeps_list.sort(key=lambda x: x["Start"], reverse=True)
        for entry in sweeps_list:
            entry["Start"] = utils.convert_int_to_str_timestamp(entry["Start"])

    def get_user_ids(self) -> List[str]:
        ngc_registry = NGCRegistryClient(
            ngc_endpoint=os.environ.get("NGC_ENDPOINT"),
            auth_endpoint=os.environ.get("NGC_AUTH_ENDPOINT"),
            ngc_org=utils.get_ngc_model_org(),
            ngc_team=utils.get_ngc_model_team(),
        )
        nvapi_key, _, _ = rest_endpoints.get_creds(self.config)
        headers = {"Authorization": f"Bearer {nvapi_key}"}
        user_id = ngc_registry.get_current_user(headers=headers)
        return [user_id]

    def get_list(
        self,
        user_mode: bool = False,
        workload_type: WorkloadType | None = None,
        since: str | None = None,
        until: str | None = None,
    ) -> List[str]:
        """Get list of sweeps with optional filtering.

        Args:
            user_mode: If True, only show sweeps for current user
            since: Show sweeps since this timestamp (format: YYYY-MM-DDTHH:MM:SS)
            until: Show sweeps until this timestamp (format: YYYY-MM-DDTHH:MM:SS)
        """
        user_ids = None
        if user_mode:
            user_ids = self.get_user_ids()

        if workload_type is None:
            sweeps_table = self.get_sweeps(user_id=user_ids, since=since, until=until)
        else:
            workloads = self.get_workloads(user_id=user_ids, workload_type=workload_type, since=since, until=until)
            sweeps_table = [w.to_dict() for w in workloads]

        if not sweeps_table:
            return []

        sweeps_list = []
        for item in sweeps_table:
            sweeps_list.append(self._process_sweep_item(item, workload_type=workload_type))

        self._transform_sweep_list(sweeps_list)
        return sweeps_list

    def put_cancel(self, sweep_id: str) -> None:
        url, headers = rest_endpoints.build_orchestrator_request(self.config, f"sweeps/{sweep_id}")
        rest_endpoints.make_request("PUT", url, headers=headers, timeout=30)

    def get_results(self, sweep_id: str) -> str:
        url, headers = rest_endpoints.build_orchestrator_request(self.config, f"sweeps/{sweep_id}/results")
        output = rest_endpoints.make_request("GET", url, headers=headers)
        return rest_endpoints.parse_json_response(output)

    def get_workload_result(self, workload_id: str) -> WorkloadResult:
        url, headers = rest_endpoints.build_orchestrator_request(self.config, f"sweeps/{workload_id}/results")
        result = rest_endpoints.make_request("GET", url, headers=headers)
        return WorkloadResult.from_dict({**result, "workload_id": workload_id})

    def get_overview(self, sweep_id: str) -> str:
        url, headers = rest_endpoints.build_orchestrator_request(self.config, f"sweeps/overview/{sweep_id}")
        output = rest_endpoints.make_request("GET", url, headers=headers, timeout=30)
        return output["sweep_overview"]

    def get_default_sweep_config(
        self,
        build_inputs: list[Dict[str, any]],
        build_output: Dict[str, Any],
        model_family: Optional[str],
        gpu: str,
        os: Literal["linux", "windows"],
        benchmark_params: list[BenchmarkProfile],
        max_trials: int,
        trtllm_version: str,
        optimization_objective: str,
        apply_heuristics: bool,
    ) -> Dict[str, Any]:
        """
        Generate and return the default sweep config for the input arguments.
        This sweep config can be saved to a file and used with 'trt-cloud sweep'.
        """
        url, headers = rest_endpoints.build_orchestrator_request(self.config, "sweep-config/generate")
        payload = {
            "build_inputs": build_inputs,
            "build_output": build_output,
            "model_family": model_family,
            "gpu": gpu,
            "os": os,
            "max_trials": max_trials,
            "benchmark_request_params": [dataclasses.asdict(profile) for profile in benchmark_params],
            "trtllm_version": trtllm_version,
            "optimization_objective": optimization_objective,
            "apply_heuristics": apply_heuristics,
        }
        return rest_endpoints.make_request("POST", url, headers=headers, _json=payload, timeout=30)

    def get_support_matrix(self) -> SupportMatrix:
        """
        Get the support matrix for the current user, including the list of available functions.

        Returns:
            A SupportMatrix object containing the support matrix for the current user.
        """
        request_url, request_headers = rest_endpoints.build_orchestrator_request(
            config=self.config, subcommand="support-matrix"
        )
        response = rest_endpoints.make_request("GET", request_url, headers=request_headers, timeout=60)
        return SupportMatrix.from_dict(response)
