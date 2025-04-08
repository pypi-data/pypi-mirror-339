# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import logging
from typing import Optional, Callable, List

from trt_cloud import utils, rest_endpoints
from trt_cloud.sweeper import SweeperClient, WorkloadType

MAX_NUM_TAGS = 10
MAX_TAG_LENGTH = 128


def validate_tags(tags: List[str]) -> List[str]:
    if (num_tags := len(tags)) > MAX_NUM_TAGS:
        raise ValueError(f"Number of tags ({num_tags}) exceeds the maximum of {MAX_NUM_TAGS}.")
    for idx, tag in enumerate(tags):
        if (tag_length := len(tag)) > MAX_TAG_LENGTH:
            raise ValueError(f"{idx}-th tag length ({tag_length}) exceeds the maximum of {MAX_TAG_LENGTH}.")
    return tags


def run_list_common(
    client: SweeperClient,
    user_mode: bool = False,
    since: Optional[str] = None,
    until: Optional[str] = None,
    limit: Optional[int] = None,
    verbose: bool = False,
    default_limit: int = 25,
    workload_type: Optional[WorkloadType] = None,
    id_column_name: str = "Sweep ID",
    show_trials_column: bool = True,
    additional_validation_fn: Optional[Callable] = None,
) -> None:
    """
    Common function for listing items (sweeps or builds) in the TensorRT Cloud.

    Args:
        client: The TensorRT Cloud Sweeper client.
        user_mode: If True, filter by the current user.
        since: Start timestamp for filtering items.
        until: End timestamp for filtering items.
        limit: Maximum number of items to display.
        verbose: If True, don't truncate tags.
        default_limit: Default number of items to display if limit is not provided.
        workload_type: Type of workload to filter by (e.g., WorkloadType.SINGLE_ENGINE for builds).
        id_column_name: Name of the ID column in the table output.
        show_trials_column: If True, include the "Total Trials" column in the output.
        additional_validation_fn: Optional function to perform additional validation on inputs.
    """
    if additional_validation_fn:
        additional_validation_fn()

    if until and not since:
        raise ValueError("Must provide --since with --until")

    if since and limit:
        raise ValueError("--limit can not be used with --since/--until")

    if limit is None:
        limit = default_limit  # set default if not provided

    if limit < 1:
        raise ValueError("Limit must be greater than 0")

    _, ngc_org_id, ngc_team_id = rest_endpoints.get_creds(client.config)
    logging.info(
        f"List Running for org {ngc_org_id}, team {ngc_team_id or 'no-team'}" + (", current user" if user_mode else "")
    )

    items_list = client.get_list(
        user_mode=user_mode,
        since=since,
        until=until,
        workload_type=workload_type,
    )

    # Define columns for table
    columns = [
        id_column_name,
        "Status",
    ]

    if show_trials_column:
        columns.append("Total Trials")

    columns.extend(
        [
            "Start",
            "Duration",
            "Tags",
        ]
    )

    # Formatting
    max_tags_length = 30
    formatters = {
        # List tags one per line, truncated
        "Tags": lambda tags: f"\n".join(
            utils.truncate_string(tag, max_tags_length) if not verbose else tag for tag in tags
        ),
    }

    table_data = [columns]

    # Apply limit to results
    display_limit = len(items_list) if since or until else min(limit, len(items_list))
    for item in items_list[:display_limit]:
        table_data.append(
            [
                # No data
                ""
                if not item.get(col, "")
                # Formatted data
                else formatters[col](item[col])
                if col in formatters
                # Raw data
                else item[col]
                for col in columns
            ]
        )

    table_output = utils.tabulate(
        table_data,
        headers="firstrow",
    )

    if since and until:
        message = f"Showing items from {since} to {until}"
    elif since:
        message = f"Showing items since {since}"
    else:
        message = (
            f"Showing {display_limit} most recent items. Use --limit or --since/--until to change default behavior."
        )

    logging.info(f"{message}\n{table_output}")
