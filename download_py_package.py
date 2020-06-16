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

"""This script run in a workflow task to download and extract python package for future steps."""

from thoth.analyzer import run_command
from thoth.workflow_helpers.configuration import Configuration
import tarfile
import zipfile
import os

WORKDIR = "/mnt/workdir"

def download_py_package():
    command = (
        f"pip download --no-binary=:all: --no-deps -d {WORKDIR} -i {Configuration._PACKAGE_INDEX} "
        f"{Configuration._PACKAGE_NAME}==={Configuration._PACKAGE_VERSION}"
    )

    run_command(command)

    for f in os.listdir(WORKDIR):
        if f.endswith(".tar.gz"):
            full_path = os.path.join(WORKDIR, f)
            tar = tarfile.open(full_path, "r:gz")
            tar.extractall(os.path.join(d, "package"))
        elif f.endswith(".zip"):
            full_path = os.path.join(WORKDIR, f)
            with zipfile.ZipFile(os.path.join(WORKDIR, f), 'r') as zip_ref:
                zip_ref.extractall(os.path.join(WORKDIR, "package"))
    else:
        raise FileNotFoundError(
            f"No source distribution found for {Configuration._PACKAGE_NAME}==={Configuration._PACKAGE_VERSION} on "
            f"index {Configuration._PACKAGE_INDEX}."
        )

if __name__ == "__main__":
    download_py_package()
