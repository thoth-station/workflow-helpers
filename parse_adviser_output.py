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

"""This script run in a workflow task to parse adviser output."""


import logging
import json
import os

from pathlib import Path
from thoth.python import Pipfile
from thoth.common import OpenShift

from thoth.workflow_helpers import __service_version__

from thoth.workflow_helpers.common import send_metrics, store_messages, parametrize_metric_messages_sent, set_metrics
from thoth.messaging.unresolved_package import UnresolvedPackageMessage

_LOGGER = logging.getLogger("thoth.parse_adviser_output")
_LOGGER.info("Thoth workflow-helpers task: parse_adviser_output v%s", __service_version__)

__COMPONENT_NAME__ = "adviser"

metric_messages_sent = parametrize_metric_messages_sent(
    component_name=__COMPONENT_NAME__, description="Thoth Adviser Workflow number messages sent"
)


def parse_adviser_output() -> None:
    """Investigate on unresolved packages in adviser output."""
    adviser_run_path = Path(os.environ["FILE_PATH"])

    file_found = True
    unresolved_found = True

    unresolved_packages = []
    packages_to_solve = {}

    if not adviser_run_path.exists():
        _LOGGER.warning(f"Cannot find the file on this path: {adviser_run_path}")
        file_found = False

    if file_found:

        with open(adviser_run_path, "r") as f:
            content = json.load(f)

        report = content["result"]["report"]

        if report:
            errors_details = report.get("_ERROR_DETAILS")
            if errors_details:
                unresolved_packages = errors_details["unresolved"]

        if not unresolved_packages:
            _LOGGER.warning("No packages to be solved with priority identified.")
            unresolved_found = False

        if unresolved_found:
            _LOGGER.info(f"Identified the following unresolved packages: {unresolved_packages}")

            parameters = content["result"]["parameters"]
            runtime_environment = parameters["project"].get("runtime_environment")

            solver = OpenShift.obtain_solver_from_runtime_environment(runtime_environment=runtime_environment)

            requirements = parameters["project"].get("requirements")

            pipfile = Pipfile.from_dict(requirements)
            packages = pipfile.packages.packages
            dev_packages = pipfile.dev_packages.packages

            for package_name in unresolved_packages:

                if package_name in packages:
                    packages_to_solve[package_name] = packages[package_name]

                if package_name in dev_packages:
                    packages_to_solve[package_name] = dev_packages[package_name]

            _LOGGER.info(f"Unresolved packages identified.. {packages_to_solve}")

    output_messages = []

    for package, package_info in packages_to_solve.items():

        message_input = {
            "component_name": {"type": "str", "value": __COMPONENT_NAME__},
            "service_version": {"type": "str", "value": __service_version__},
            "package_name": {"type": "Dict", "value": package_info.name},
            "package_version": {"type": "str", "value": package_info.version},
            "index_url": {"type": "str", "value": package_info.index},
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
    parse_adviser_output()
