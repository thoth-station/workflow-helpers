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

"""This task creates a message file to be used by messaging cli in a workflow."""

import os

from thoth.messaging.inspection_complete import InspectionCompletedMessage

from thoth.workflow_helpers.common import store_messages
from thoth.workflow_helpers import __service_version__

COMPONENT_NAME = "workflow_helper.create_inspection_complete_message"


def create_inspection_complete_message():
    """Create message file (InspectionCompleteMessage) to be sent by thoth-messaging cli."""
    inspection_id = os.getenv("THOTH_AMUN_INSPECTION_ID")
    force_sync = bool(int(os.getenv("THOTH_FORCE_SYNC")))

    message_contents = {
        "service_version": {"type": "str", "value": __service_version__},
        "component_name": {"type": "str", "value": COMPONENT_NAME},
        "inspection_id": {"type": "str", "value": inspection_id},
        "force_sync": {"type": "bool", "value": force_sync},
    }

    message = {"topic_name": InspectionCompletedMessage.base_name, "message_contents": message_contents}
    store_messages([message])


if __name__ == "__main__":
    create_inspection_complete_message()
