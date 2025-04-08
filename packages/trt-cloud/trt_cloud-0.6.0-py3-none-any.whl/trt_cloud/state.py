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
Manage state for the TRT Cloud CLI which is preserved between uses.

Currently this includes a config file with login credentials and a NGC Private Registry cache.
"""

import configparser
import dataclasses
import datetime
import hashlib
import json
import logging
import os
import platform
import shutil
from typing import Dict, List, Optional, Tuple
import uuid

from rich.progress import BarColumn, DownloadColumn, Progress, TaskProgressColumn, TextColumn, TimeRemainingColumn

from trt_cloud import constants

# Directory where TRT Cloud stores persistent state.
TRT_CLOUD_DIR = {
    "Linux": os.path.join(os.path.expanduser("~"), ".trt-cloud"),
    "Darwin": os.path.join(os.path.expanduser("~"), ".trt-cloud"),
    "Windows": os.path.join(os.path.expandvars("%appdata%"), "NVIDIA", "TRT Cloud"),
}[platform.system()]

CONFIG_FILE = os.path.join(TRT_CLOUD_DIR, "config")
CONFIG_FILE_BACKUP = os.path.join(TRT_CLOUD_DIR, "config.backup")
PRIVATE_REGISTRY_CACHE_FILE = os.path.join(TRT_CLOUD_DIR, "ngc_private_registry_cache.json")


class CredentialError(ValueError):
    pass


def _create_trt_cloud_dir():
    """Create a directory for storing TRT Cloud state."""
    os.makedirs(TRT_CLOUD_DIR, exist_ok=True)


class TRTCloudConfig:
    """
    Class for managing persistent user config for TRT Cloud.
    """

    CONFIG_CREDENTIALS = ["ngc", "login"]

    def __init__(self):
        _create_trt_cloud_dir()

        # Create config if it doesn't already exist.
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "x"):
                pass

    def read_saved_login(self) -> str:
        """
        Read login credentials from the config file.
        """
        return self._read_config(parent="login", child="nvapi_key")

    def save_login(
        self,
        nvapi_key: str,
    ):
        """
        Write login credentials to the config file.
        NOTE: credentials are stored in plaintext.
        """
        self._write_config(parent="login", child="nvapi_key", value=nvapi_key)

    def read_ngc_info(self) -> Tuple[str, str]:
        """
        Read login credentials from the config file.
        """
        return (
            self.get_credential(parent="ngc", child="ngc_org_id"),
            self.get_credential(parent="ngc", child="ngc_team_id", optional=True),
        )

    def save_ngc_info(self, ngc_org_id=None, ngc_team_id=None):
        self._write_config(parent="ngc", child=None, value={})
        self._write_config(parent="ngc", child="ngc_org_id", value=ngc_org_id)
        self._write_config(parent="ngc", child="ngc_team_id", value=ngc_team_id)

    def get_credential(self, parent, child, optional=False):
        val = self._read_config(parent=parent, child=child)
        if not optional and not val:
            raise CredentialError(f"The credential: {child} is not found. Please use trt-cloud login to add it.")
        return val

    def backup(self):
        """Back up the config file."""
        shutil.copy(CONFIG_FILE, CONFIG_FILE_BACKUP)

    def restore_backup(self):
        """Restore the config file backup."""
        shutil.copy(CONFIG_FILE_BACKUP, CONFIG_FILE)

    def agreed_to_license(self, version: str) -> bool:
        """Return whether the user has agreed to the TRT Cloud license."""
        return bool(self._read_config("license", version))

    def save_agreed_to_license(self, version: str):
        """Agree to the TRT Cloud license."""
        self._write_config("license", version, "True")

    def agreed_to_engine_license(self, version: str) -> bool:
        """Return whether the user has agreed to the TRT Cloud Prebuilt Engine license."""
        return bool(self._read_config("prebuilt_license", version))

    def save_agreed_to_engine_license(self, version: str):
        """Agree to the TRT Cloud Prebuilt Engine license."""
        self._write_config("prebuilt_license", version, "True")

    def _clear_children(self, to_clear: List[str]):
        for c in to_clear:
            self._write_config(parent=c, child=None, value={})

    def _read_config(self, parent: str, child: str) -> str:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        if parent not in config:
            return None

        return config[parent].get(child)

    def _write_config(self, parent: str, child: Optional[str], value: Optional[str]):
        if value is None:
            return

        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        if child is not None:
            if parent not in config:
                config[parent] = {}
            config[parent][child] = value
        else:
            config[parent] = value

        with open(CONFIG_FILE, "w") as f:
            config.write(f)


@dataclasses.dataclass
class NGCModel:
    org: str
    team: str
    model_name: str
    version: str

    @property
    def _team_str(self) -> str:
        # Even though most NGC print-outs show "no-team" when selecting the default team, most
        # assets, including NGC private registry models, actually skip the team name when that is
        # the case.
        if self.team == constants.NGC_NO_TEAM:
            return ""
        if self.team:
            return f"{self.team}/"
        return ""

    @property
    def target(self) -> str:
        return f"{self.org}/{self._team_str}{self.model_name}:{self.version}"

    @property
    def target_without_version(self) -> str:
        return f"{self.org}/{self._team_str}{self.model_name}"


class NGCRegistryCache:
    """
    Class for reading and writing to the NGC private registry cache.
    The cache is helpful to prevent uploading the same input file or directory multiple times.

    The cache file has the following JSON format:

    {
        "<file_or_dir_hash>": {
            "org": <str>,
            "team": <str>,
            "model_name": <str>,
            "version": <str>,
        },
        ...
    },
    """

    def __init__(self):
        _create_trt_cloud_dir()

        # Create cache file if it doesn't already exist.
        if not os.path.exists(PRIVATE_REGISTRY_CACHE_FILE):
            self.clear()

    def file_hash(self, filepath: str) -> str:
        """
        Compute the SHA256 hash of a file.
        """
        block_size = 64 * 1024
        sha = hashlib.sha256()
        with open(filepath, "rb") as f:
            blob = f.read(block_size)
            while blob:
                sha.update(blob)
                blob = f.read(block_size)
        return sha.hexdigest()

    def path_hash(self, path: str) -> str:
        """
        Compute the SHA256 hash of a file or directory.

        Adapted from https://stackoverflow.com/a/49701019.
        """
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Input path {abs_path} does not exist.")

        if os.path.isfile(abs_path):
            return self.file_hash(abs_path)

        digest = hashlib.sha256()
        for root, _, files in sorted(os.walk(path)):
            for file in files:
                file_path = os.path.join(root, file)

                # Hash the relative path and add to the digest to account for empty files
                relative_path = os.path.relpath(file_path, path)
                digest.update(hashlib.sha256(relative_path.encode()).digest())

                if os.path.isfile(file_path):
                    file_hash = self.file_hash(file_path)
                    digest.update(file_hash.encode())

        return digest.hexdigest()

    def read(self) -> Dict[str, NGCModel]:
        with open(PRIVATE_REGISTRY_CACHE_FILE, "r") as f:
            cache_json = json.load(f)
        cache = {
            file_hash: NGCModel(
                org=entry["org"], team=entry["team"], model_name=entry["model_name"], version=entry["version"]
            )
            for file_hash, entry in cache_json.items()
        }
        return cache

    def write(self, cache: Dict[str, NGCModel]):
        cache_json = {
            file_hash: dataclasses.asdict(entry)
            for file_hash, entry in cache.items()  # noqa
        }
        with open(PRIVATE_REGISTRY_CACHE_FILE, "w") as f:
            json.dump(cache_json, f, indent=4)

    def clear(self):
        self.write({})

    def upload_path(self, filepath_to_upload: str) -> str:
        """
        Uploads a local file or directory to NGC and returns the NGC model target.

        If the file or directory was already uploaded, the existing NGC model target is returned.
        """
        import ngcsdk
        from ngcbase.errors import ResourceAlreadyExistsException

        logging.info("Local model was provided. Checking NGC upload cache for existing model...")
        config = TRTCloudConfig()
        ngc_client = ngcsdk.Client()
        org, team = config.read_ngc_info()
        nvapi_key = config.read_saved_login()

        team_display = "None (default)" if team == "" else team
        logging.info(f"Configuring NGC client with org: {org}, team: {team_display}")
        # NGC SDK does not understand that `team_name=""` or `team_name=None` should correspond to
        # "no-team".
        team_name = team if team else "no-team"
        ngc_client.configure(org_name=org, team_name=team_name, api_key=nvapi_key)
        logging.info("NGC client configured successfully.")

        logging.info(f"Computing hash of local path '{filepath_to_upload}' for cache lookup...")
        hash = self.path_hash(filepath_to_upload)
        cache = self.read()

        # The file or directory was already uploaded.
        if hash in cache:
            ngc_model = cache[hash]
            # Double-check that the NGC model still exists.
            try:
                ngc_client.registry.model.get_version(
                    org_name=ngc_model.org,
                    team_name=ngc_model.team,
                    model_name=ngc_model.model_name,
                    version=ngc_model.version,
                )

                logging.info(f"Reusing uploaded NGC model with target '{ngc_model.target}'")
                return ngc_model.target
            except Exception:
                logging.info(f"NGC model with target '{ngc_model.target}' does not exist. Uploading new model.")
                del cache[hash]
                self.write(cache)

        created_model = False
        while not created_model:
            # There is a very small chance of short UUID collision, hence the while loop.
            short_uuid = str(uuid.uuid4())[:8]
            model_name = f"local-model-{short_uuid}"
            ngc_model = NGCModel(org=org, team=team, model_name=model_name, version="1.0")

            logging.info(f"Creating NGC Model '{model_name}' in Private Registry")
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                ngc_client.registry.model.create(
                    target=ngc_model.target_without_version,
                    application="CONTENT_GENERATION",
                    framework="unknown_framework",
                    model_format="unknown_format",
                    precision="ALL",
                    short_description=f"This model was uploaded from a local file using TensorRT Cloud at {now}",
                )
                created_model = True
            except ResourceAlreadyExistsException:
                logging.warning(f"NGC Model '{model_name}' already exists. Creating a new model.")

        logging.info(f"Uploading local path '{filepath_to_upload}' to NGC Model '{model_name}'")
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("Upload progress:")

            def progress_callback_func(
                completed_bytes,
                failed_bytes,
                total_bytes,
                completed_count,
                failed_count,
                total_count,
            ):
                progress.update(task, completed=completed_bytes, total=total_bytes)

            upload_result = ngc_client.registry.model.upload_version(
                target=ngc_model.target,
                source=filepath_to_upload,
                progress_callback_func=progress_callback_func,
            )
            upload_status = upload_result[1]

        if upload_status == "Completed":
            logging.info(f"Successfully uploaded NGC Model '{model_name}'")
        else:
            # Clean up if the upload failed.
            try:
                logging.info(f"Attempting to remove NGC Model '{model_name}'")
                ngc_client.registry.model.remove(ngc_model.target_without_version)
                logging.info(f"Successfully removed NGC Model '{model_name}'")
            except Exception as e:
                logging.error(f"Failed to remove NGC Model '{model_name}': {e}")

            raise RuntimeError(f"Failed to upload NGC Model '{model_name}' because upload status is {upload_status}.")

        # Save model to cache.
        cache[hash] = ngc_model
        self.write(cache)
        return ngc_model.target
