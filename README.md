# workflow-helpers

This repo is used to collect all helpers that can be used across workflows. The collection of workflow helpers is triggered using
`THOTH_WORKFLOW_TASK` environment variable:

## download_py_package

```shell
REPO_PATH=. THOTH_WORKFLOW_TASK=download_package ./app.sh
```

uses `download_py_package.py` which is used in SI workflow to downalod a Python package from a certain index

## parse_solver_inputs

```shell
REPO_PATH=. THOTH_WORKFLOW_TASK=parse_solver_inputs ./app.sh
```

uses `parse_solver_inputs.py` which is used in Solver workflow to parse inputs and store messages file
that is used by Kafka task to send messages

## parse_solved_package

```shell
REPO_PATH=. THOTH_WORKFLOW_TASK=parse_solved_package ./app.sh
```

uses `parse_solved_package.py` which is used in Solver workflow to check adviser run that have unresolved packages
and store messages file that is used by Kafka task to send messages

## qeb_thamos_advise

```shell
REPO_PATH=. THOTH_WORKFLOW_TASK=qeb_hwt ./app.sh
```

will `trigger qeb_thamos_advise.py` which is used in Qeb-Hwt Outer workflow before calling submitting an advise.

## select_thoth_integration

```shell
REPO_PATH=. THOTH_WORKFLOW_TASK=trigger_integration ./app.sh
```

uses `select_thoth_integration.py` which is used in adviser workflow to trigger
the correct tasks depending on which Thoth integration requested adviser to run (CLI, Qeb-Hwt, S2I, etc.)
