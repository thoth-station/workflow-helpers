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

"""This is script for Qeb-Hwt thamos advise workflow task."""


import os
import json
import yaml
import logging
from pathlib import Path

from thamos.lib import advise_here
from thamos.config import _Configuration
from thoth.python.exceptions import FileLoadError
from thamos.exceptions import NoRuntimeEnvironmentError
from thoth.workflow_helpers.trigger_finished_webhook import trigger_finished_webhook
from thoth.workflow_helpers.configuration import Configuration

_LOGGER = logging.getLogger("qebhwt")


def _create_message_config_file_error(no_file: bool):
    """Create message for config file error."""
    if no_file:
        message = "No .thoth.yaml was provided."
        message += " Please add .thoth.yaml to your PR."
    else:
        message = "No configuration for adviser in .thoth.yaml was provided."
        message += " Please add configuration in .thoth.yaml to your PR."

    message += (
        "\n\nFor more information have a look at Qeb-Hwt README file:"
        + "\n https://github.com/thoth-station/Qeb-Hwt#usage\n"
    )

    message += """

    Example:
        host: khemenu.thoth-station.ninja
        tls_verify: false
        requirements_format: pipenv

        runtime_environments:
        - name: rhel:8
          operating_system:
            name: rhel
            version: "8"
          python_version: "3.6"
          recommendation_type: stable
    """
    return message


def qeb_hwt_thamos_advise() -> None:
    """Qeb-Hwt Thamos Advise Task."""
    if not Configuration._REPO_PATH:
        raise Exception(f"No path has been provided to REPO_PATH env variable.")

    if not Path(Configuration._REPO_PATH).exists():
        raise FileNotFoundError(f"Cannot find the file on this path: {Configuration._REPO_PATH}")

    os.chdir(Configuration._REPO_PATH)
    thoth_yaml_config = _Configuration()

    if not thoth_yaml_config.config_file_exists():
        exception_message = _create_message_config_file_error(no_file=True)
        trigger_finished_webhook(exception_message=exception_message, has_error=True)
        return

    try:
        analysis_id = advise_here(
            nowait=True,
            github_event_type=Configuration._GITHUB_EVENT_TYPE,
            github_check_run_id=Configuration._GITHUB_CHECK_RUN_ID,
            github_installation_id=Configuration._GITHUB_INSTALLATION_ID,
            github_base_repo_url=Configuration._GITHUB_BASE_REPO_URL,
            origin=Configuration._ORIGIN,
            source_type="GITHUB_APP",
        )
        _LOGGER.info("Successfully submitted thamos advise call.")
    except Exception as exception:
        if isinstance(
            exception, (
                NoRuntimeEnvironmentError,
                FileNotFoundError,
                FileLoadError,
                KeyError,
                ValueError
                )
            ):
            _LOGGER.debug(exception)
            exception_message = str(exception)
        else:
            _LOGGER.debug(json.loads(exception.body)["error"])
            exception_message = json.loads(exception.body)["error"]

        trigger_finished_webhook(exception_message=exception_message, has_error=True)


if __name__ == "__main__":
    qeb_hwt_thamos_advise()
