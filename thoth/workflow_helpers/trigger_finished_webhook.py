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
from thoth.common import init_logging
from thoth.common import OpenShift
from .exception import TriggerFinishedWebhookInputsMissing

from thoth.workflow_helpers.configuration import Configuration

_LOGGER = logging.getLogger("trigger_finished_webhook")


def _verify_inputs_triggering_finished_webhook(
    github_event_type: Optional[str],
    github_check_run_id: Optional[int],
    github_installation_id: Optional[int],
    github_base_repo_url: Optional[str],
    workflow_name: Optional[str]
) -> None:
    """Verify if Trigger Finished Webhook inputs are correct."""
    parameters = locals()
    if not all(parameters.values()):
        raise TriggerFinishedWebhookInputsMissing(
            f"Not all inputs to trigger finished webhook are provided: {parameters}"
        )


def trigger_finished_webhook(
    has_error: bool = False,
    exception_message: Optional[str] = None,
    metadata: Optional[dict] = None,
    document_id: Optional[str] = None,
    error_type: Optional[str] = None
) -> None:
    """Trigger finished webhook."""
    payload = {}
    installation_id = {}

    if has_error:
        payload["analysis_id"] = None
        payload["exception"] = exception_message
        payload["error_type"] = error_type
        installation_id["id"] = Configuration._GITHUB_INSTALLATION_ID
        check_run_id = Configuration._GITHUB_CHECK_RUN_ID
        base_repo_url = Configuration._GITHUB_BASE_REPO_URL
        github_event_type = Configuration._GITHUB_EVENT_TYPE
        workflow_name = "workflow-not-run"

    else:
        _verify_inputs_triggering_finished_webhook(
            github_event_type=Configuration._GITHUB_EVENT_TYPE,
            github_check_run_id=Configuration._GITHUB_CHECK_RUN_ID,
            github_installation_id=Configuration._GITHUB_INSTALLATION_ID,
            github_base_repo_url=Configuration._GITHUB_BASE_REPO_URL,
            workflow_name=Configuration._WORKFLOW_NAME,
        )

        payload["analysis_id"] = document_id
        installation_id["id"] = metadata["github_installation_id"]
        check_run_id = metadata["github_check_run_id"]
        base_repo_url = metadata["github_base_repo_url"]
        github_event_type = metadata["github_event_type"]
        workflow_name = Configuration._WORKFLOW_NAME

    data = {
        "action": "finished",
        "check_run_id": check_run_id,
        "installation": installation_id,
        "base_repo_url": base_repo_url,
        "payload": payload,
    }

    key = Configuration._KEY
    msg = json.dumps(data).encode("UTF-8")

    secret = key.encode("UTF-8")
    signature = hmac.new(secret, msg, digestmod="sha1")

    headers = {
        "Accept": "application/vnd.github.antiope-preview+json",
        "Content-Type": "application/json",
        "User-Agent": f"Workflow/{workflow_name}",
        "X-GitHub-Delivery": str(uuid.uuid4()),
        "X-GitHub-Event": github_event_type,
        "X-Hub-Signature": f"sha1={signature.hexdigest()}",
    }

    _LOGGER.info("Headers:\n", headers)
    _LOGGER.info("Data:\n", data)

    response = requests.post(Configuration._WEBHOOK_CALLBACK_URL, data=json.dumps(data), headers=headers)
    response.raise_for_status()
