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

"""These are common scripts that can be reused."""

import os

THOTH_DOCUMENT_PATH = os.getenv("THOTH_DOCUMENT_PATH")

def retrieve_adviser_document():
    """Retrieve document ID."""
    metadata = {}

    if THOTH_DOCUMENT_PATH:

        document = json.loads(THOTH_DOCUMENT_PATH)
        cli_arguments = document["metadata"]["arguments"]["thoth-adviser"]
        metadata = cli_arguments.get("metadata")

    return metadata
