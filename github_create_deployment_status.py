#!/usr/bin/env python3
# create_github_deployment
# Copyright(C) 2021 Christoph Görn
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


"""A tiny helper to create a GitHub Deployment."""


import logging
import json
import os
import sys

import http.client

from thoth.workflow_helpers import __service_version__


logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger("thoth.devops.create_github_deployment")
_LOGGER.info("Thoth workflow-helpers: github_create_deployment v%s", __service_version__)


REPO_FULL_NAME = os.getenv("REPO_FULL_NAME", None)
DEPLOYMENT_ID = os.getenv("DEPLOYMENT_ID", None)
PAYLOAD = os.getenv("PAYLOAD", None)
STATE = os.getenv("STATE", "inactive")  # TODO check is in the list of valid states
ENVIRONMENT = os.getenv("ENVIRONMENT", "test")
ENVIRONMENT_URL = os.getenv("ENVIRONMENT_URL", None)
DESCRIPTION = os.getenv("DESCRIPTION ", f"a deployment to {ENVIRONMENT} just changed state to {STATE}")

if __name__ == "__main__":
    if REPO_FULL_NAME is None:
        _LOGGER.error("no full name of the repository provided?!")
        sys.exit(2)

    if DEPLOYMENT_ID is None:
        _LOGGER.error("no deployment id provided?!")
        sys.exit(3)

    _deployment_status_url = f"/repos/{REPO_FULL_NAME}/deployments/{DEPLOYMENT_ID}/statuses"

    data = {
        "state": STATE,
        #            "log_url": "$(LOG_URL)",
        "description": DESCRIPTION,
        "environment_url": ENVIRONMENT_URL,
        "environment": ENVIRONMENT,
        "auto_inactive": "true",
    }

    _LOGGER.debug("sending to github: ", data)

    conn = http.client.HTTPSConnection("api.github.com")
    r = conn.request(
        "POST",
        _deployment_status_url,
        body=json.dumps(data),
        headers={
            "User-Agent": f"Thoth workflow-helpers/v%{__service_version__}",
            "Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
            "Accept": "application/vnd.github.v3+json",
        },
    )
    resp = conn.getresponse()

    # only look for 201 statuses to signify a deployment was successfully
    # created
    if resp.status != 201:
        _LOGGER.error(f"Error: {resp.status}")
        _LOGGER.info(resp.read())

        sys.exit(1)
    else:
        body = json.loads(resp.read().decode())
        _LOGGER.info(
            f"GitHub deployment state created for {REPO_FULL_NAME}: "
            f'id={body["id"]} state={body["state"]} '
            f'environment={body["environment"]} url={body["url"]}'
        )
