#!/usr/bin/env python3
# workflow-helpers
# Copyright(C) 2022 Kevin Postlethwait
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

"""This script sends all webhooks in a directory, each is represented by a JSON object."""

import json
import logging
import os

from kubernetes import kubernetes as k8
from kubernetes.client.rest import ApiException as K8ApiException

import requests

_LOGGER = logging.getLogger("thoth.send_webhooks")

try:
    k8.config.load_kube_config()
except Exception as exc:
    # load_kube_config throws if there is no config,
    # but does not document what it throws,
    # so I can't rely on any particular type here
    _LOGGER.warning(
        "Failed to load kube config, fallback to incluster config: %s",
        str(exc),
    )
    k8.config.load_incluster_config()

core_api = k8.client.CoreV1Api()

dir = os.environ["WEBHOOK_DIR"]
document_id = os.environ["DOCUMENT_ID"]
secret_namespace = os.environ["THOTH_BACKEND_NAMESPACE"]

for f_name in os.listdir(dir):
    path = os.path.join(dir, f_name)
    if not os.path.isfile(path=path):
        continue
    with open(path, "r") as f:
        webhook = json.load(f)
    contents = {
        "client_data": webhook["client_data"],
        "document_id": document_id,
    }
    headers = {"Authorization": webhook["Authorization"]}
    try:
        requests.post(url=webhook["callback_url"], data=contents, headers=headers)
    except Exception as e:
        _LOGGER.exception(e)

try:
    core_api.delete_namespaced_secret(name=f"callback-{document_id}", namespace=secret_namespace)
except K8ApiException:
    _LOGGER.debug(f"Callback secret (callback-{document_id}) does not exist.")
