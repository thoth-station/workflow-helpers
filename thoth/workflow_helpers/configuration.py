#!/usr/bin/env python3
# thoth-workflow-helpers
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

"""Configuration for all workflow helpers."""

import logging
import os
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)


class Configuration:
    """Configuration for workflow-helpers."""

    _REPO_PATH = os.getenv("REPO_PATH")

    _ORIGIN = os.getenv("ORIGIN")
    _GITHUB_EVENT_TYPE = os.getenv("GITHUB_EVENT_TYPE")
    _GITHUB_CHECK_RUN_ID = os.getenv("GITHUB_CHECK_RUN_ID")
    _GITHUB_INSTALLATION_ID = os.getenv("GITHUB_INSTALLATION_ID")
    _GITHUB_BASE_REPO_URL = os.getenv("GITHUB_BASE_REPO_URL")
    _THOTH_HOST = os.getenv("THOTH_HOST")

    _WORKFLOW_NAME = os.getenv("WORKFLOW_NAME")

    _KEY = os.getenv("WEBHOOK_SECRET")
    _WEBHOOK_CALLBACK_URL = os.getenv("WEBHOOK_CALLBACK_URL")
