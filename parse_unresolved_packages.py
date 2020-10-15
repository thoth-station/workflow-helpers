#!/usr/bin/env python3
# workflow-helpers
# Copyright(C) 2020 Kevin Postlethwait
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


import sys
import logging
import json
import os

from typing import Dict, Any, Tuple, Optional
from pathlib import Path
from thoth.python import Pipfile
from thoth.common import OpenShift

from thoth.workflow_helpers import __service_version__

_LOGGER = logging.getLogger("thoth.parse_unresolved_packages")
_LOGGER.info("Thoth workflow-helpers task: parse_unresolved_packages v%s", __service_version__)

__COMPONENT_NAME__ = "adviser"

def parse_unresolved_packages(file_test_path: Optional[Path] = None) -> Tuple[Dict[Any, Any], Optional[str]]:
    """Investigate on unresolved packages."""
    if file_test_path:
        _LOGGER.debug("Dry run..")
        adviser_run_path = file_test_path
    else:
        adviser_run_path = Path(os.environ["FILE_PATH"])

    if not adviser_run_path.exists():
        raise FileNotFoundError(f"Cannot find the file on this path: {adviser_run_path}")

    with open(adviser_run_path, "r") as f:
        content = json.load(f)

    unresolved_packages = []
    report = content["result"]["report"]
    if report:
        errors_details = report.get("_ERROR_DETAILS")
        if errors_details:
            unresolved_packages = errors_details["unresolved"]

    if not unresolved_packages:
        _LOGGER.warning("No packages to be solved with priority identified.")
        sys.exit(2)

    parameters = content["result"]["parameters"]
    runtime_environment = parameters["project"].get("runtime_environment")

    solver = OpenShift.obtain_solver_from_runtime_environment(runtime_environment=runtime_environment)

    requirements = parameters["project"].get("requirements")

    pipfile = Pipfile.from_dict(requirements)
    packages = pipfile.packages.packages
    dev_packages = pipfile.dev_packages.packages

    packages_to_solve = {}
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
            "solver": {"type": "int", "value": solver},
        }

        # We store the message to put in the output file here.
        output_messages.append(
            {"topic_name": "thoth.investigator.unresolved-package", "message_contents": message_input}
        )

    # Store message to file that need to be sent.
    with open(f"/mnt/workdir/messages_to_be_sent.json", "w") as json_file:
        json.dump(output_messages, json_file)

    if output_messages:
        _LOGGER.info(f"Successfully stored file with messages to be sent!: {output_messages}")



if __name__ == "__main__":
    parse_unresolved_packages()
