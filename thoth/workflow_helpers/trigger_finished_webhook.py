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

"""This is script for triggering finished webhook for workflow task."""

import hmac
import json
import os
import requests
import uuid
import logging

from typing import Optional
from utils import retrieve_adviser_document
from thoth.common import init_logging

_LOGGER = logging.getLogger("trigger_finished_webhook")

_KEY = os.getenv("WEBHOOK_SECRET")
_WEBHOOK_CALLBACK_URL = os.getenv("WEBHOOK_CALLBACK_URL")


def trigger_finished_webhook(
    has_error: bool = False,
    exception_message: Optional[str] = None,
    metadata: Optional[dict] = None,
    document_id: Optional[str] = None,
):
    """Trigger finished webhook."""
    payload = {}

    if has_error:
        payload["analysis_id"] = None
        payload["exception"] = exception_message
    else:
        payload["analysis_id"] = document_id

    installation_id = {}
    installation_id["id"] = int(metadata["github_installation_id"])

    data = {
        "action": "finished",
        "check_run_id": int(metadata["github_check_run_id"]),
        "installation": installation_id,
        "base_repo_url": metadata["github_base_repo_url"],
        "payload": payload,
    }

    key = _KEY
    msg = json.dumps(data).encode("UTF-8")

    secret = key.encode("UTF-8")
    signature = hmac.new(secret, msg, digestmod="sha1")

    headers = {
        "Accept": "application/vnd.github.antiope-preview+json",
        "Content-Type": "application/json",
        "User-Agent": "Workflow/{{inputs.parameters.WORKFLOW_NAME}}",
        "X-GitHub-Delivery": str(uuid.uuid4()),
        "X-GitHub-Event": metadata["github_event_type"],
        "X-Hub-Signature": f"sha1={signature.hexdigest()}",
    }

    _LOGGER.info("Headers:\n", headers)
    _LOGGER.info("Data:\n", data)

    WEBHOOK_CALLBACK_URL = _WEBHOOK_CALLBACK_URL

    response = requests.post(WEBHOOK_CALLBACK_URL, data=json.dumps(data), headers=headers)
    response.raise_for_status()
