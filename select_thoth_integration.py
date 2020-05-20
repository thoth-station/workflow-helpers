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

"""This script run in a workflow task to select Thoth integration workflow to run."""

import json
import os
import logging

from thoth.workflow_helpers.utils import retrieve_adviser_document
from thoth.workflow_helpers.trigger_finished_webhook import trigger_finished_webhook
from thoth.common.enums import ThothAdviserIntegrationEnum

_LOGGER = logging.getLogger("select_thoth_integration")


def trigger_integration_workflow():
    """Trigger specific workflow depending on Thoth integration type."""
    metadata = retrieve_adviser_document()
    source_type = metadata["source_type"]

    if source_type is ThothAdviserIntegrationEnum.KEBECHET:
        with open("/tmp/source_type", "w") as f:
            f.write(source_type)

        with open("/tmp/origin", "w") as f:
            if metadata["origin"] is not None:
                f.write(metadata["origin"])

    if source_type is ThothAdviserIntegrationEnum.GITHUB_APP:
        _THOTH_DOCUMENT_ID = os.getenv("THOTH_DOCUMENT_ID")
        trigger_finished_webhook(metadata=metadata, document_id=_THOTH_DOCUMENT_ID)