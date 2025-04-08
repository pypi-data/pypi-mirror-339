# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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
import sys
import zipfile
import textwrap
import time
from datetime import datetime, timezone
from decimal import Decimal
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union
import shutil
from pathlib import Path

from tabulate import tabulate as python_tabulate

import blessed
import requests
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

from trt_cloud.constants import TRTC_PREBUILT_ENGINE_ORG, TRTC_PREBUILT_ENGINE_TEAM
from trt_cloud.rest_endpoints import EndpointException
from trt_cloud.types import BuilderFunction

HEADING_PADDING = ": "
INDENTATION_PADDING = "    "

LEFT_BORDER = "│ "
RIGHT_BORDER = " │"
TOTAL_BORDER_WIDTH = len(LEFT_BORDER) + len(RIGHT_BORDER)


def download_file(
    url: str,
    output_filepath: str,
    headers: dict = None,
    quiet: bool = False,
) -> str:
    response = requests.get(url, allow_redirects=True, stream=True, headers=headers)
    if not response.ok:
        raise RuntimeError(f"Failed to download {url}", response)

    total_length = int(response.headers["Content-Length"])
    chunk_size = 2**20  # 1MB

    # Create a Progress bar
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        disable=quiet,
    ) as progress:
        # Create a Task object to represent the progress of the download
        task = progress.add_task(f"Downloading to {os.path.basename(output_filepath)}", total=total_length)

        with open(output_filepath, "wb") as output:
            for content in response.iter_content(chunk_size):
                if content:
                    output.write(content)
                    progress.update(task, advance=len(content))

    return output_filepath


def check_and_display_eula(
    license_path: str,
    eula_name: str,
    license_preamble: str = "",
    license_path_format_string="Please find a copy of the license here: {}.",
) -> bool:
    if os.path.exists(license_path):
        with open(license_path, "r", encoding="utf8") as f:
            license_text = f.read()
    else:
        raise ValueError(f"{eula_name} not found. Must agree to EULA to proceed.")
    print(f"\n{eula_name}\n{license_preamble}{license_text}\n{license_path_format_string.format(license_path)}\n")
    user_input = input(f"Do you agree to the {eula_name}? (yes/no) ").lower().strip()

    user_agreed = user_input in {"y", "yes"}
    if not user_agreed:
        raise ValueError(f"You must agree to the {eula_name} to proceed.")

    return user_agreed


def upload_file(
    url: str,
    filepath: str,
    headers: dict = None,
):
    total_length = os.stat(filepath).st_size
    chunk_size = 2**20  # 1MB

    class ReadFileWithProgressBar(object):
        def __init__(self, filepath):
            self.file = open(filepath, "rb")
            self.total_length = os.stat(filepath).st_size
            self.progress = Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TaskProgressColumn(),
                TimeRemainingColumn(),
            )
            self.progress.start()
            self.task = self.progress.add_task(f"Uploading {filepath}", total=self.total_length)

        def read(self, size=chunk_size):
            chunk = self.file.read(size)
            self.progress.update(self.task, advance=len(chunk))
            if len(chunk) == 0:
                self.progress.stop()
                self.file.close()
            return chunk

        def __len__(self):
            return total_length

    resp = requests.put(
        url,
        data=ReadFileWithProgressBar(filepath),
        headers=headers,
    )
    return resp


def extract_onnx_file(tmpdir, onnx_zip) -> str:
    with zipfile.ZipFile(onnx_zip, "r") as zip:
        zip.extractall(tmpdir)
    onnx_files_in_zip = list(Path(tmpdir).rglob("*.onnx"))
    if not onnx_files_in_zip:
        raise ValueError(f"No .onnx files found in {onnx_zip}.")
    if len(onnx_files_in_zip) > 1:
        raise ValueError(f"Multiple .onnx files found in archive: {onnx_files_in_zip}")
    return str(onnx_files_in_zip[0])


def find_dir_with_file(root_dir, filename):
    dirs: List[str] = list()
    for root, _, files in os.walk(root_dir):
        if filename in files:
            dirs.append(root)
    if len(dirs) == 0:
        raise FileNotFoundError(f"Cannot find {filename} in input dir.")
    if len(dirs) > 1:
        raise FileNotFoundError(f"Found multiple files named {filename} in input dir.")
    return dirs[0]


def add_verbose_flag_to_parser(parser):
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase logging verbosity.")


@lru_cache()
def get_ngc_model_org():
    return os.environ.get("TRTC_ENGINE_ORG", "") or TRTC_PREBUILT_ENGINE_ORG


@lru_cache()
def get_ngc_model_team():
    return os.environ.get("TRTC_ENGINE_TEAM", None) or TRTC_PREBUILT_ENGINE_TEAM


class PrintMessageOnCtrlC:
    """
    Context manager which prints a message if it receives a KeyboardInterrupt.
    """

    def __init__(self, msg, level=logging.INFO):
        self.msg = msg
        self.level = level

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is KeyboardInterrupt:
            logging.log(self.level, self.msg)


class PrintNewlineOnExit:
    """
    Context manager which prints a new line on exit.
    Useful for printing the missing newline after "Latest poll status".
    """

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        print("")


class Display:
    class DummyTerminal:
        # Use when the terminal is not available
        width = 100

        def move_x(self, x):
            return ""

        def move_up(self, x):
            return ""

        def clear_eol(self):
            return ""

        def clear_eos(self):
            return ""

        def bold(self, x):
            return x

    def __init__(self):
        if sys.stdout.isatty():
            self.term = blessed.Terminal()
        else:
            # Terminal is not available.
            self.term = Display.DummyTerminal()

        self.num_lines = 1
        self.width = self.term.width - 4
        print()

    def print(self, text, heading="", truncate=True):
        # We split the text into lines and print each line separately. Otherwise, the text could
        # contain multiple lines and the message end up looking unreadable.
        lines = text.splitlines()
        TOTAL_HEADING_PADDING = len(heading) + len(HEADING_PADDING)
        # If there's a heading present then the subsequent lines printed will have
        # an indentation. This makes the output text easier to read.
        indentation = INDENTATION_PADDING if heading != "" else ""

        for idx, line in enumerate(lines):
            split_lines = (
                [line]
                if truncate is True
                else textwrap.wrap(line, self.width - (TOTAL_HEADING_PADDING + TOTAL_BORDER_WIDTH))
            )
            for inner_idx, split_line in enumerate(split_lines):
                if idx > 0 or inner_idx > 0:
                    split_line = indentation + split_line
                split_line = self._get_line_to_print(split_line, heading=heading)
                print(split_line)
                self.num_lines += 1
                # Heading is only necessary on the first line printed.
                heading = ""

    def _print_bar(self, start, middle, end):
        print(self.term.move_x(0) + self.term.clear_eol() + start + middle * self.width + end)
        self.num_lines += 1

    def print_top_bar(self):
        self._print_bar("┌", "─", "┐")

    def print_middle_bar(self):
        self._print_bar("├", "─", "┤")

    def print_bottom_bar(self):
        self._print_bar("└", "─", "┘")

    def reset(self):
        print(self.term.move_up(self.num_lines) + self.term.clear_eos())
        self.num_lines = 1
        self.width = self.term.width - 4

    def _get_line_to_print(self, line, heading=""):
        heading = heading + HEADING_PADDING if heading != "" else ""
        msg_len = len(line) + len(heading) + TOTAL_BORDER_WIDTH

        # Shorten long messages so they fit into one line.
        if msg_len > self.width:
            # Available width equals the total display width minus
            # the heading, padding, and borders.
            half = (self.width - (len(heading) + TOTAL_BORDER_WIDTH)) // 2
            line = f"{line[:half]}...{line[-half:]}"

        # Pad messages so they are exactly 'width' long
        msg_len = len(line) + len(heading) + 2
        line += " " * max(0, self.width - msg_len)

        to_print = self.term.move_x(0) + self.term.clear_eol() + LEFT_BORDER
        if heading:
            to_print += self.term.bold(heading)

        to_print += line
        to_print += RIGHT_BORDER

        return to_print


def get_status_message_response(status, status_message, timestamp, end_timestamp):
    elapsed_time = ((end_timestamp if status == "DONE" else datetime.now(timezone.utc)) - timestamp).total_seconds()
    minutes, seconds = divmod(elapsed_time, 60)
    formatted_time_duration = f"{int(minutes)} min {int(seconds)} sec"

    if status == "PENDING":
        result = f"Pending - {formatted_time_duration}"
        if status_message:
            result += f" - {status_message}"
        return result
    elif status == "QUEUED":
        result = f"Queued - {formatted_time_duration}"
        if status_message:
            result += f" - {status_message}"
        return result
    elif status == "IN_PROGRESS":
        result = f"In Progress - {formatted_time_duration}"
        if status_message:
            result += f" - {status_message}"
        return result
    elif status == "DONE":
        return f"Completed - {formatted_time_duration}"
    elif status == "CANCELLED":
        return "Cancelled"
    elif status == "ERROR":
        return f"Error - {status_message}"


def format_time_string(seconds):
    """
    Formats a duration in seconds into a SLURM-like time format (HH:MM:SS or MM:SS)

    Parameters:
    seconds (int): The duration in seconds.

    Returns:
    str: The formatted time as a string.
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    if hours > 0:
        return f"{hours}:{minutes:02}:{secs:02}"
    else:
        return f"{minutes:02}:{secs:02}"


def calculate_duration(start: Decimal, end: Decimal, format_string=False) -> str:
    """
    Computes duration between two timestamps from the database.
    If `start` time is negative, returns 0.
    If `end` time is negative, uses current time as end time.
    If `format_string` is True, the duration is formatted as HH:MM:SS.
    If `format_string` is False, the duration is formatted as minutes rounded to one decimal place.
    """
    int_start = int(start)
    if int_start < 0:
        return "0"
    start_time = datetime.fromtimestamp(int_start, tz=timezone.utc)
    int_end = int(end)
    if int_end < 0:
        end_time = datetime.now(tz=timezone.utc)
    else:
        end_time = datetime.fromtimestamp(int_end, tz=timezone.utc)
    diff_seconds = (end_time - start_time).total_seconds()
    if format_string:
        diff_str = format_time_string(int(diff_seconds))
    else:
        diff_minutes = diff_seconds / 60.0
        diff_str = f"{diff_minutes:.1f}"
    return diff_str


def convert_str_to_int_timestamp(str_timestamp: str) -> datetime:
    return datetime.strptime(str_timestamp, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)


def convert_int_to_str_timestamp(timestamp: datetime) -> str:
    if timestamp == -1:
        return "-1"
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def get_build_info(
    engine_build_rows: List[Dict[str, Any]],
    trial_id: Union[str, None] = None,
):
    # Get information about separate build(s) for a given sweep_id and trial_id:
    # 1) if only |engine_build_rows| is specified (containing all the trials for some sweep_id):
    #       send back a list of builds that look as following:
    #       [{"id": 0, "status": "Buidling|Completed", "duration": 1.5}]
    # 2) if |trial_id| is specified as well:
    #       send back a list consisting of a single build that also includes its |status_message|:
    #       [{"id": 0, "status": "Buidling|Completed", "duration": 1.5,
    #         "status_message": "Error! Received no response"}]
    builds = []
    try:
        # iterate over raw rows, filling the |builds| list
        for engine_build_row in engine_build_rows:
            # calculate duration
            timestamp = convert_str_to_int_timestamp(engine_build_row["timestamp"])
            end_timestamp = convert_str_to_int_timestamp(engine_build_row["end_timestamp"])
            duration_mins = calculate_duration(int(timestamp.timestamp()), int(end_timestamp.timestamp()))
            build_info = {
                "id": engine_build_row.get("id", "-1"),
                "status": engine_build_row.get("status", "ERROR"),
                "duration": duration_mins,
            }
            if trial_id:
                build_info["status_message"] = engine_build_row.get("status_message", "")
            builds.append(build_info)
        builds.sort(key=lambda x: int(x["id"]))
    except Exception as e:
        raise EndpointException(f"Failed to parse the sweep results: {e!s}")
    return builds


def truncate_string(input_string: str, max_length: int = 30) -> str:
    if not input_string:
        return ""
    ret = input_string[: min(len(input_string), max_length)]
    if len(input_string) > max_length:
        ret += "\u2026"
    return ret


def tabulate(*args, **kwargs):
    """
    Wrapper around python-tabulate with a consistent default tablefmt.

    Reference: https://github.com/astanin/python-tabulate/blob/master/README.md#table-format
    """
    # NOTE: most `tablefmt` break when using `\n` in the data; pretty does not.
    kwargs["tablefmt"] = kwargs.get("tablefmt") or "pretty"
    kwargs["stralign"] = kwargs.get("stralign", "left")
    return python_tabulate(*args, **kwargs)


def find_parameters_to_identify_function(
    needle: BuilderFunction, haystack: List[BuilderFunction], parameters: List[str]
) -> List[Tuple[str, str]]:
    """
    Find the combination of parameters that uniquely identify needle in haystack.
    """
    # Try to add --parameters one by one until we're able to uniquely identify a function
    combination_parameters = []
    last_len_find_items = 0
    for parameter_name in parameters:
        if not getattr(needle, parameter_name):
            continue

        parameter_values = getattr(needle, parameter_name)

        if not isinstance(parameter_values, (set, list)):
            parameter_values = [parameter_values]

        # For parameters that are lists, try every value
        found_combination = False
        for parameter_value in parameter_values:
            combination_parameters.append((parameter_name, parameter_value))

            # Check how many functions match the current combination of parameters
            len_find_items = len(
                [
                    f
                    for f in haystack
                    if all(
                        getattr(f, c_param_name) == c_param_value
                        if not isinstance(getattr(f, c_param_name), (set, list))
                        else c_param_value in getattr(f, c_param_name)
                        for c_param_name, c_param_value in combination_parameters
                    )
                ]
            )

            # Adding this parameter didn't change anything, so skip it and continue looking
            if last_len_find_items == len_find_items:
                combination_parameters.pop()
                continue

            # Found a unique combination of parameters, so stop here
            if len_find_items == 1:
                found_combination = True
                break

            # No unique combination of parameters found, so skip this parameter and continue looking
            elif len_find_items == 0:
                combination_parameters.pop()
                continue

            # Still too many combinations, continue looking
            last_len_find_items = len_find_items

        if found_combination:
            break
    else:
        pass

    return combination_parameters


def fix_broken_ngc_windows_directory_structure(base_dir):
    """
    Fixes a flat directory structure where paths are represented with backslashes
    into a proper hierarchical directory structure.

    This is a workaround for a bug in the NGC SDK where it incorrectly
    flattens the directory structure of uploaded build result on Windows.

    Args:
        base_dir: Path to the directory containing the flattened files
    """
    # Get all files in the directory
    files = [f for f in os.listdir(base_dir) if "\\" in f]

    for file_path in files:
        # Convert Windows path to proper path parts
        parts = file_path.split("\\")

        # Create the full directory path
        dir_path = os.path.join(base_dir, *parts[:-1])

        # Create directories if they don't exist
        os.makedirs(dir_path, exist_ok=True)

        # Source and destination paths
        src = os.path.join(base_dir, file_path)
        dst = os.path.join(base_dir, *parts)

        # Move the file to its proper location
        shutil.move(src, dst)
