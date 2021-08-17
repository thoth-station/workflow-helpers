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

"""This task creates issues in repositories using Kebechet GitHub app when data purges occur."""

import os
import logging

from ogr.services.github import GithubService
from prometheus_client import Gauge

from thoth.storages import GraphDatabase
from thoth.workflow_helpers import __service_version__
from thoth.workflow_helpers.configuration import Configuration
from thoth.workflow_helpers.common import send_metrics, set_schema_metrics, PROMETHEUS_REGISTRY


GRAPH = GraphDatabase()
GRAPH.connect()

_LOGGER = logging.getLogger("thoth.create_purge_issues")
_LOGGER.info("Thoth workflow-helpers task: create_purge_issue v%s", __service_version__)


number_purge_issues_created = Gauge(
    "thoth_number_purge_issues_created",
    "Thoth number of purge issues created",
    ["component", "env"],
    registry=PROMETHEUS_REGISTRY,
)

number_purge_issues_total = Gauge(
    "thoth_number_purge_issues_total",
    "Thoth number of purge issues to be created.",
    ["component", "env"],
    registry=PROMETHEUS_REGISTRY,
)


def main():
    """Create issues warning users of data purge and how to continue injesting knowledge from Thoth."""
    # this takes care of accidentally passing a filter on empty strings to the database which will usually result in no
    # entries being found
    os_name = os.getenv("PURGE_OS_NAME") if os.getenv("PURGE_OS_NAME") else None
    os_version = os.getenv("PURGE_OS_VERSION") if os.getenv("PURGE_OS_VERSION") else None
    python_version = os.getenv("PURGE_PYTHON_VERSION") if os.getenv("PURGE_PYTHON_VERSION") else None

    all_installations = GRAPH.get_kebechet_github_installation_info_with_software_environment_all(
        os_name=os_name,
        os_version=os_version,
        python_version=python_version,
    )

    gh = GithubService(
        token=os.getenv("GITHUB_KEBECHET_TOKEN"),
        github_app_id=os.getenv("GITHUB_APP_ID"),
        github_private_key_path=os.getenv("GITHUB_PRIVATE_KEY_PATH"),
    )

    number_issues_total = len(all_installations)
    number_issues_created = 0

    for i in all_installations:
        try:
            p = gh.get_project(namespace=i["slug"].split("/")[0], repo=i["repo_name"])
            # We shouldn't have to check if the issue exists because the purge job is run for each env only once
            p.create_issue(
                title=f"{os_name}:{os_version}py{python_version} being purged from Thoth DB",
                body=(
                    "Thoth is constantly ingesting new data, it purges data as operating system "
                    "and python versions are EOL. "
                    f"{os_name}:{os_version}py{python_version} was just removed "
                    "and Thoth will no longer be able to advise on this environment. "
                    "Please update to a newer version or another supported operating system."
                ),
                private=i["private"],
                labels=["bot"],
            )

            number_issues_created += 1

        except Exception as e:
            _LOGGER.error(f"Could not create issue for {i['slug']} because: {e!r}")

    set_schema_metrics()
    number_purge_issues_created.labels(component="workflow-helpers", env=Configuration.THOTH_DEPLOYMENT_NAME).set(
        number_issues_created
    )
    number_purge_issues_total.labels(component="workflow-helpers", env=Configuration.THOTH_DEPLOYMENT_NAME).set(
        number_issues_total
    )
    send_metrics()


if __name__ == "__main__":
    main()
