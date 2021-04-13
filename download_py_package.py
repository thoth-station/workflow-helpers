#!/usr/bin/env python3
# workflow-helpers
# Copyright(C) 2020 Kevin Postlethwait
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

"""This script run in a workflow task to download and extract python package for future steps."""

import tarfile
import zipfile
import os
import logging
import json
from urllib import request

from thoth.analyzer import run_command
from thoth.workflow_helpers.configuration import Configuration
from thoth.workflow_helpers import __service_version__
from bs4 import BeautifulSoup, SoupStrainer

from thoth.messaging import update_provides_source_distro_message, missing_version_message
from thoth.messaging.update_provides_src_distro import MessageContents as UpdateProvidesSrcDistroContents
from thoth.messaging.missing_version import MessageContents as MissingVersionContents

WORKDIR = "/mnt/workdir"

MESSAGE_LOCATION = "/mnt/workdir/message"
FAILED_STATUS_FILE = "/mnt/workdir/failed_status"

_LOGGER = logging.getLogger("thoth.download_package")
_LOGGER.info("Thoth workflow-helpers task: download_package v%s", __service_version__)

COMPONENT_NAME = "workflow_helper.download_py_package"


def download_py_package() -> None:
    """Download package which needs to be analyzed by future steps."""
    page = request.urlopen(os.path.join(Configuration.PACKAGE_INDEX, Configuration.PACKAGE_NAME))
    version_exists = False

    for link in BeautifulSoup(
        page, "html.parser", from_encoding=page.info().get_param("charset"), parse_only=SoupStrainer("a")
    ):
        if link.string.endswith(f"-{Configuration.PACKAGE_VERSION}.zip") or link.string.endswith(
            f"-{Configuration.PACKAGE_VERSION}.tar.gz"
        ):
            break

        elif f"-{Configuration.PACKAGE_VERSION}-" in link.string:
            version_exists = True

    else:
        if version_exists:
            _LOGGER.warning(
                f"version {Configuration.PACKAGE_VERSION}"
                f"for package {Configuration.PACKAGE_NAME}"
                f"from {Configuration.PACKAGE_INDEX} does not provide source distro."
            )
            message_contents = [
                {
                    "topic_name": update_provides_source_distro_message.base_name,
                    "message_contents": UpdateProvidesSrcDistroContents(
                        service_version=__service_version__,
                        component_name=COMPONENT_NAME,
                        package_name=Configuration.PACKAGE_NAME,
                        package_version=Configuration.PACKAGE_VERSION,
                        index_url=Configuration.PACKAGE_INDEX,
                        value=False,
                    ).dict(),
                }
            ]
            with open(MESSAGE_LOCATION, "w") as f:
                content = json.dumps(message_contents, indent=4)
                f.write(content)
            with open(FAILED_STATUS_FILE, "w") as f:
                f.write("1")

            return
        else:
            _LOGGER.warning(
                f"version {Configuration.PACKAGE_VERSION}"
                f"for package {Configuration.PACKAGE_NAME}"
                f"from {Configuration.PACKAGE_INDEX} is missing."
            )
            message_contents = [
                {
                    "topic_name": missing_version_message.base_name,
                    "message_contents": MissingVersionContents(
                        service_version=__service_version__,
                        component_name=COMPONENT_NAME,
                        package_name=Configuration.PACKAGE_NAME,
                        package_version=Configuration.PACKAGE_VERSION,
                        index_url=Configuration.PACKAGE_INDEX,
                    ).dict(),
                }
            ]
            with open(MESSAGE_LOCATION, "w") as f:
                content = json.dumps(message_contents, indent=4)
                f.write(content)
            with open(FAILED_STATUS_FILE, "w") as f:
                f.write("1")

            return

    with open(MESSAGE_LOCATION, "w") as f:
        f.write("")
    with open(FAILED_STATUS_FILE, "w") as f:
        f.write("0")

    command = (
        f"pip download --no-binary=:all: --no-deps -d {WORKDIR} -i {Configuration.PACKAGE_INDEX} "
        f"{Configuration.PACKAGE_NAME}==={Configuration.PACKAGE_VERSION}"
    )
    run_command(command)

    for file_ in os.listdir(WORKDIR):
        if file_.endswith(".tar.gz"):
            full_path = os.path.join(WORKDIR, file_)
            tar = tarfile.open(full_path, "r:gz")
            tar.extractall(os.path.join(WORKDIR, "package"))
            break
        elif file_.endswith(".zip"):
            full_path = os.path.join(WORKDIR, file_)
            with zipfile.ZipFile(os.path.join(WORKDIR, file_), "r") as zip_ref:
                zip_ref.extractall(os.path.join(WORKDIR, "package"))
            break
    else:
        raise FileNotFoundError(
            f"No source distribution found for {Configuration.PACKAGE_NAME}==={Configuration.PACKAGE_VERSION} on "
            f"index {Configuration.PACKAGE_INDEX}."
        )


if __name__ == "__main__":
    download_py_package()
