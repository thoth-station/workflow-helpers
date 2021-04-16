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
import logging
from pathlib import Path

from thoth.python import Project
from thamos.config import _Configuration

from thoth.common.enums import ThothAdviserIntegrationEnum
from thoth.common import OpenShift

from thoth.workflow_helpers.trigger_finished_webhook import trigger_finished_webhook
from thoth.workflow_helpers.common import store_messages
from thoth.workflow_helpers.configuration import Configuration
from thoth.workflow_helpers import __service_version__
from thamos.lib import advise_using_config

_LOGGER = logging.getLogger("thoth.qebhwt")
_LOGGER.info("Thoth workflow-helpers task: qebhwt v%s", __service_version__)
__COMPONENT_NAME__ = "Qeb-hwt"


def _create_message_config_file_error(no_file: bool):
    """Create message for config file error."""
    if no_file:
        initial_message = """
        No .thoth.yaml was provided.
        Please add .thoth.yaml to your PR."""
    else:
        initial_message = """
        No configuration for adviser in .thoth.yaml was provided.
        Please add configuration in .thoth.yaml to your PR."""

    message = f"""
    {initial_message}

    For more information have a look at Qeb-Hwt README file:"
    https://github.com/thoth-station/Qeb-Hwt#usage

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
        raise Exception("No path has been provided to REPO_PATH env variable.")

    if not Path(Configuration._REPO_PATH).exists():
        raise FileNotFoundError(f"Cannot find the file on this path: {Configuration._REPO_PATH}")

    output_messages: list = []

    OpenShift.verify_github_app_inputs(
        github_event_type=Configuration._GITHUB_EVENT_TYPE,
        github_check_run_id=Configuration._GITHUB_CHECK_RUN_ID,
        github_installation_id=Configuration._GITHUB_INSTALLATION_ID,
        github_base_repo_url=Configuration._GITHUB_BASE_REPO_URL,
        origin=Configuration._ORIGIN,
    )

    os.chdir(Configuration._REPO_PATH)
    thoth_yaml_config = _Configuration()

    if not thoth_yaml_config.config_file_exists():
        exception_message = _create_message_config_file_error(no_file=True)
        store_messages(output_messages)
        trigger_finished_webhook(exception_message=exception_message, has_error=True, error_type="MissingThothYamlFile")
        return

    try:
        requirements_format = thoth_yaml_config.requirements_format
        if requirements_format == "pipenv":
            project = Project.from_files(without_pipfile_lock=not os.path.exists("Pipfile.lock"))
        elif requirements_format in ("pip", "pip-tools", "pip-compile"):
            project = Project.from_pip_compile_files(allow_without_lock=True)
        else:
            raise ValueError(f"Unknown configuration option for requirements format: {requirements_format!r}")

        pipfile_str = project.pipfile.to_string()
        pipfile_lock_str = project.pipfile_lock.to_string() if project.pipfile_lock else ""

    except Exception as exception:
        _LOGGER.debug(json.loads(exception.body)["error"])  # type: ignore
        exception_message = json.loads(exception.body)["error"]  # type: ignore
        store_messages(output_messages)
        trigger_finished_webhook(exception_message=exception_message, has_error=True)
        return

    response = advise_using_config(
        pipfile=pipfile_str,
        pipfile_lock=pipfile_lock_str,
        config=json.dumps(thoth_yaml_config.content),
        github_event_type=Configuration._GITHUB_EVENT_TYPE,
        github_check_run_id=Configuration._GITHUB_CHECK_RUN_ID,
        github_installation_id=Configuration._GITHUB_INSTALLATION_ID,
        github_base_repo_url=Configuration._GITHUB_BASE_REPO_URL,
        origin=Configuration._ORIGIN,
        source_type=ThothAdviserIntegrationEnum.GITHUB_APP,
        no_static_analysis=False,
        nowait=True,
    )

    _LOGGER.info(f"thamos advise response: {response}.")


if __name__ == "__main__":
    qeb_hwt_thamos_advise()
