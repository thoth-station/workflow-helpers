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

from typing import List
from thoth.storages import GraphDatabase
from thoth.storages import AdvisersResultsStore
from thoth.storages.graph.enums import ThothAdviserIntegrationEnum

from thoth.workflow_helpers.common import retrieve_solver_document
from thoth.workflow_helpers.common import send_metrics, store_messages, parametrize_metric_messages_sent, set_metrics
from thoth.messaging.unresolved_package import AdviserReRunMessage
from thoth.workflow_helpers import __service_version__

GRAPH = GraphDatabase()
GRAPH.connect()

ADVISER_STORE = AdvisersResultsStore()
ADVISER_STORE.connect()

component_name = os.environ["THOTH_MESSAGING_COMPONENT_NAME"]
document_path = os.environ["THOTH_SOLVER_DOCUMENT_PATH"]

_LOGGER = logging.getLogger("thoth.parse_solver_output")
_LOGGER.info("Thoth workflow-helpers task: parse_solver_output v%s", __service_version__)

metric_messages_sent = parametrize_metric_messages_sent(
    component_name=component_name, description="Thoth Provenance Checker Workflow number messages sent"
)


def _check_unsolved_packages(
    unsolved_packages: List[str], package_name: str, package_version: str, index_url: str
) -> int:
    """Check unsolved packages to decide if adviser can be re run."""
    solved_counter = 0
    if package_name not in unsolved_packages:
        return solved_counter

    # current package name, version, index has been solved already!
    solved_counter += 1

    for package in unsolved_packages:
        # Check if all packages are solved (except just solved)
        if package != package_name:
            is_present = GRAPH.python_package_version_exists(
                package_name=package_name, package_version=package_version, index_url=index_url
            )
            if not is_present:
                return solved_counter

            solved_counter += 1

    return solved_counter


def parse_solver_output() -> None:
    """Parse solver output and produce inputs for Kafka message."""
    solver_name = os.environ["THOTH_SOLVER_NAME"]

    solver_document = retrieve_solver_document(document_path)
    service_version = solver_document["metadata"]["analyzer_version"]

    # 1. Retrieve adviser ids for specific thoth_integrations with need_re_run == True
    source_type = ThothAdviserIntegrationEnum.GITHUB_APP.name
    unsolved_per_adviser_runs = GRAPH.get_unsolved_python_packages_all_per_adviser_run(source_type=source_type)

    output_messages = []

    for python_package_info in solver_document["result"]["tree"]:
        package_name = python_package_info["package_name"]
        package_version = python_package_info["package_version_requested"]
        index_url = python_package_info["index_url"]

        message_input = {
            "component_name": {"type": "str", "value": component_name},
            "service_version": {"type": "str", "value": service_version},
            "package_name": {"type": "str", "value": package_name},
            "package_version": {"type": "str", "value": package_version},
            "index_url": {"type": "str", "value": index_url},
            "solver": {"type": "str", "value": solver_name},
        }

        output_messages.append({"topic_name": "thoth.solver.solved-package", "message_contents": message_input})

        for adviser_id in unsolved_per_adviser_runs:

            unsolved_packages = unsolved_per_adviser_runs[adviser_id]

            # 2. Check if all packages have been solved
            number_packages_solved = _check_unsolved_packages(
                unsolved_packages=unsolved_packages,
                package_name=package_name,
                package_version=package_version,
                index_url=index_url,
            )

            if number_packages_solved >= len(unsolved_packages):
                _LOGGER.info("All packages have been solved! Adviser can re run.")

                # 3. Retrieve adviser inputs to re run from adviser id
                document = ADVISER_STORE.retrieve_document(adviser_id)
                parameters = document["result"]["parameters"]
                cli_inputs = document["metadata"]["arguments"]
                cli_arguments = document["metadata"]["arguments"]["thoth-adviser"]

                application_stack = {
                    "requirements": cli_inputs["requirements"],
                    "requirements_lock": cli_inputs["requirements_lock"],
                    "requirements_format": cli_inputs["requirements_format"],
                }

                recommendation_type = parameters["recommendation_type"]
                runtime_environment = parameters["project"].get("runtime_environment")

                origin = cli_arguments["metadata"]["origin"]
                github_event_type = cli_arguments["metadata"]["github_event_type"]
                github_check_run_id = cli_arguments["metadata"]["github_event_type"]
                github_installation_id = cli_arguments["metadata"]["github_event_type"]
                github_base_repo_url = cli_arguments["metadata"]["github_event_type"]

                source_type = (cli_arguments.get("metadata") or {}).get("source_type")
                source_type = source_type.upper() if source_type else None

                # 4. Save adviser_id_message inputs
                message_input = {
                    "component_name": {"type": "str", "value": component_name},
                    "service_version": {"type": "str", "value": service_version},
                    "re_run_adviser_id": {"type": "str", "value": adviser_id},
                    "application_stack": {"type": "Dict[Any, Any]", "value": application_stack},
                    "recommendation_type": {"type": "str", "value": recommendation_type},
                    "runtime_environment": {"type": "Optional[Dict[Any, Any]]", "value": runtime_environment},
                    "origin": {"type": "Optional[str]", "value": origin},
                    "github_event_type": {"type": "Optional[str]", "value": github_event_type},
                    "github_check_run_id": {"type": "Optional[str]", "value": github_check_run_id},
                    "github_installation_id": {"type": "Optional[str]", "value": github_installation_id},
                    "github_base_repo_url": {"type": "Optional[str]", "value": github_base_repo_url},
                    "source_type": {"type": "Optional[str]", "value": source_type},
                }

                output_messages.append({"topic_name": AdviserReRunMessage.base_name, "message_contents": message_input})

    # 5. Store messages that need to be sent
    store_messages(output_messages)

    set_metrics(
        metric_messages_sent=metric_messages_sent,
        message_type=AdviserReRunMessage.base_name,
        service_version=__service_version__,
        number_messages_sent=len(output_messages),
    )

    send_metrics()


if __name__ == "__main__":
    parse_solver_output()
