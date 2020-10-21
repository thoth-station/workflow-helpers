#!/usr/bin/env python3
# workflow-helpers Kebechet Administrator
# Copyright(C) 2020 Sai Sankar Gochhayat
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

"""Kebechet Administrator.

This script run in a workflow task to take an incoming message and decides which repositories Kebechet
needs to be run on and store the necessary messages to be sent.
"""

import logging
import json
import semver
from typing import Dict
from thoth.storages import GraphDatabase
from thoth.workflow_helpers.configuration import Configuration
from thoth.messaging import __all__ as all_messages
from thoth.workflow_helpers import __service_version__

__COMPONENT_NAME__ = "Kebechet Administrator"

_LOGGER = logging.getLogger("thoth.run_kebechet_administrator")
_LOGGER.info("Thoth workflow-helpers task: run_kebechet_administrator v%s", __service_version__)

# Estabilish connection to Database.
GRAPH = GraphDatabase()
GRAPH.connect()

_URL_PREFIX = "https://github.com/"

output_messages = []  # Messages to be sent by producer.


def _handle_solved_message(Configuration):  # noqa: N803
    """Handle all the messages for which Kebechet needs to run on if the sovler type matches the os type."""
    solver_string = Configuration.get("THOTH_SOLVER_NAME")  # ex - solver-fedora-31-py38
    if not solver_string:
        raise ValueError(
            f"SolverMessageType has been provided to the MESSAGE_TYPE env variable. \
            but solver name is missing."
        )
    _, os_name, os_version, python_version = solver_string.rsplit(sep="-", maxsplit=3)
    python_version = ".".join([i for i in python_version if i.isdigit()])  # generates '3.8' from 'py39'
    repositories: Dict[str, Dict] = GRAPH.get_kebechet_github_installations_info_for_python_package_version(
        package_name=Configuration.PACKAGE_NAME,
        index_url=Configuration.PACKAGE_INDEX,
        os_name=os_name,
        os_version=os_version,
        python_version=python_version,
    )  # We query without the package_version.
    for key in repositories.keys():
        repo_info = repositories[key]
        # Construct the message input
        if repo_info.get("private"):
            continue  # We skip for private repo's.
        if semver.compare(repo_info.get("package_version"), Configuration.PACKAGE_VERSION):
            continue  # We dont schedule, if the package version > version of the solved package version.
        message_input = {
            "component_name": {"type": "str", "value": __COMPONENT_NAME__},
            "service_version": {"type": "str", "value": __service_version__},
            "url": {"type": "str", "value": _URL_PREFIX + key},
            "service_name": {"type": "str", "value": "github"},
            "installation_id": {"type": "str", "value": repo_info.get("installation_id")},
        }

        # We store the message to put in the output file here.
        output_messages.append({"topic_name": "thoth.kebechet-run-url-trigger", "message_contents": message_input})


def _handle_package_issue(Configuration):  # noqa: N803
    """Handle all the messages for which Kebechet needs to run on all repos associated."""
    # We getch all the Kebechet repos using a non optimal package(missing package or CVE or missing version)
    repositories: Dict[str, Dict] = GRAPH.get_kebechet_github_installations_info_for_python_package_version(
        package_name=Configuration.PACKAGE_NAME,
        version=Configuration.PACKAGE_VERSION,
        index_url=Configuration.PACKAGE_INDEX,
    )
    # The keys represent the repo names and the value dictionary is the details for the repo.
    for key in repositories.keys():
        repo_info = repositories[key]
        # Construct the message input
        if repo_info.get("private"):
            continue  # We skip for private repo's.
        message_input = {
            "component_name": {"type": "str", "value": __COMPONENT_NAME__},
            "service_version": {"type": "str", "value": __service_version__},
            "url": {"type": "str", "value": _URL_PREFIX + key},
            "service_name": {"type": "str", "value": "github"},
            "installation_id": {"type": "str", "value": repo_info.get("installation_id")},
        }

        # We store the message to put in the output file here.
        output_messages.append({"topic_name": "thoth.kebechet-run-url-trigger", "message_contents": message_input})


# This handler dispatches the specific method based on a paticular message.
_message_handler = {
    "SolvedPackageMessage": _handle_solved_message,
    "HashMismatchMessage": _handle_package_issue,
    "MissingPackageMessage": _handle_package_issue,
    "MissingVersionMessage": _handle_package_issue,
    "CVEProvidedMessage": _handle_package_issue,
}


def _input_validation():
    required_inputs = frozenset({"PACKAGE_NAME", "PACKAGE_VERSION", "PACKAGE_INDEX", "MESSAGE_TYPE"})
    supported_messages = _message_handler.keys()
    for env_var in required_inputs:
        if not getattr(Configuration, env_var):
            _LOGGER.error(f"No value has been provided to the {env_var} env variable.")
            raise ValueError(f"No value has been provided to the {env_var} env variable.")
    # Validation on the message type  # ex - `SolvedPackageMessage.__name__`
    if Configuration.MESSAGE_TYPE not in supported_messages or Configuration.MESSAGE_TYPE not in all_messages:
        _LOGGER.error(
            f"Unsupported message type has been provided to the MESSAGE_TYPE env variable. \
            Message type - {Configuration.MESSAGE_TYPE}"
        )
        raise ValueError(
            f"Unsupported message type has been provided to the MESSAGE_TYPE env variable. \
            Message type - {Configuration.MESSAGE_TYPE}"
        )


def run_kebechet_administrator():
    """Run Kebechet Administrator to determine the repositories on which Kebechet will be triggered internally."""
    # We check if all the necessary env variables have been set correctly.
    _input_validation()
    # If input validation passes, we call the specific handler to generate the messages for the producer.
    _message_handler[Configuration.MESSAGE_TYPE](Configuration)

    # Store message to file that need to be sent.
    with open(f"/mnt/workdir/messages_to_be_sent.json", "w") as json_file:
        json.dump(output_messages, json_file)

    if output_messages:
        _LOGGER.info(f"Successfully stored file with messages to be sent!: {output_messages}")


if __name__ == "__main__":
    run_kebechet_administrator()
