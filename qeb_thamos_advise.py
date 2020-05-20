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
from thamos.config import config
from thoth.python.exceptions import FileLoadError
from trigger_finished_webhook import trigger_finished_webhook

_LOGGER = logging.getLogger("qebhwt")

_GITHUB_EVENT_TYPE = os.getenv("GITHUB_EVENT_TYPE")
_GITHUB_CHECK_RUN_ID = os.getenv("GITHUB_CHECK_RUN_ID")
_GITHUB_INSTALLATION_ID = os.getenv("GITHUB_INSTALLATION_ID")
_GITHUB_BASE_REPO_URL = os.getenv("GITHUB_BASE_REPO_URL")
_ORIGIN = os.getenv("ORIGIN")


def _create_message_config_file_error():
    """Create message for config file error."""
    message = "No .thoth.yaml was provided."
    message += " Please add .thoth.yaml to your PR."

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


def qeb_hwt_thamos_advise():
    """Qeb-Hwt Thamos Advise Task."""
    os.chdir("/mnt/inputs/artifacts/repository")
    config.explicit_host = "{{inputs.parameters.THOTH_HOST}}"
    config.tls_verify = True

    artifact_path = Path.cwd()

    thoth_conf_file_path = artifact_path.joinpath(".thoth.yaml")

    if not thoth_conf_file_path.exists():
        exception_message = _create_message_config_file_error()
        trigger_finished_webhook(exception_message=exception_message, is_error=True)

    with open(thoth_conf_file_path, "r") as yaml_file:
        thoth_yaml = yaml.safe_load(yaml_file)

    try:
        analysis_id = advise_here(
            recommendation_type=thoth_yaml["runtime_environments"][0]["recommendation_type"],
            runtime_environment=thoth_yaml["runtime_environments"][0],
            nowait=True,
            github_event_type=_GITHUB_EVENT_TYPE,
            github_check_run_id=_GITHUB_CHECK_RUN_ID,
            github_installation_id=_GITHUB_INSTALLATION_ID,
            github_base_repo_url=_GITHUB_BASE_REPO_URL,
            origin=_ORIGIN,
            source_type="GITHUB_APP",
        )
    except Exception as exception:
        if isinstance(exception, (FileNotFoundError, FileLoadError, KeyError, ValueError)):
            _LOGGER.debug(exception)
            exception_message = str(exception)
        else:
            _LOGGER.debug(json.loads(exception.body)["error"])
            exception_message = json.loads(exception.body)["error"]

        trigger_finished_webhook(exception_message=exception_message, is_error=True)
