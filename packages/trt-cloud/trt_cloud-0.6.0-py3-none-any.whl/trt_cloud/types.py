# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import logging
from dataclasses import dataclass, field, asdict, fields
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List


class StringEnum(Enum):
    def __str__(self) -> str:
        return self.value


@dataclass
class Base:
    @classmethod
    def from_dict(cls, dict_: Dict[str, Any]) -> "Base":
        if not isinstance(dict_, dict):
            raise TypeError(f"Expected a dictionary in {cls.__name__}.from_dict(), got '{type(dict_).__name__}'")

        _fields = [f.name for f in fields(cls)]
        try:
            return cls(**{k: v for k, v in dict_.items() if v is not None and k in _fields})
        except TypeError as e:
            logging.debug(f"Failed to create {cls.__name__} from {dict_}")
            raise TypeError(f"Failed to create {cls.__name__}: invalid format") from e

    def to_dict(self, exclude_none: bool = True, exclude_empty: bool = True) -> Dict[str, Any]:
        """
        Convert the dataclass to a dictionary.

        Args:
            exclude_none (bool): Whether to exclude fields with None values.
            exclude_empty (bool): Whether to exclude fields with empty lists or dictionaries.

        Returns:
        """

        def dict_factory(items):
            if exclude_none:
                return {
                    k: v
                    for k, v in items
                    if not (exclude_none and v is None)
                    and not (exclude_empty and (isinstance(v, (list, dict)) and len(v) == 0))
                }
            return dict(items)

        return asdict(self, dict_factory=dict_factory if exclude_none or exclude_empty else None)


@dataclass
class BuilderFunction(Base):
    gpu: str
    os: str
    created_at: datetime | None = None
    trt_versions: List[str] = field(default_factory=list)
    trtllm_versions: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    is_latest: bool = True
    is_stage: bool = False

    def __post_init__(self):
        for field in ("trt_versions", "trtllm_versions"):
            value = getattr(self, field, None)
            # Support comma-separated strings in lists
            if isinstance(getattr(self, field), str):
                value = [s.strip() for s in getattr(self, field).split(",")]
                setattr(self, field, value)

            if value:
                setattr(self, field, sorted(value))

    @classmethod
    def from_dict(cls, dict_: Dict[str, Any]) -> "BuilderFunction":
        if not isinstance(dict_, dict):
            raise TypeError(f"Expected a dictionary in {cls.__name__}.from_dict(), got '{type(dict_).__name__}'")

        # Support camelcase keys
        dict_ = dict(dict_)
        if dict_.get("trtVersions"):
            dict_["trt_versions"] = dict_.pop("trtVersions")
        if dict_.get("trtllmVersions"):
            dict_["trtllm_versions"] = dict_.pop("trtllmVersions")
        return super().from_dict(dict_)

    @classmethod
    def from_nvcf_function(cls, fn: Dict[str, Any]) -> "BuilderFunction":
        """
        Convert an NVCF function to a BuilderFunction.

        Args:
            fn (Dict[str, Any]): The NVCF function as returned by the NVCF API.

        Returns:
            BuilderFunction: The converted BuilderFunction.
        """
        os_name = gpu = None
        tags = []
        trt_versions = []
        trtllm_versions = []
        is_stage = False
        created_at = None

        if not fn.get("os"):
            raise ValueError("NVCF function does not have an OS")

        if not fn.get("gpu"):
            raise ValueError("NVCF function does not have a GPU")

        # Remove trailing 'Z' which python versions <3.11 don't support
        if fn["createdAt"].endswith("Z"):
            fn["createdAt"] = f"{fn['createdAt'][:-1]}+00:00"

        created_at = datetime.fromisoformat(fn["createdAt"])

        # Parse OS, GPU, TRT, and TRT-LLM versions from the tags
        for tag in fn.get("tags") or []:
            if tag.startswith("os=") and len(tag) > 3:
                os_name = tag[3:]
            if tag.startswith("gpu=") and len(tag) > 4:
                gpu = tag[4:]
            if tag.startswith("trt_versions="):
                trt_versions = [trt_version.replace("-", ".") for trt_version in tag[len("trt_versions=") :].split("_")]
            for tagname in ["trtllm_version=", "trtllm_versions="]:
                if tag.startswith(tagname):
                    new_versions = [trt_version.replace("-", ".") for trt_version in tag[len(tagname) :].split("_")]
                    trtllm_versions.extend(v for v in new_versions if v not in trtllm_versions)

            if tag.startswith("env="):
                is_stage = tag[len("env=") :].lower() == "stage"

            if tag.startswith("trt_versions="):
                trt_versions = [trt_version.replace("-", ".") for trt_version in tag[len("trt_versions=") :].split("_")]
            if tag.startswith("trtllm_versions="):
                trtllm_versions = [
                    trtllm_version.replace("-", ".") for trtllm_version in tag[len("trtllm_versions=") :].split("_")
                ]

        # Remove tags that were just parsed
        if tags:
            tags = sorted(
                list(
                    set(
                        tag
                        for tag in tags
                        if not any(
                            tag.startswith(prefix)
                            for prefix in ("trt_versions=", "trtllm_versions=", "os=", "gpu=", "env=")
                        )
                    )
                )
            )

        return cls(
            # func_id=fn["id"],
            # version_id=fn["versionId"],
            gpu=gpu,
            os=os_name,
            created_at=created_at,
            is_latest=True,
            trt_versions=trt_versions,
            trtllm_versions=trtllm_versions,
            tags=tags,
            # is_stage=is_stage,
        )

    def _supports_version(self, version, existing_versions) -> bool:
        if version is None:
            return True

        if version in ["latest", "default"]:
            return len(existing_versions) > 0

        return version in existing_versions

    def supports_trt_version(self, trt_version):
        return self._supports_version(trt_version, self.trt_versions)

    def supports_trtllm_version(self, trtllm_version):
        return self._supports_version(trtllm_version, self.trtllm_versions)


# TODO: move to `build_spec`


@dataclass
class SupportMatrix(Base):
    # `functions` is actually `support_matrix` in the API response
    functions: list[BuilderFunction] = field(default_factory=list)
    allowed_models: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, dict_: Dict[str, Any]) -> "SupportMatrix":
        if isinstance(dict_, dict):
            dict_["functions"] = [
                BuilderFunction.from_dict(item) for item in dict_.pop("support_matrix", []) or [] if item
            ]
        return super().from_dict(dict_)
