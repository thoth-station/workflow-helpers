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
import json

MSG_FILE = "/mnt/workdir/messages_to_be_sent.json"


def create_inspection_complete_message():
    """Create message file (InspectionCompleteMessage) to be sent by thoth-messaging cli."""
    inspection_id = os.getenv("THOTH_AMUN_INSPECTION_ID")
    amun_api_url = os.getenv("THOTH_AMUN_API_URL")
    deployment_name = os.getenv("THOTH_DEPLOYMENT_NAME")

    message_contents = {
        "inspection_id": {"type": "str", "value": inspection_id},
        "amun_api_url": {"type": "str", "value": amun_api_url},
        "deployment_name": {"type": "str", "value": deployment_name},
    }

    messages = [{"topic_name": "thoth.inspection-completed", "message_contents": message_contents}]

    with open(MSG_FILE, "w") as f:
        json.dump(messages, f)


if __name__ == "__main__":
    create_inspection_complete_message()
