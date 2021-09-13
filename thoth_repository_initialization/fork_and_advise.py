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

"""This task creates demos a simple thoth-advise on a repository by forking the project and opening a PR."""

import os
import logging
from ogr.services.github import GithubService
import thamos

from utils import _parse_url_4_args, cloned_repo, _write_to_file, _write_result2files
from . import templates
from . import resources

import click

import importlib.resources as pkg_resources

_TOKEN = os.getenv("GITHUB_TOKEN")

_LOGGER = logging.getLogger("workflow-meteor-demo")


@click.command()
@click.option("-u", "--project-url", envvar="THOTH_DEMO_PROJECT_URL", required=True)
@click.option("-f", "--fork-namespace", envvar="THOTH_DEMO_FORK_NAMESPACE")
def run(project_url: str, fork_namespace: str):
    """Run single repo thoth-advise demo."""
    namespace, repo, service_url = _parse_url_4_args(project_url)
    service = GithubService(token=_TOKEN)
    original_project = service.get_project(namespace=namespace, repo=repo)
    if original_project.is_fork:
        original_project.create_issue(
            title="Thoth Demo failed due to forked repository",
            body=templates.run_on_fork_issue,
        )
        raise NotImplementedError("This workflow does not work on projects which are already forks of other projects.")

    original_project.github_repo.create_fork(organization=fork_namespace)
    fork_project = service.get_project(namespace=fork_namespace, repo=repo)
    base_thoth_config = pkg_resources.read_text(resources, "example.thoth.yaml")
    with cloned_repo(fork_project) as repo:
        _write_to_file(".thoth.yaml", base_thoth_config)

        result, error = thamos.lib.advise_here()  # type: ignore

        if error:
            _LOGGER.warning("Thoth adviser failed to resolve a stack... Quitting")
            original_project.create_issue(
                title="Thoth cannot issue advice at this time.", body=templates.failed_issue_body
            )
            exit(1)

        _write_result2files(result)
        repo.git.checkout("-b", "thoth-demo")
        repo.index.add([".thoth.yaml", "Pipfile", "Pipfile.lock"])
        repo.index.commit("Lock down dependencies using Thoth resolution and add basic thoth configuration.")
        repo.remotes.origin.push("thoth-demo")
        original_project.create_pr(
            title="Demonstration of Thoth dependency management",
            body=templates.thoth_demo_body,
            target_branch=original_project.default_branch,
            source_branch="thoth-demo",
            fork_username=fork_namespace,
        )


if __name__ == "__main__":
    run()
