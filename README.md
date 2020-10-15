# workflow-helpers

This repo is used to collect all helpers that can be used across workflows. The collection of workflow helpers is triggered using
`THOTH_WORKFLOW_TASK` environment variable:

## download_py_package

```shell
REPO_PATH=. THOTH_WORKFLOW_TASK=download_package ./app.sh
```

uses `download_py_package.py` which is used in SI workflow to downalod a Python package from a certain index

## parse_solver_outputs

```shell
REPO_PATH=. THOTH_WORKFLOW_TASK=parse_solver_outputs ./app.sh
```

uses `parse_solver_outputs.py` which is used in Solver workflow to parse inputs and store messages file
that is used by Kafka task to send messages. Moreover it is used to check adviser run that have unresolved packages
and store messages file that is used by Kafka task to send messages.

## qeb_thamos_advise

```shell
REPO_PATH=. THOTH_WORKFLOW_TASK=qeb_hwt ./app.sh
```

will trigger `qeb_thamos_advise.py` which is used in Qeb-Hwt Outer workflow before calling submitting an advise.

## select_thoth_integration

```shell
REPO_PATH=. THOTH_WORKFLOW_TASK=trigger_integration ./app.sh
```

uses `select_thoth_integration.py` which is used in adviser workflow to trigger
the correct tasks depending on which Thoth integration requested adviser to run (CLI, Qeb-Hwt, S2I, etc.)

## parse_unresolved_packages.py

```shell
REPO_PATH=. THOTH_WORKFLOW_TASK=parse_unresolved_packages ./app.sh
```

It checks for any unresolved packages in the adviser report.
When the unresolved packages are present, it store messages to be sent for
an [UnresolvedPackageMessage](https://github.com/thoth-station/messaging/blob/a579a480819a9b35123e9002243f4bba6d082929/thoth/messaging/unresolved_package.py#L35),
so that these packages can be solved using Thoth [Solver](https://github.com/thoth-station/solver) workflow.
