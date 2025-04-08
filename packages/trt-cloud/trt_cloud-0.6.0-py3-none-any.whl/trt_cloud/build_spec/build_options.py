# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

from enum import Enum
from typing import List

from trt_cloud.types import StringEnum


class BuildType(StringEnum):
    ONNX = "onnx"
    TRT_LLM = "llm"


class TRTLLMBuildReturnType(StringEnum):
    CHECKPOINT_ONLY = "checkpoint_only"
    ENGINE_ONLY = "engine_only"
    METRICS_ONLY = "metrics_only"
    ENGINE_AND_METRICS = "engine_and_metrics"

    def get_api_outputs(self) -> List[str]:
        outputs = ["system_info"]
        if self is TRTLLMBuildReturnType.CHECKPOINT_ONLY:
            outputs.append("trtllm_checkpoint")
        elif self is TRTLLMBuildReturnType.ENGINE_ONLY:
            outputs.extend(["trtllm_engine", "timing_cache"])
        elif self is TRTLLMBuildReturnType.METRICS_ONLY:
            outputs.append("trtllm_metrics")
        elif self is TRTLLMBuildReturnType.ENGINE_AND_METRICS:
            outputs.extend(["trtllm_engine", "trtllm_metrics", "timing_cache"])
        else:
            raise RuntimeError("Unknown build return type: ", self.value)
        return outputs


class TRTLLMQuantizationType(StringEnum):
    FP8 = "fp8"
    INT4_AWQ = "int4_awq"
    W4A8_AWQ = "w4a8_awq"
    INT8_WO = "int8_wo"
    INT4_WO = "int4_wo"
    FULL_PREC = "full_prec"


class TRTLLMKVQuantizationType(StringEnum):
    INT8 = "int8"
    FP8 = "fp8"


class TRTLLMDtype(StringEnum):
    FLOAT16 = "float16"
    BFLOAT16 = "bfloat16"
