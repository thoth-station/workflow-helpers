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

"""This script run in a workflow task to parse solver inputs and produce inputs for Kafka message."""

import os
import logging
import json

from thoth.workflow_helpers.common import retrieve_solver_service_version
from thoth.workflow_helpers import __service_version__

component_name = os.environ["THOTH_MESSAGING_COMPONENT_NAME"]
document_path = os.environ["THOTH_SOLVER_DOCUMENT_PATH"]

_LOGGER = logging.getLogger("thoth.parse_solver_inputs")
_LOGGER.info("Thoth workflow-helpers task: parse_solver_inputs v%s", __service_version__)


def parse_solver_inputs() -> None:
    """Parse solver inputs and produce inputs for Kafka message."""
    solver_name = os.environ["THOTH_SOLVER_NAME"]
    package = os.environ["THOTH_SOLVER_PACKAGES"]

    package_inputs = package.split("===")

    solver_indexes = os.environ["THOTH_SOLVER_INDEXES"]
    indexes = solver_indexes.split(",")

    service_version = retrieve_solver_service_version(document_path)

    output_messages = []

    for index_url in indexes:

        message_input = {
            "component_name": {"type": "str", "value": component_name},
            "service_version": {"type": "str", "value": service_version},
            "package_name": {"type": "str", "value": package_inputs[0]},
            "package_version": {"type": "str", "value": package_inputs[1]},
            "index_url": {"type": "str", "value": index_url},
            "solver": {"type": "str", "value": solver_name},
        }

        output_messages.append({"topic_name": "thoth.solver.solved-package", "message_contents": message_input})

    if output_messages:
        with open(f"/mnt/workdir/solved_messages.json", "w") as json_file:
            json.dump(output_messages, json_file)


if __name__ == "__main__":
    parse_solver_inputs()
