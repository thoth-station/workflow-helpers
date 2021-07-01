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

from typing import List, Optional
from thoth.storages import GraphDatabase
from thoth.storages import AdvisersResultsStore
from thoth.common import OpenShift
from thoth.common.enums import ThothAdviserIntegrationEnum

from thoth.workflow_helpers.common import retrieve_solver_document
from thoth.workflow_helpers.common import send_metrics, store_messages, parametrize_metric_messages_sent, set_metrics
from thoth.messaging import solved_package_message, adviser_trigger_message
from thoth.messaging.solved_package import MessageContents as SolvedPackageContents
from thoth.messaging.adviser_trigger import MessageContents as AdviserTriggerContents
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
    source_type: Optional[str]
    source_type = ThothAdviserIntegrationEnum.KEBECHET.name
    unsolved_per_adviser_runs = GRAPH.get_unsolved_python_packages_all_per_adviser_run(source_type=source_type)

    output_messages = []
    solver_messages_count = 0
    adviser_messages_count = 0

    for python_package_info in solver_document["result"]["tree"]:
        package_name = python_package_info["package_name"]
        package_version = python_package_info["package_version_requested"]
        index_url = python_package_info["index_url"]

        messgae_input = SolvedPackageContents(
            component_name=component_name,
            service_version=service_version,
            index_url=index_url,
            package_name=package_name,
            package_version=package_version,
            solver=solver_name,
        ).dict()

        output_messages.append({"topic_name": solved_package_message.base_name, "message_contents": messgae_input})

        solver_messages_count += 1

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

                # 3. Retrieve adviser inputs to create a new request and schedule adviser with thamos

                retrieved_parameters = True
                try:
                    parameters = ADVISER_STORE.retrieve_request(adviser_id)
                except Exception as retrieve_error:
                    _LOGGER.error(
                        f"Failed to retrieve parameters for request with adviser id: {adviser_id}: {retrieve_error}"
                    )
                    retrieved_parameters = False

                parameters.pop("job_id")

                new_adviser_id = OpenShift.generate_id("adviser")
                parameters["job_id"] = new_adviser_id

                ADVISER_STORE.store_request(parameters["job_id"], parameters)

                if retrieved_parameters:

                    try:
                        message_input = AdviserTriggerContents(
                            job_id=new_adviser_id,
                            component_name=component_name,
                            service_version=__service_version__,
                            authenticated=True,
                            github_event_type=parameters["github_event_type"],
                            github_check_run_id=parameters["github_check_run_id"],
                            github_installation_id=parameters["github_installation_id"],
                            github_base_repo_url=parameters["github_base_repo_url"],
                            origin=parameters["origin"],
                            recommendation_type=parameters["recommendation_type"],
                            re_run_adviser_id=adviser_id,
                            source_type=parameters["source_type"],
                            count=parameters["count"],
                            debug=parameters["debug"],
                            dev=parameters["dev"],
                            limit=parameters["limit"],
                        ).dict()

                        output_messages.append(
                            {"topic_name": adviser_trigger_message.base_name, "message_contents": message_input}
                        )

                        adviser_messages_count += 1

                    except Exception as message_error:
                        _LOGGER.error(
                            f"Failed creating message for adviser trigger using parameters: {parameters}"
                            f" from adviser id {adviser_id}: {message_error}"
                        )

    # 5. Store messages that need to be sent
    store_messages(output_messages)

    set_metrics(
        metric_messages_sent=metric_messages_sent,
        message_type=adviser_trigger_message.base_name,
        service_version=__service_version__,
        number_messages_sent=adviser_messages_count,
    )

    set_metrics(
        metric_messages_sent=metric_messages_sent,
        message_type=solved_package_message.base_name,
        service_version=__service_version__,
        number_messages_sent=solver_messages_count,
    )

    send_metrics()


if __name__ == "__main__":
    parse_solver_output()
