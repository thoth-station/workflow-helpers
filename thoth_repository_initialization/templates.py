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

"""This is a file that just contains templates for PRs and issues opened by this task."""

footer = """### For more information

https://thoth-station.ninja/

### To open a support issue

https://github.com/thoth-station/support/issues/new/choose

### To install our GitHub App

https://github.com/marketplace/khebhut
"""

failed_issue_body = (
    """## Sorry from the Thoth team
Thank you for your interest in the Thoth project, at this time we were not able to offer advice
on your software stack. This may be due to a service outage or lack of data. We strive to be able to service more users
everyday. You may have more luck on another project, we primarily focus on injesting popular packages in the datascience
domain.

"""
    + footer
)

thoth_demo_body = (
    """## Hello! from the Thoth team
Thank you for your interest in the Thoth project. This is an example of the service that we provide. We run benchmarks
and other metrics on Python packages trying to provide you with the best software stack we can. If you install Kebechet
on your repository Thoth will take care of dependencies so you can just get to coding.

"""
    + footer
)

run_on_fork_issue = (
    """## Sorry from the Thoth team
This demo cannot be run on forked repositories.

"""
    + footer
)
