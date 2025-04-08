# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import datetime
import json
import logging
import os
import re
import shutil
import time
import zipfile
from dataclasses import asdict, dataclass
from fnmatch import fnmatch
from packaging.version import Version
from tempfile import TemporaryDirectory
from typing import List, Optional, Set

from trt_cloud import constants, utils
from trt_cloud.build_spec.build_input_source import BuildInput
from trt_cloud.build_spec.build_options import BuildType, TRTLLMBuildReturnType
from trt_cloud.build_spec.build_recipe import BuildRecipeSpec, TrtexecArgListRecipe, TRTLLMRecipe
from trt_cloud.ngc_registry import NGCRegistryClient
from trt_cloud.refitter.refit_helper import RefitHelper
from trt_cloud.state import NGCRegistryCache, TRTCloudConfig

from trt_cloud.sweeper import (
    TERMINAL_SWEEP_STATES,
    BuildConfig,
    BuildConfigHardware,
    BuildOutput,
    BuildRequest,
    ONNXBuildConfig,
    SweeperClient,
    TRTLLMBuildConfig,
    Workload,
    WorkloadResult,
    WorkloadStatus,
    WorkloadType,
)
from trt_cloud.trtllm_helper import TRTLLMHelper
from trt_cloud.types import BuilderFunction


class BuilderFunctionException(Exception):
    """
    Exception which is raised when a Builder Function returns an error response.
    """

    pass


@dataclass
class PrebuiltEngine:
    """
    A class representing a TRT engine (or multidevice engines)
    which can be downloaded from NGC.
    """

    model_name: str
    version_name: str

    @property
    def id(self):
        return f"{self.model_name}:{self.version_name}"

    trtllm_version: str = None
    os: str = "Unknown"
    cpu_arch: str = "Unknown"
    gpu: str = "Unknown"
    num_gpus: int = -1
    max_batch_size: int = -1
    download_size: str = "Unknown"
    download_size_bytes: int = 0
    weight_stripped: bool = False
    other_attributes: dict = None

    def __post_init__(self):
        self.download_size = f"{self.download_size_bytes / 1e6:.2f} MB"

    @classmethod
    def from_attributes(cls, model_name: str, version_name: str, attributes: dict) -> "PrebuiltEngine":
        attrs = attributes.copy()
        return PrebuiltEngine(
            model_name=model_name,
            version_name=version_name,
            trtllm_version=attrs.pop("trtllm_version", "Unknown"),
            os=attrs.pop("os", "Unknown"),
            cpu_arch=attrs.pop("cpu_arch", "Unknown"),
            gpu=attrs.pop("gpu", "Unknown"),
            num_gpus=int(attrs.pop("num_gpus", -1)),
            max_batch_size=int(attrs.pop("max_batch_size", -1)),
            download_size_bytes=attrs.pop("download_size", 0),
            weight_stripped=(
                str(attrs.pop("weightless", "False")).lower() == "true"
                or str(attrs.pop("weight_stripped", "False")).lower() == "true"
            ),
            other_attributes=attrs,
        )

    def as_pretty_print_dict(self, include_all_headers=True):
        ret = asdict(self)
        ret["other_attributes"] = self.other_attributes or ""

        if not include_all_headers:
            del ret["cpu_arch"]
            del ret["max_batch_size"]
            del ret["download_size_bytes"]
            del ret["other_attributes"]
        return ret


class TRTCloud:
    """
    A client for building and downloading TRT Cloud inference engines.
    """

    def __init__(self):
        self.config = TRTCloudConfig()
        self.ngc_registry = NGCRegistryClient(
            ngc_org=utils.get_ngc_model_org(),
            ngc_team=utils.get_ngc_model_team(),
        )
        self.registry_cache = NGCRegistryCache()
        self.refit_helper = RefitHelper()

        self._sweeper_client = None

    @property
    def sweeper_client(self) -> SweeperClient:
        if self._sweeper_client is None:
            self._sweeper_client = SweeperClient()
        return self._sweeper_client

    def get_available_functions(self) -> List[BuilderFunction]:
        """
        Get the latest versions of available engine-building NVCF functions.
        """
        support_matrix = self.sweeper_client.get_support_matrix()
        if not support_matrix or not support_matrix.functions:
            raise RuntimeError("No builders currently available on TRT Cloud")
        return support_matrix.functions

    def _select_function(
        self,
        gpu: str | None = None,
        os_name: str | None = None,
        trt_version: str | None = None,
        trtllm_version: str | None = None,
    ) -> BuilderFunction:
        err_str_tail = "Please use 'trt-cloud info' to get information on available functions."
        available_functions = self.get_available_functions()
        for nvcf_func in available_functions:
            if (
                nvcf_func.os.lower() == os_name.lower()
                and nvcf_func.gpu.lower() == gpu.lower()
                and nvcf_func.supports_trt_version(trt_version)
                and nvcf_func.supports_trtllm_version(trtllm_version)
            ):
                return nvcf_func

        missing_params = f"GPU={gpu}, OS={os_name}"
        if trt_version is not None:
            missing_params += f", trt_version={trt_version}"
        if trtllm_version is not None:
            missing_params += f", trtllm_version={trtllm_version}"

        error_str = f"No available function with {missing_params}. {err_str_tail}"
        raise ValueError(error_str)

    def submit_build_in_orchestrator(
        self,
        build_config: BuildConfig,
        tags: List[str] = None,
    ) -> str:
        """
        Submit a build to the Orchestrator and return the build ID.
        """
        build_id = None
        build_request = BuildRequest(build_config=build_config)
        if tags:
            build_request.tags = tags

        build_id = self.sweeper_client.post_single_engine_build(build_request)
        if not build_id:
            raise RuntimeError("Failed to start build: Unknown error")

        logging.debug("Submitted build request. Build ID: %s", build_id)
        return build_id

    def create_onnx_build_config(
        self,
        build_input: BuildInput,
        gpu: str,
        os_name: str,
        strip_weights: bool,
        trtexec_args: List[str],
        local_refit: bool,
        build_output: BuildOutput,
        trt_version: str = "default",
    ) -> ONNXBuildConfig:
        """
        Create Build Config for a TRT Engine from an ONNX model on the cloud.

        Args:
            build_input (BuildInput):
                Build input for the ONNX model that will be built into a TRT engine.
            gpu (str):
                The GPU model which the engine should be built for. Use `trt-cloud info` to get
                the list of available GPUs.
            os_name (str):
                The name of the OS which the engine will be used on - "linux" or "windows".
            strip_weights (bool):
                Strip weights from the ONNX model before uploading it to TRT Cloud. The engine
                returned by the server will be weight-stripped. After the engine is downloaded,
                it will be refit with the original weights if 'local_refit' is True.
            trtexec_args (List[str]):
                Additional command-line arguments to pass to trtexec when building the engine.
                See the user guide for the list of allowed trtexec arguments.
            local_refit (bool):
                Used only when 'strip_weights' is True. If 'local_refit' is True, the downloaded engine
                will be refit locally with the original weights in the ONNX model.
            trt_version (str | None):
                The TRT Version to build the engine for. Can be "default", "latest", or a
                numerical TRT version such as "10.0".
            out_file (str | None):
                The path to save the built engine to. If not provided, the engine will not be saved.

        Returns:
            The ID of the build.
        """
        # Validate the os/gpu/trt/trtllm versions
        self._select_function(
            gpu,
            os_name,
            trt_version,
            None,  # trtllm_version
        )

        if strip_weights and "--stripWeights" not in set(trtexec_args):
            logging.debug("Adding --stripWeights to trtexec args for weight-stripped engine build.")
            trtexec_args.append("--stripWeights")

        build_recipe: BuildRecipeSpec = BuildRecipeSpec.from_dict(
            TrtexecArgListRecipe(trt_version, trtexec_args).get_recipe_spec()
        )
        return ONNXBuildConfig(
            hardware=BuildConfigHardware(gpu=gpu, os=os_name),
            inputs=[build_input],
            build_output=build_output,
            recipes=[build_recipe],
            outputs=["trt_engine", "trt_metrics", "timing_cache", "system_info"],
        )

    # TODO: get build status for sweeps?
    def get_single_engine_build(self, build_id: str) -> Workload:
        results = self.sweeper_client.get_single_engine_builds(build_id=build_id)
        if not results or not len(results):
            return None
        return results[0]

    def get_workload_result(self, build_id: str) -> WorkloadResult:
        return self.sweeper_client.get_workload_result(build_id)

    # TODO(nsantos): refactor interactive / CLI handling out into the subcommands
    def poll_workload_status(
        self,
        workload_id: str,
        wait_for_status: WorkloadStatus | Set[WorkloadStatus] = TERMINAL_SWEEP_STATES,
        interrupt_msg: str = "",
        workload_type: WorkloadType | None = None,
    ) -> Workload:
        """
        Poll a build until it reaches one of the specified statuses.

        Args:
            workload_id (str):
                The ID of the workload to poll.
            wait_for_status (WorkloadStatus | Set[WorkloadStatus]):
                A set of statuses that the workload should reach before returning.
                Defaults to TERMINAL_SWEEP_STATES.
            interrupt_msg (str):
                A message to display when the user interrupts the poll.

        Returns:
            The workload object.
        """
        workload: Workload | None = None
        workload_status = None
        POLL_INITIAL = 1  # seconds - start with frequent polling
        POLL_MAX = 10  # seconds - maximum polling interval
        POLL_EVERY = POLL_INITIAL  # current polling interval
        POLL_INCREASE_FACTOR = 1.5  # increase polling interval by 50% each time
        start_time = time.time() - POLL_EVERY  # skip the first wait.
        if isinstance(wait_for_status, WorkloadStatus):
            wait_for_status = {wait_for_status}

        # Do a first check before entering the polling loop
        workloads = self.sweeper_client.get_workloads(workload_id=workload_id, workload_type=workload_type)
        if not workloads:
            raise ValueError(f"{workload_type.display_name} '{workload_id}' not found")
        workload = workloads[0]
        workload_status = workload.status.value
        if workload_status in wait_for_status:
            return workload

        logging.info(
            f"Polling the status for {workload_type.display_name} '{workload_id}' "
            f"until status is one of: {', '.join(wait_for_status)}"
        )
        display = utils.Display()

        with (
            utils.PrintMessageOnCtrlC(msg=f"Poll interrupted by user. {interrupt_msg}"),
            utils.PrintNewlineOnExit(),
        ):
            while workload_status not in wait_for_status:
                end_time = time.time()
                elapsed = end_time - start_time
                if elapsed < POLL_EVERY:
                    time.sleep(POLL_EVERY - elapsed)
                    # Gradually increase polling interval up to POLL_MAX
                    if POLL_EVERY < POLL_MAX:
                        POLL_EVERY = min(POLL_EVERY * POLL_INCREASE_FACTOR, POLL_MAX)

                start_time = end_time
                now = datetime.datetime.now().strftime("%H:%M:%S")

                # TODO(nsantos): user_id?
                workloads = self.sweeper_client.get_workloads(workload_id=workload_id, workload_type=workload_type)
                if not workloads:
                    raise ValueError(f"{workload_type.display_name} '{workload_id}' not found")

                workload = workloads[0]
                workload_status = workload.status.value

                display.reset()
                display.print_top_bar()
                display.print(workload_id, heading=workload_type.display_name)
                display.print(workload_status, heading="Status")
                display.print(workload.status_message, heading="Message")
                display.print(f"{workload_status} at {now}", heading="Latest Poll")
                display.print_bottom_bar()

        return workload

    def create_trtllm_build_config(
        self,
        gpu: str,
        os_name: str,
        trtllm_version: str,
        build_inputs: list[BuildInput],
        trtllm_build_recipe: TRTLLMRecipe,
        build_return_type: Optional[TRTLLMBuildReturnType],
        build_output: BuildOutput,
    ) -> TRTLLMBuildConfig:
        # Select NVCF Function based on specified GPU and OS.
        nvcf_func = self._select_function(
            gpu,
            os_name,
            None,  # trt_version,
            trtllm_version,
        )

        build_recipes = []
        build_outputs = []
        if not nvcf_func.trtllm_versions:
            raise RuntimeError("Selected NVCF function does not have TRT LLM.")
        trtllm_version = trtllm_build_recipe.trtllm_version
        if not trtllm_version or trtllm_version == "latest":
            trtllm_version = max([Version(v) for v in nvcf_func.trtllm_versions]).base_version
            logging.info("Will build using TRT LLM version %s", trtllm_version)
            trtllm_build_recipe.set_trtllm_version(trtllm_version)
        else:
            if trtllm_version not in nvcf_func.trtllm_versions:
                raise ValueError(
                    f"The selected NVCF function does not have TRT LLM version {repr(trtllm_version)}. "
                    f"The available versions are: {nvcf_func.trtllm_versions}"
                )

        build_recipes = [BuildRecipeSpec.from_dict(trtllm_build_recipe.get_recipe_spec())]
        build_outputs = build_return_type.get_api_outputs()

        # Work around TRT-LLM crash on Windows.
        if os_name.lower() == "windows" and build_recipes:
            build_recipes[0].gemm_plugin = "auto"

        # Create build config
        return TRTLLMBuildConfig(
            hardware=BuildConfigHardware(gpu=gpu, os=os_name),
            inputs=build_inputs,
            build_output=build_output,
            recipes=build_recipes,
            outputs=build_outputs,
        )

    def _refit_onnx_model(self, engine_path: str, onnx_model_path: str, output_path: str, is_engine_vc: bool):
        try:
            self.refit_helper.refit(
                engine_path=engine_path,
                model_path=onnx_model_path,
                model_type=BuildType.ONNX,
                output_path=output_path,
                is_engine_vc=is_engine_vc,
            )
        except Exception:
            logging.exception("Unable to refit engine. Please run the refit command manually.")

    def _refit_trtllm_model(self, build_output: str, trtllm_checkpoint: str, output_path: str):
        try:
            logging.info(f"Refitting {build_output} -> {output_path}")
            self.refit_helper.refit(
                engine_path=build_output,
                model_path=trtllm_checkpoint,
                model_type=BuildType.TRT_LLM,
                output_path=output_path,
            )
            logging.info(f"Refitted engine saved to {output_path}")
        except Exception:
            logging.exception("Unable to refit engine. Please run the refit command manually.")

    def _save_build_result(
        self,
        nvcf_response,
        out_file=None,
        refit=False,
        refit_type=None,
        refit_model_path=None,
        is_engine_vc=False,
    ):
        """
        Handle a completed build given a response from NVCF.

        Either save it to a file or print out the download URL.
        """

        def get_corrected_output_filename(out_file):
            if out_file is not None and not os.path.isdir(out_file):
                filename, ext = os.path.splitext(out_file)
                if not ext:
                    out_file = f"{filename}.zip"
                    logging.info(f"Output path {filename} does not include an extension, will save as {out_file}")
                elif ext != ".zip":
                    out_file = f"{out_file}.zip"
                    logging.warning(
                        f"The output path has the extension {ext}, save as {out_file} since it will be a zip archive"
                    )
                return out_file

            out_dir = out_file
            candidate_filename = "build_result.zip"
            if out_dir is not None:
                candidate_filename = os.path.join(out_dir, candidate_filename)
            i = 1
            while os.path.isfile(candidate_filename):
                candidate_filename = f"build_result_{i}.zip"
                if out_dir is not None:
                    candidate_filename = os.path.join(out_dir, candidate_filename)
                i += 1
            return candidate_filename

        def get_refitted_output_filename(out_file: str, refit_model_type: BuildType):
            refit_output_dir = os.path.dirname(os.path.abspath(out_file))
            refit_file_name, _ = os.path.splitext(os.path.basename(os.path.abspath(out_file)))

            if refit_model_type is BuildType.ONNX:
                return os.path.join(refit_output_dir, f"{refit_file_name}_refitted.trt")
            elif refit_model_type is BuildType.TRT_LLM:
                return os.path.join(refit_output_dir, f"{refit_file_name}_refitted_trtllm")

        def peek_at_build_result(saved_zip_path):
            with zipfile.ZipFile(saved_zip_path) as zipped:
                filenames = zipped.namelist()

                # Check TRT LLM accuracy
                for filename in filenames:
                    if os.path.basename(filename) == "metrics.json":
                        with zipped.open(filename, "r") as f:
                            metrics = json.load(f)
                        rouge1 = metrics.get("rouge1")
                        if rouge1 is not None:
                            logging.info("Measured rouge1 score of engine: %f", rouge1)
                            if rouge1 < 15:
                                logging.warning("Low rouge1 score detected. Generated engine may have low accuracy. ")
                        break

                def show_build_suggestion(filename):
                    with zipped.open(filename, "r") as f:
                        output = f.read().decode()

                    for error_pattern, suggestion in constants.BUILD_SUGGESTIONS.items():
                        if error_pattern in output:
                            logging.warning(f"Detected possible error in {filename}, {suggestion}")

                def print_last_few_lines(filename, num_lines=5):
                    with zipped.open(filename, "r") as f:
                        lines = f.read().decode().rstrip("\n").splitlines(keepends=False)

                    logging.info("Last %d lines of %s:\n---", num_lines, os.path.basename(filename))
                    for line in lines[-num_lines:]:
                        logging.info("    %s", line.replace("\n", ""))
                    logging.info("---")
                    show_build_suggestion(filename)

                for filename in filenames:
                    if os.path.basename(filename) == "summarize.log":
                        print_last_few_lines(filename, num_lines=15)
                for filename in filenames:
                    if os.path.basename(filename) in {"build.log", "trtllm_build.log"}:
                        return print_last_few_lines(filename)
                for filename in filenames:
                    if os.path.basename(filename) in {"convert_checkpoint.log", "quantize.log"}:
                        return print_last_few_lines(filename)
                logging.warning("Could not find a build log in archive. Build likely failed.")
                for filename in filenames:
                    if os.path.basename(filename) == "trt_cloud.log":
                        return print_last_few_lines(filename)
                logging.warning("Could not find trt_cloud.log in archive.")

        def postprocess_build_result(out_file):
            peek_at_build_result(out_file)
            logging.info("Saved build result to %s", out_file)
            if refit:
                if refit_type is BuildType.ONNX:
                    self._refit_onnx_model(
                        engine_path=out_file,
                        onnx_model_path=refit_model_path,
                        output_path=get_refitted_output_filename(out_file, refit_type),
                        is_engine_vc=is_engine_vc,
                    )
                elif refit_type is BuildType.TRT_LLM:
                    self._refit_trtllm_model(
                        build_output=out_file,
                        trtllm_checkpoint=refit_model_path,
                        output_path=get_refitted_output_filename(out_file, refit_type),
                    )

        out_file = get_corrected_output_filename(out_file)

        # Small build results are returned in the body.
        if nvcf_response.status_code == 200:
            with open(out_file, "wb") as f:
                f.write(nvcf_response.content)
            postprocess_build_result(out_file)

        # Large builds are returned as a download URL.
        elif nvcf_response.status_code == 302:
            url = nvcf_response.headers["Location"]
            url_message = (
                f"Build result download URL: {url}."
                "\n\n"
                "!!! IMPORTANT: After downloading, you must unzip BOTH the downloaded <request_id>.zip file "
                "as well as the enclosed '<request_id>.response' file to see the build result."
                "\n\n"
            )
            logging.debug(url_message)

            with TemporaryDirectory() as tmpdir:
                try:
                    nvcf_zip_path = os.path.join(tmpdir, "nvcf_download.zip")
                    utils.download_file(url, nvcf_zip_path)
                except (Exception, KeyboardInterrupt) as e:
                    logging.error(
                        "Failed to download build result. You may still download from the URL manually. " + url_message
                    )
                    raise e

                logging.debug("Downloaded NVCF zip to %s", nvcf_zip_path)

                # Extract build from NVCF-created zip
                with zipfile.ZipFile(nvcf_zip_path, "r") as f:
                    filename = f.namelist()[0]
                    f.extract(filename)
                    shutil.move(filename, out_file)

            postprocess_build_result(out_file)

        else:
            raise ValueError(nvcf_response.status_code)

    def _handle_possible_error_response(self, response):
        """
        If the NVCF response is an error, raise a BuilderFunctionException.
        """

        status_code: int = response.status_code

        if status_code in [200, 202, 302]:
            return

        if status_code == 400:
            raise BuilderFunctionException(
                f"Build function rejected the build request with reason: \n\t{response.json()['detail']}"
            )
        elif status_code == 422:
            # Request body was invalid.
            detail = response.json()["detail"]
            try:
                errors = json.loads(detail)
                error_msg = "Build function rejected the build request with reason:"
                for error in errors:
                    if "msg" in error:
                        error = error["msg"]
                    error_msg += f"\n{json.dumps(error, indent=4)}"
            except json.decoder.JSONDecodeError:
                error_msg = detail
            raise BuilderFunctionException(error_msg)
        else:
            raise BuilderFunctionException(
                "Unknown response from builder function: \n"
                f"\tStatus Code: {response.status_code}"
                f"\tContent: {response.text}"
            )

    def get_prebuilt_models(self) -> List[str]:
        """
        Return the list of Deep Learning model names for which
        there are prebuilt engines available on TensorRT Cloud.
        """

        return self.ngc_registry.list_models_in_collection(collection_name=constants.TRTC_PREBUILT_COLLECTION_NAME)

    def get_prebuilt_engines(
        self,
        model_name: str = None,
        trtllm_version: str = None,
        os_name: str = None,
        gpu: str = None,
        glob_match_model_name: bool = True,
    ) -> List[PrebuiltEngine]:
        """
        Return the list of NVIDIA's prebuilt TensorRT engines available for download.
        """

        all_models = self.get_prebuilt_models()
        if model_name is None:
            selected_models = all_models
        else:
            if "*" in model_name or "?" in model_name or not glob_match_model_name:
                model_name_match_string = model_name
            else:
                model_name_match_string = f"{model_name}*"

            selected_models = [model for model in all_models if fnmatch(model, model_name_match_string)]

        prebuilt_engines = []

        for selected_model in selected_models:
            engines_for_model = self.ngc_registry.get_versions_for_model(model_name=selected_model)

            for version_name, attributes in engines_for_model.items():
                prebuilt_engine = PrebuiltEngine.from_attributes(
                    model_name=selected_model,
                    version_name=version_name,
                    attributes=attributes,
                )
                if trtllm_version and trtllm_version.upper() != prebuilt_engine.trtllm_version.upper():
                    continue
                if os_name and os_name.upper() != prebuilt_engine.os.upper():
                    continue
                if gpu and gpu.upper() != prebuilt_engine.gpu.upper():
                    continue
                prebuilt_engines.append(prebuilt_engine)

        return prebuilt_engines

    def download_prebuilt_engine(self, model_name: str, version_name: str, output_filepath=None):
        """
        Download a Prebuilt TRT engine from TensorRT Cloud.
        """

        candidate_engines = self.get_prebuilt_engines(model_name=model_name, glob_match_model_name=False)
        candidate_engines = [
            engine
            for engine in candidate_engines
            if engine.model_name == model_name and engine.version_name == version_name
        ]

        if not candidate_engines:
            raise ValueError(f"No engine found for model '{model_name}' called '{version_name}'")

        if len(candidate_engines) > 1:
            # Shouldn't happen but just in case.
            logging.warning(f"Found multiple engines with version {version_name}.")

        if not output_filepath:
            output_filepath = f"{model_name}_{version_name}_files.zip"
        else:
            _, file_ext = os.path.splitext(os.path.basename(output_filepath))
            if file_ext == "":
                logging.warning("No file extension provided. Adding .zip extension to the downloaded file")
                output_filepath += ".zip"
            elif file_ext != ".zip":
                logging.warning(f"Output will be saved with the extension {file_ext} but will be a zip archive.")

        self.ngc_registry.download_model(
            model_name=model_name,
            model_version=version_name,
            output_path=output_filepath,
        )

        return output_filepath
