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
from thamos.swagger_client import PythonStack
from thamos.config import _Configuration

from thoth.common.enums import ThothAdviserIntegrationEnum
from thoth.common import OpenShift

from thoth.workflow_helpers.trigger_finished_webhook import trigger_finished_webhook
from thoth.workflow_helpers.configuration import Configuration
from thoth.workflow_helpers import __service_version__

_LOGGER = logging.getLogger("thoth.qebhwt")
_LOGGER.info("Thoth workflow-helpers task: qebhwt v%s", __service_version__)
__COMPOENENT_NAME__ = "Qeb-hwt"


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
        raise Exception(f"No path has been provided to REPO_PATH env variable.")

    if not Path(Configuration._REPO_PATH).exists():
        raise FileNotFoundError(f"Cannot find the file on this path: {Configuration._REPO_PATH}")

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
        trigger_finished_webhook(exception_message=exception_message, has_error=True, error_type="MissingThothYamlFile")
        return

    # Fetch recommedation type
    try:
        thoth_yaml_runtime_env = thoth_yaml_config.content.get("runtime_environments")
        recommendation_type = thoth_yaml_runtime_env[0].get("recommendation_type") if thoth_yaml_config else "latest"

        requirements_format = thoth_yaml_config.requirements_format
        if requirements_format == "pipenv":
            project = Project.from_files(without_pipfile_lock=not os.path.exists("Pipfile.lock"))
        elif requirements_format in ("pip", "pip-tools", "pip-compile"):
            project = Project.from_pip_compile_files(allow_without_lock=True)
        else:
            raise ValueError(f"Unknown configuration option for requirements format: {requirements_format!r}")

        pipfile = project.pipfile.to_string()
        pipfile_lock_str = project.pipfile_lock.to_string() if project.pipfile_lock else ""
        application_stack = PythonStack(
            requirements=pipfile, requirements_lock=pipfile_lock_str, requirements_format=requirements_format
        ).to_dict()
    except Exception as exception:
        _LOGGER.debug(json.loads(exception.body)["error"])  # type: ignore
        exception_message = json.loads(exception.body)["error"]  # type: ignore
        trigger_finished_webhook(exception_message=exception_message, has_error=True)
        return

    # The input for AdviserTriggerMessage if no exceptions were found
    message_input = {
        "component_name": {"type": "str", "value": __COMPOENENT_NAME__},
        "service_version": {"type": "str", "value": __service_version__},
        "application_stack": {"type": "Dict", "value": application_stack},
        "recommendation_type": {"type": "str", "value": recommendation_type},
        "github_event_type": {"type": "str", "value": Configuration._GITHUB_EVENT_TYPE},
        "github_check_run_id": {"type": "int", "value": int(Configuration._GITHUB_CHECK_RUN_ID)},
        "github_installation_id": {"type": "int", "value": int(Configuration._GITHUB_INSTALLATION_ID)},
        "github_base_repo_url": {"type": "str", "value": Configuration._GITHUB_BASE_REPO_URL},
        "origin": {"type": "str", "value": Configuration._ORIGIN},
        "source_type": {"type": "str", "value": ThothAdviserIntegrationEnum.GITHUB_APP.name},
    }

    # We store the message to put in the output file here.
    message_output = [{"topic_name": "thoth.adviser-trigger", "message_contents": message_input}]

    # Store message to file that need to be sent.
    with open(f"/mnt/workdir/messages_to_be_sent.json", "w") as json_file:
        json.dump(message_output, json_file)

    if message_output:
        _LOGGER.info(f"Successfully stored file with messages to be sent!: {message_output}")


if __name__ == "__main__":
    qeb_hwt_thamos_advise()
