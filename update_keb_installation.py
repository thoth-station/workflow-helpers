#!/usr/bin/env python3
# workflow-helpers
# Copyright(C) 2021 Kevin Postlethwait
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

"""Update Kebechet installation details in DB during webhook workflows."""

import os
from tempfile import TemporaryDirectory

import yaml
import logging
from ogr.services.github import GithubService

from thoth.storages import GraphDatabase
from thoth.common import init_logging, cwd, RuntimeEnvironment
from thoth.python import Project

from thoth.workflow_helpers import __service_version__

init_logging()

_SLUG = os.getenv("KEBECHET_SLUG", None)
if _SLUG == "null":
    _SLUG = None

db = GraphDatabase()
db.connect()

_LOGGER = logging.getLogger("thoth.update_kebechet_installation")
_LOGGER.info("Thoth workflow-helpers task: update kebechet installation details v%s", __service_version__)


def update_keb_installation():
    """Load files and pass them to storages update function."""
    if _SLUG is None:
        _LOGGER.info("No slug present, continuing to next step in task.")
        return

    service = GithubService(
        github_app_id=os.getenv("GITHUB_APP_ID"),
        github_app_private_key_path=os.getenv("GITHUB_PRIVATE_KEY_PATH"),
    )  # TODO: extend to use other services

    project = service.get_project(namespace=_SLUG.split("/")[0], repo=_SLUG.split("/")[1])

    raw_thoth_config = project.get_file_content(".thoth.yaml")

    with TemporaryDirectory() as repo_path, cwd(repo_path):
        thoth_config = yaml.safe_load(raw_thoth_config)
        requirements_format = thoth_config["requirements_format"]
        # TODO: choose runtime_environment based on name
        runtime_environment = RuntimeEnvironment.from_dict(thoth_config["runtime_environments"][0])
        if requirements_format == "pipenv":
            pipfile_r = project.get_file_content("Pipfile")
            with open("Pipfile", "wb") as f:
                f.write(pipfile_r)

            try:
                piplock_r = project.get_file_content("Pipfile.lock")
                with open("Pipfile.lock", "wb") as f:
                    f.write(piplock_r)
                project = Project.from_files(pipfile_path="Pipfile", pipfile_lock_path="Pipfile.lock")
            except Exception:
                _LOGGER.debug("No Pipfile.lock found")
                project = Project.from_files(
                    pipfile_path="Pipfile",
                    without_pipfile_lock=True,
                    runtime_environment=runtime_environment,
                )

        elif requirements_format in ["pip", "pip-tools", "pip-compile"]:
            try:
                requirements_r = project.get_file_content("requirements.txt")
                with open("requirements.txt", "wb") as f:
                    f.write(requirements_r)
                project = Project.from_pip_compile_files(
                    requirements_path="requirements.txt",
                    allow_without_lock=True,
                    runtime_environment=runtime_environment,
                )
            except Exception:
                _LOGGER.debug("No requirements.txt found, trying to download requirements.in")
                requirements_r = project.get_file_content("requirements.in")
                with open("requirements.in", "wb") as f:
                    f.write(requirements_r.content)
                project = Project.from_pip_compile_files(
                    requirements_path="requirements.in",
                    allow_without_lock=True,
                    runtime_environment=runtime_environment,
                )

            project = Project.from_pip_compile_files(allow_without_lock=True)
        else:
            raise NotImplementedError(f"{requirements_format} requirements format not supported.")

        db.update_kebechet_installation_using_files(
            slug=_SLUG,
            installation_id=str(project.github_repo.id),
            requirements=project.pipfile.to_dict(),
            requirements_lock=project.pipfile_lock.to_dict(),
            thoth_config=thoth_config,
        )


if __name__ == "__main__":
    if _SLUG is None:
        _LOGGER.info("No slug provided, no action to be taken.")
        exit(0)
    update_keb_installation()
