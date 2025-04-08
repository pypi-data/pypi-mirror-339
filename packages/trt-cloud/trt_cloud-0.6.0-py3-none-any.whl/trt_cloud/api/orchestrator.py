# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, field_serializer, Field


# TODO(nsantos): move to some shared package
class Base(BaseModel):
    def to_dict(self) -> dict:
        return self.model_dump()


class ErrorResponse(Base):
    """
    Generic error response returned from the Orchestrator API.
    """

    message: str


class OrchestratorResponse(Base):
    """
    Generic response returned from the Orchestrator API.
    """

    pass


class WorkloadStatus(str, Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    CANCELLED = "CANCELLED"
    ERROR = "ERROR"
    DONE = "DONE"
    UNKNOWN = "UNKNOWN"


class WorkloadType(str, Enum):
    SWEEP = "SWEEP"
    SINGLE_ENGINE = "SINGLE_ENGINE"

    @property
    def display_name(self) -> str:
        return "Engine Build" if self is WorkloadType.SINGLE_ENGINE else "Sweep"


class Workload(OrchestratorResponse):
    """
    A workload (single-engine build or a sweep) returned from the Orchestrator API.
    """

    id: str
    user_id: str
    org_id: str
    status: WorkloadStatus
    status_message: str
    type: WorkloadType
    timestamp: datetime
    end_timestamp: datetime | None = None
    team_id: str | None = None

    @classmethod
    def model_validate(cls, obj: dict):
        for key in ("timestamp", "end_timestamp"):
            if isinstance(obj.get(key), (int, float)):
                obj[key] = datetime.fromtimestamp(obj[key])
        return super().model_validate(obj)

    @field_serializer("timestamp", "end_timestamp")
    def serialize_datetime(self, dt: datetime | None, _info):
        if dt is None:
            return None
        return dt.strftime("%Y-%m-%dT%H:%M:%S")


class WorkloadListResponse(OrchestratorResponse):
    """
    Response returned from the Orchestrator API when listing workloads.
    """

    workloads: list[Workload]


class BuildResultEngine(Base):
    """
    Result of an engine build returned from the Orchestrator API.
    """

    url: str


class BuildResult(OrchestratorResponse):
    """
    Result of a build returned from the Orchestrator API.
    """

    id: str
    sweep_id: str
    ready: bool
    status: WorkloadStatus
    engines: list[BuildResultEngine]


class EnginePicksRow(OrchestratorResponse):
    """
    Result of an engine pick query returned from the Orchestrator API.
    """

    sweep_id: str
    profile: str | None = None
    benchmarks_url: str | None = None
    engine_build_id: str | None = None
    url: str | None = None


class BuilderFunction(Base):
    """
    A builder function returned from the Orchestrator API.

    The Orchestrator API returns the `trtVersions` and `trtllmVersions` in camelCase, but use snake_case internally.
    """

    os: str
    gpu: str
    trt_versions: List[str] = Field(default_factory=list, alias="trtVersions")
    trtllm_versions: List[str] = Field(default_factory=list, alias="trtllmVersions")
    tags: List[str] = Field(default_factory=list)
    is_stage: bool = False


class SupportMatrix(OrchestratorResponse):
    # `functions` is actually `support_matrix` in the API response
    functions: list[BuilderFunction] = Field(default_factory=list, alias="support_matrix")
    allowed_models: List[str] = Field(default_factory=list)
