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
    force_sync = bool(int(os.getenv("FORCE_SYNC")))

    message_contents = {
        "inspection_id": {"type": "str", "value": inspection_id},
        "force_sync": {"type": "bool", "value": force_sync},
    }

    message = {"topic_name": "thoth.inspection-completed", "message_contents": message_contents}

    with open(MSG_FILE, "rw") as f:
        if os.stat(f).st_size != 0:
            all_messages: list = json.load(f)
            if type(all_messages) != list:
                raise TypeError(f"Message file must be a list of messages. Got type {type(all_messages)}")
            all_messages.append(message)
        else:
            all_messages = [message]

        json.dump(all_messages, f)


if __name__ == "__main__":
    create_inspection_complete_message()
