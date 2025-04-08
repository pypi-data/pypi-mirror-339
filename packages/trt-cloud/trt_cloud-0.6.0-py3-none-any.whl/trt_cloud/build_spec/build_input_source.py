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
from enum import Enum
import logging
import os.path
import shutil
from tempfile import TemporaryDirectory
from typing import Iterable, Literal, Optional, Union

from trt_cloud import utils
from trt_cloud.polygraphy_helper import PolyGraphyCallResult, PolygraphyTool, PolygraphyToolHelper
from trt_cloud.refitter.refit_helper import RefitFileType, RefitHelper
from trt_cloud.state import NGCRegistryCache, TRTCloudConfig
from trt_cloud.trtllm_helper import TRTLLMHelper
from trt_cloud.types import Base


# TODO: most of this file is effectively duplicated from builder's BuildInput; ideally we should share the
# classes and methods between the two.
class BuildInputFileType(str, Enum):
    ONNX = "onnx"
    HF_CHECKPOINT = "huggingface_checkpoint"
    HF_CHECKPOINT_WEIGHTLESS = "huggingface_checkpoint_weightless"
    TOKENIZER = "tokenizer"
    TRTLLM_CHECKPOINT = "trtllm_checkpoint"


def _check_file_path(file_path: str, allowed_extensions: Iterable[str] = None, allow_directories=False):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Path {file_path} does not exist.")

    if os.path.isfile(file_path):
        if allowed_extensions is not None:
            _, file_ext = os.path.splitext(os.path.basename(file_path))

            if file_ext not in allowed_extensions:
                raise ValueError(
                    f"File at {file_path} has unsupported file format '{file_ext}'. Allowed extensions: "
                    f"{allowed_extensions}"
                )
    elif not allow_directories:
        raise FileNotFoundError(f"Path {file_path} is a directory but only files are allowed.")


@dataclasses.dataclass
class NGCPrivateRegistryInputSource(Base):
    target: str
    nvapi_token: str
    source_type: Literal["ngc_private_registry"] = "ngc_private_registry"

    @classmethod
    def from_local_path(cls, path: str, allowed_extensions: Iterable[str] = None) -> "NGCPrivateRegistryInputSource":
        # TODO: share the logic from builder's BuildInput._extract to validate the path, particularly for
        # directories or zip files
        _check_file_path(
            file_path=path,
            allowed_extensions=allowed_extensions,
            allow_directories=True,
        )
        ngc_model_target = NGCRegistryCache().upload_path(path)
        return cls(
            target=ngc_model_target,
            nvapi_token=TRTCloudConfig().read_saved_login(),
        )


def weight_stripped_trtllm_checkpoint_source(local_path: str) -> NGCPrivateRegistryInputSource:
    with (
        TemporaryDirectory() as weight_strip_output_dir,
        TemporaryDirectory() as weight_strip_archive_output_dir,
    ):
        with RefitHelper()._handle_llm_refit_input(RefitFileType.CHECKPOINT, local_path) as checkpoint_dir:
            logging.info(f"Pruning weights from TRT-LLM checkpoint at {checkpoint_dir}...")

            TRTLLMHelper().prune(
                checkpoint_directory=checkpoint_dir,
                output_directory=weight_strip_output_dir,
            )

        logging.info("Creating pruned checkpoint archive.")
        pruned_checkpoint_filepath = shutil.make_archive(
            base_name=os.path.join(weight_strip_archive_output_dir, "weight_pruned_checkpoint"),
            format="zip",
            root_dir=weight_strip_output_dir,
        )
        return NGCPrivateRegistryInputSource.from_local_path(path=pruned_checkpoint_filepath)


def weight_stripped_onnx_source(local_path: str) -> NGCPrivateRegistryInputSource:
    with (
        TemporaryDirectory() as weight_strip_temp_dir,
        TemporaryDirectory() as weight_strip_output_dir,
    ):
        logging.info(f"Stripping weights from ONNX model at {local_path}...")
        _, model_ext = os.path.splitext(os.path.basename(local_path))
        if model_ext == ".zip":
            weight_strip_input_onnx = utils.extract_onnx_file(weight_strip_temp_dir, local_path)
        elif model_ext == ".onnx":
            weight_strip_input_onnx = local_path
        else:
            raise ValueError(
                f"{local_path} does not appear to be a .onnx or a .zip file. "
                "Cannot prune weights from unknown file format."
            )

        polygraphy_helper = PolygraphyToolHelper(polygraphy_tool=PolygraphyTool.SURGEON)
        weight_stripped_model = os.path.join(weight_strip_output_dir, "model_weightless.onnx")
        polygraphy_call_result, polygraphy_output = polygraphy_helper.run(
            [
                "weight-strip",
                weight_strip_input_onnx,
                "-o",
                weight_stripped_model,
            ]
        )

        if polygraphy_call_result == PolyGraphyCallResult.ERROR or not os.path.exists(weight_stripped_model):
            raise RuntimeError(f"Failed to prune weights from {local_path} :\n{polygraphy_output}")
        else:
            logging.info(f"Pruned weights from {local_path} -> {weight_stripped_model}")

        # Zip in case weight_strip_output_dir contains external weight files.
        if len(os.listdir(weight_strip_output_dir)) > 1:
            weight_stripped_model = shutil.make_archive(
                os.path.join(weight_strip_temp_dir, "weights_stripped"),
                "zip",
                weight_strip_output_dir,
            )

        return NGCPrivateRegistryInputSource.from_local_path(path=weight_stripped_model)


@dataclasses.dataclass
class HFRepoInputSource(Base):
    id: str  # e.g. 'google/gemma-2b'
    token: Optional[str] = None
    source_type: Literal["huggingface_repo"] = "huggingface_repo"


@dataclasses.dataclass
class URLInputSource(Base):
    url: str
    source_type: Literal["url"] = "url"


BuildInputSource = Union[NGCPrivateRegistryInputSource, HFRepoInputSource, URLInputSource]


@dataclasses.dataclass
class BuildInput(Base):
    type: BuildInputFileType
    source: BuildInputSource
