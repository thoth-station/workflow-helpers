#!/usr/bin/env python3
# workflow-helpers
# Copyright(C) 2020 Francesco Murdaca, Bissenbay Dauletbayev
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

"""This script run in a workflow task to parse solver output and produce inputs for Kafka message."""

import os
import logging
import json

from thoth.workflow_helpers.common import retrieve_solver_document
from thoth.workflow_helpers import __service_version__

component_name = os.environ["THOTH_MESSAGING_COMPONENT_NAME"]
document_path = os.environ["THOTH_SOLVER_DOCUMENT_PATH"]

_LOGGER = logging.getLogger("thoth.parse_solver_output")
_LOGGER.info("Thoth workflow-helpers task: parse_solver_output v%s", __service_version__)


def parse_solver_output() -> None:
    """Parse solver output and produce inputs for Kafka message."""
    solver_name = os.environ["THOTH_SOLVER_NAME"]

    solver_document = retrieve_solver_document(document_path)
    service_version = solver_document["metadata"]["analyzer_version"]

    output_messages = []

    for python_package_info in solver_document["result"]["tree"]:
        message_input = {
            "component_name": {"type": "str", "value": component_name},
            "service_version": {"type": "str", "value": service_version},
            "package_name": {"type": "str", "value": python_package_info["package_name"]},
            "package_version": {"type": "str", "value": python_package_info["package_version_requested"]},
            "index_url": {"type": "str", "value": python_package_info["index_url"]},
            "solver": {"type": "str", "value": solver_name},
        }

        output_messages.append({"topic_name": "thoth.solver.solved-package", "message_contents": message_input})

    with open(f"/mnt/workdir/messages_to_be_sent.json", "w") as json_file:
        json.dump(output_messages, json_file)

    if output_messages:
        _LOGGER.info(f"Successfully stored file with solved messages!: {output_messages}")


if __name__ == "__main__":
    parse_solver_output()
