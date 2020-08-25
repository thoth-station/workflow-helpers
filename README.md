# workflow-helpers

This repo is used to collect all helpers that can be used across workflows. The collection of workflow helpers is triggered using
`THOTH_WORKFLOW_TASK` environment variable:

```shell
REPO_PATH=. THOTH_WORKFLOW_TASK=qeb_hwt ./app.sh
```

will `trigger qeb_thamos_advise.py` which is used in Qeb-Hwt Outer workflow before calling submitting an advise.

```shell
REPO_PATH=. THOTH_WORKFLOW_TASK=trigger_integration ./app.sh
```

uses `select_thoth_integration.py` which is used in adviser workflow to trigger
the correct tasks depending on which Thoth integration requested adviser to run (CLI, Qeb-Hwt, S2I, etc.)
