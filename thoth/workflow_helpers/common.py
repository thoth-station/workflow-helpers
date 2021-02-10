#!/usr/bin/env python3
# thoth-workflow-helpers
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

"""Common methods for all workflow helpers."""

import logging
import json
import os

from prometheus_client import Metric, Gauge, Counter, CollectorRegistry, push_to_gateway
from thoth.storages import GraphDatabase
from thoth.workflow_helpers.configuration import Configuration

_LOGGER = logging.getLogger(__name__)

PROMETHEUS_REGISTRY = CollectorRegistry()

PUSHGATEWAY_URL = Configuration.THOTH_METRICS_PUSHGATEWAY_URL
DEPLOYMENT_NAME = Configuration.THOTH_DEPLOYMENT_NAME

MSG_OUT_FILE = "/mnt/workdir/messages_to_be_sent.json"

database_schema_revision_script = Gauge(
    "thoth_database_schema_revision_script",
    "Thoth database schema revision from script",
    ["component", "revision", "env"],
    registry=PROMETHEUS_REGISTRY,
)


def parametrize_metric_messages_sent(component_name: str, description: str):
    """Parametrize metric for number of messages to be sent."""
    metric_messages_sent = Counter(
        f"thoth_{component_name}_messages_sent",
        description,
        ["message_type", "env", "version"],
        registry=PROMETHEUS_REGISTRY,
    )

    return metric_messages_sent


def retrieve_solver_document(document_path: str):
    """Retrieve solver document."""
    _LOGGER.info("Loading document from a local file: %r", document_path)
    with open(document_path, "r") as document_file:
        solver_document = json.loads(document_file.read())

    return solver_document


def store_messages(output_messages: list):
    """Store messages."""
    # Store message to file that need to be sent.
    try:
        with open(MSG_OUT_FILE, "r") as json_file:
            if os.stat(MSG_OUT_FILE).st_size != 0:
                all_messages: list = json.load(json_file)
                if type(all_messages) != list:
                    raise TypeError(f"Message file must be a list of messages. Got type {type(all_messages)}")
                all_messages = all_messages + output_messages
    except Exception as e:
        _LOGGER.exception(e)
        all_messages = output_messages

    with open(MSG_OUT_FILE, "w") as json_file:
        json.dump(all_messages, json_file)

    if output_messages:
        _LOGGER.info(f"Successfully stored file with messages to be sent!: {output_messages}")


def set_metrics(
    metric_messages_sent: Metric,
    message_type: str,
    service_version: str,
    number_messages_sent: int,
    is_storages_used: bool = True,
):
    """Set metrics to be sent to pushgateway."""
    if DEPLOYMENT_NAME:
        if is_storages_used:
            database_schema_revision_script.labels(
                "workflow-helpers", GraphDatabase().get_script_alembic_version_head(), DEPLOYMENT_NAME
            ).inc()

        metric_messages_sent.labels(
            message_type=message_type,
            env=DEPLOYMENT_NAME,
            version=service_version,
        ).inc(number_messages_sent)

    else:
        _LOGGER.warning("THOTH_DEPLOYMENT_NAME env variable is not set.")


def send_metrics():
    """Send metrics to pushgateway."""
    component_name = "workflow-helpers"
    if PUSHGATEWAY_URL and DEPLOYMENT_NAME:
        try:
            _LOGGER.debug(f"Submitting metrics to Prometheus pushgateway {PUSHGATEWAY_URL}")
            push_to_gateway(
                PUSHGATEWAY_URL,
                job=component_name,
                registry=PROMETHEUS_REGISTRY,
            )
        except Exception as e:
            _LOGGER.exception(f"An error occurred pushing the metrics: {str(e)}")

    else:
        _LOGGER.warning("PROMETHEUS_PUSHGATEWAY_URL env variable is not set.")
