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

"""Kebechet Administrator

   This script run in a workflow task to take and incoming message and decide and decides which repositores
   Kebechet needs to be run on and schedules the necessary messages.
"""

import logging
from typing import List
from thoth.storages import GraphDatabase
from thoth.workflow_helpers.configuration import Configuration
from thoth.messaging import __all__ as all_messages
from thoth.workflow_helpers import __service_version__

_LOGGER = logging.getLogger("thoth.run_kebechet_administrator")
_LOGGER.info("Thoth workflow-helpers task: run_kebechet_administrator v%s", __service_version__)

# Estabilish connection to Database.
GRAPH = GraphDatabase()
GRAPH.connect()


def _input_validation():
    required_inputs = frozenset({"PACKAGE_NAME", "PACKAGE_VERSION", "PACKAGE_INDEX", "MESSAGE_TYPE"})
    supported_messages = frozenset(
        {"SolvedPackageMessage", "HashMismatchMessage", "MissingPackageMessage", "MissingVersionMessage"}
    )
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

    print(all_messages)


if __name__ == "__main__":
    run_kebechet_administrator()
