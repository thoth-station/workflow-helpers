#!/usr/bin/env python3
# workflow-helpers
# Copyright(C) 2020 Francesco Murdaca
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""This script run in a workflow task to parse provenance checker output."""


import logging
import json
import os

from typing import List, Any, Dict
from pathlib import Path

from thoth.workflow_helpers import __service_version__

from thoth.workflow_helpers.common import store_messages

from thoth.workflow_helpers.common import send_metrics, parametrize_metric_messages_sent, set_metrics
from thoth.messaging.unresolved_package import UnresolvedPackageMessage

_LOGGER = logging.getLogger("thoth.parse_provenance_checker_output")
_LOGGER.info("Thoth workflow-helpers task: parse_provenance_checker_output v%s", __service_version__)

__COMPONENT_NAME__ = "provenance-checker"

metric_messages_sent = parametrize_metric_messages_sent(
    component_name=__COMPONENT_NAME__, description="Thoth Provenance Checker Workflow number messages sent"
)


def _parse_provenance_check_report(report: List[Any]) -> List[Dict[str, str]]:
    """Retrieve unsolved packages from provenance checker run."""
    package_id = "MISSING-PACKAGE"

    unresolved_packages = []

    for package in report:
        if package["id"] == package_id:
            unresolved_packages.append(
                {
                    "package_name": package["package_name"],
                    "package_version": package["package_version"].lstrip("=="),
                    "index_url": package["source"]["url"],
                }
            )

    return unresolved_packages


def parse_provenance_checker_output() -> None:
    """Investigate on unresolved packages in provenance-checker output."""
    provenance_checker_run_path = Path(os.environ["FILE_PATH"])

    file_found = True

    unresolved_packages = []

    if not provenance_checker_run_path.exists():
        _LOGGER.warning(f"Cannot find the file on this path: {provenance_checker_run_path}")
        file_found = False

    if file_found:

        with open(provenance_checker_run_path, "r") as f:
            content = json.load(f)

        report = content["result"]["report"]

        if report:
            unresolved_packages = _parse_provenance_check_report(report=report)
        else:
            _LOGGER.warning("Report in the document is empty.")

        if not unresolved_packages:
            _LOGGER.warning("No packages to be solved with priority identified.")

        else:
            _LOGGER.info(f"Identified the following unresolved packages: {unresolved_packages}")

    solver = None  # No solver: all available solvers will be scheduled for unsolved package
    output_messages = []

    for package in unresolved_packages:

        message_input = {
            "component_name": {"type": "str", "value": __COMPONENT_NAME__},
            "service_version": {"type": "str", "value": __service_version__},
            "package_name": {"type": "Dict", "value": package["package_name"]},
            "package_version": {"type": "str", "value": package["package_version"]},
            "index_url": {"type": "str", "value": package["index_url"]},
            "solver": {"type": "str", "value": solver},
        }

        # We store the message to put in the output file here.
        output_messages.append({"topic_name": UnresolvedPackageMessage.base_name, "message_contents": message_input})

    # Store message to file that need to be sent.
    store_messages(output_messages)

    set_metrics(
        metric_messages_sent=metric_messages_sent,
        message_type=UnresolvedPackageMessage.base_name,
        service_version=__service_version__,
        number_messages_sent=len(output_messages),
        is_storages_used=False,
    )

    send_metrics()


if __name__ == "__main__":
    parse_provenance_checker_output()
