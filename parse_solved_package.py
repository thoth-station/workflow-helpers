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

"""This script run in a workflow task to parse solved package and produce inputs for Kafka message."""

import os
import logging
import json

from thoth.storages import GraphDatabase

GRAPH = GraphDatabase()
GRAPH.connect()

ADVISER_STORE = AdvisersResultsStore()
ADVISER_STORE.connect()

_LOGGER = logging.getLogger("thoth.parse_solved_package")

def _check_unsolved_packages(unsolved_packages: List[str], package_name: str) -> int:
    """Check unsolved packages to decide if adviser can be re run."""
    solved_counter = 0
    if package_name not in unsolved_packages:
        return solved_counter

    solved_counter += 1

    for package in unsolved_packages:
        # Check if all packages are solved (except just solved)
        if package != package_name:
            is_present = GRAPH.python_package_version_exists(
                package_name=package_name, package_version=version, index_url=index_url
            )
            if not is_present:
                return solved_counter

            solved_counter += 1

    return solved_counter


def parse_solved_package():
    """Parse solver inputs and produce inputs for Kafka message."""
    solved_package = os.environ["THOTH_SOLVER_PACKAGES"]

    package_name = solved_package.split("===")[0]

    # 1. Retrieve adviser ids for specific thoth_integrations with need_re_run == True
    unsolved_per_adviser_runs = graph.get_unsolved_python_packages_all_per_adviser_run(
        source_type="github_app"
    )

    output_message_counter = 1

    for adviser_id in unsolved_per_adviser_runs:
        
        unsolved_packages = unsolved_per_adviser_runs[adviser_id]

        # 2. Check if all packages have been solved
        number_packages_solved = _check_unsolved_packages(
            unsolved_packages=,
            package_name=package_name
        )

        if number_packages_solved == len(unsolved_packages):
            _LOGGER.("All packages have been solved! Adviser can re run.")
            # 3. Retrieve adviser inputs to re run from adviser id
            document = ADVISER_STORE.retrieve_document(document_id)
            parameters = document["result"]["parameters"]
            cli_inputs = document["metadata"]["arguments"]
            cli_arguments = document["metadata"]["arguments"]["thoth-adviser"]

            application_stack={
                "requirements": cli_inputs["requirements"],
                "requirements_lock": cli_inputs["requirements_lock"],
                "requirements_format": cli_inputs["requirements_format"]
            }

            recommendation_type = parameters["recommendation_type"]
            runtime_environment = parameters["project"].get("runtime_environment")

            origin = cli_arguments['metadata']['origin']
            github_event_type = cli_arguments['metadata']['github_event_type']
            github_check_run_id = cli_arguments['metadata']['github_event_type']
            github_installation_id = cli_arguments['metadata']['github_event_type']
            github_base_repo_url = cli_arguments['metadata']['github_event_type']

            source_type = (cli_arguments.get("metadata") or {}).get("source_type")
            source_type = source_type.upper() if source_type else None

            # 4. Store adviser_id_message inputs
            message_input = {
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
            message = json.dumps(message_input)

            with open(f"/mnt/workdir/{output_message_counter}_message", "w") as f:
                f.write(message)

            output_message_counter += 1


if __name__ == "__main__":
    parse_solved_package()
