Thoth's workflow-helpers
------------------------

Welcome to Thoth's workflow-helpers documentation

.. image:: https://img.shields.io/github/v/tag/thoth-station/workflow-helpers?style=plastic
  :target: https://github.com/thoth-station/workflow-helpers/tags
  :alt: GitHub tag (latest by date)

.. image:: https://quay.io/repository/thoth-station/workflow-helpers/status
  :target: https://quay.io/repository/thoth-station/workflow-helpers?tab=tags
  :alt: Quay - Build

This repo is used to collect all helpers that can be used across workflows. The collection of workflow helpers is triggered using `THOTH_WORKFLOW_TASK` environment variable:


.. list-table:: Thoth workflow helpers Tasks
   :widths: 25 25 50
   :header-rows: 1

   * - THOTH_WORKFLOW_TASK
     - Description
     - Command
   * - create_inspection_complete_message
     -  This task creates a message file to be used by messaging cli in a workflow.
     -  .. code:: bash

            REPO_PATH=. THOTH_WORKFLOW_TASK=create_inspection_complete_message ./app.sh

   * - create_purge_issues
     -  This task creates issues in repositories using Kebechet GitHub app when data purges occur.
     -  .. code:: bash

            REPO_PATH=. THOTH_WORKFLOW_TASK=create_purge_issues ./app.sh

   * - download_py_package
     -  This script run in a workflow task to download and extract python package for future steps.
     -  .. code:: bash

            REPO_PATH=. THOTH_WORKFLOW_TASK=download_package ./app.sh

   * - graph_schema_update
     -  This task is used to update the Graph schema for Thoth project.
     -  .. code:: bash

            REPO_PATH=. THOTH_WORKFLOW_TASK=graph_schema_update ./app.sh

   * - kebechet_administrator
     -  This script run in a workflow task to take an incoming message and decides which repositories Kebechet needs to be run on and store the necessary messages to be sent.
     -  .. code:: bash

            REPO_PATH=. THOTH_WORKFLOW_TASK=kebechet_administrator ./app.sh

   * - parse_solver_output
     -  This script run in a workflow task to parse solver output and produce inputs for Kafka message.
     -  .. code:: bash

            REPO_PATH=. THOTH_WORKFLOW_TASK=parse_solver_output ./app.sh

   * - parse_adviser_output
     -  This script run in adviser workflow task to parse adviser output.
     -  .. code:: bash

            REPO_PATH=. THOTH_WORKFLOW_TASK=parse_adviser_output ./app.sh

   * - parse_provenance_checker_output
     -  This script run in a workflow task to parse provenance checker output.
     -  .. code:: bash

            REPO_PATH=. THOTH_WORKFLOW_TASK=parse_provenance_checker_output ./app.sh

   * - thoth_repository_initialization
     -  This task creates demos a simple thoth-advise on a repository by forking the project and opening a PR.
     -  .. code:: bash

            REPO_PATH=. THOTH_WORKFLOW_TASK=thoth_repository_initialization ./app.sh

   * - trigger_integration
     -  This script run in a workflow task to select Thoth integration workflow to run.
     -  .. code:: bash

            REPO_PATH=. THOTH_WORKFLOW_TASK=trigger_integration ./app.sh

   * - update_kebechet_installation
     -  This task is run to update Kebechet installation details in DB during webhook workflows.
     -  .. code:: bash

            REPO_PATH=. THOTH_WORKFLOW_TASK=update_kebechet_installation ./app.sh
