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

_LOGGER = logging.getLogger(__name__)


class Configuration:
    """Configuration for workflow-helpers."""

    # General
    _THOTH_ADVISER_METADATA = os.getenv("THOTH_ADVISER_METADATA")

    # Python Package Info
    PACKAGE_NAME = os.getenv("THOTH_PACKAGE_NAME")
    PACKAGE_VERSION = os.getenv("THOTH_PACKAGE_VERSION")
    PACKAGE_INDEX = os.getenv("THOTH_PACKAGE_INDEX")

    # Kebechet Administrator
    # This needs package info + solver type + message type
    SOLVER_NAME = os.getenv("THOTH_SOLVER_NAME")
    MESSAGE_TYPE = os.getenv("THOTH_MESSAGE_TYPE")

    # metrics
    THOTH_METRICS_PUSHGATEWAY_URL = os.getenv("PROMETHEUS_PUSHGATEWAY_URL")
    THOTH_DEPLOYMENT_NAME = os.getenv("THOTH_DEPLOYMENT_NAME")
