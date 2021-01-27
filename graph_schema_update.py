#!/usr/bin/env python3
# graph-schema-update
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

"""Graph schema update task for Thoth project."""

import logging

from thoth.workflow_helpers import __service_version__
from thoth.storages import GraphDatabase
from thoth.workflow_helpers.common import send_metrics

_LOGGER = logging.getLogger("thoth.graph_schema_update")
_LOGGER.info("Thoth workflow-helpers task: graph_schema_update v%s", __service_version__)


def update_schema() -> None:
    """Perform schema update for the graph database."""
    graph = GraphDatabase()
    graph.connect()

    graph.initialize_schema()


if __name__ == "__main__":
    send_metrics()
    update_schema()
