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

"""Utility functions for repository initialization step."""

from ogr.services.github import GithubProject
from ogr.services.github.auth_providers.github_app import GithubApp
from thamos.lib import write_files
from typing import Tuple
from contextlib import contextmanager
import urllib3
from tempfile import TemporaryDirectory
import git
import os
from thoth.common import cwd

APP_NAME = os.getenv("GITHUB_APP_NAME", "khebhut")


def _write_result2files(result):
    pipfile = result["report"]["products"][0]["project"]["requirements"]
    pipfile_lock = result["report"]["products"][0]["project"]["requirements_locked"]
    write_files(pipfile, pipfile_lock, "pipenv")


def _parse_url_4_args(url: str) -> Tuple[str, str, str]:
    """
    Parse url for args required by kebechet_runners.run(...).

    args:
    url to remote git repository
    returns:
    tuple: (slug, namespace, project, service_url)
    """
    scheme, _, host, _, slug, _, _ = urllib3.util.parse_url(url)
    slug = slug[1:]
    namespace, project = slug.split("/")

    service_url = host

    return (namespace, project, service_url)


def _remove_protocol(url: str) -> str:
    return urllib3.util.parse_url(url).host


@contextmanager
def cloned_repo(project: GithubProject, **clone_kwargs):
    """Clone the given Git repository and cd into it."""
    service_url = project.service.instance_url

    installation = isinstance(project.service.authentication, GithubApp)

    namespace, repository = (project.namespace, project.repo)
    slug = f"{namespace}/{repository}"
    if installation:
        access_token = project.service.authentication.get_token(namespace, repository)  # type: ignore
        repo_url = f"https://{APP_NAME}:{access_token}@{service_url}/{slug}"
    else:
        repo_url = f"git@{_remove_protocol(service_url)}:{slug}.git"

    with TemporaryDirectory() as repo_path, cwd(repo_path):
        # _LOGGER.info(f"Cloning repository {repo_url} to {repo_path}")
        repo = git.Repo.clone_from(repo_url, repo_path, branch=project.default_branch, **clone_kwargs)
        repo.config_writer().set_value("user", "name", os.getenv("KEBECHET_GIT_NAME", "Kebechet")).release()
        repo.config_writer().set_value(
            "user",
            "email",
            os.getenv("KEBECHET_GIT_EMAIL", "noreply+kebechet@redhat.com"),
        ).release()
        yield repo


def _get_file_contents(path: str):
    with open(path, "r") as f:
        return f.read()


def _write_to_file(path: str, contents: str):
    with open(path, "w+") as f:
        f.write(contents)
