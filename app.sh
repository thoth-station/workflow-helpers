#!/usr/bin/env sh
#
# This script is run by OpenShift's s2i. Here we guarantee that we run desired
# command
#

set -o nounset
set -o errexit
set -o errtrace
set -o pipefail
trap 'echo "Aborting due to errexit on line $LINENO. Exit code: $?" >&2' ERR

THOTH_WORKFLOW_TASK=${THOTH_WORKFLOW_TASK:?'THOTH_WORKFLOW_TASK is not selected!'}

if [ "$THOTH_WORKFLOW_TASK" = "trigger_integration" ]; then
    exec python3 select_thoth_integration.py
elif [ "$THOTH_WORKFLOW_TASK" = "qeb_hwt" ]; then
    exec python3 qeb_thamos_advise.py
elif [ "$THOTH_WORKFLOW_TASK" = "download_package" ]; then
    exec python3 download_py_package.py
elif [ "$THOTH_WORKFLOW_TASK" = "parse_solver_inputs" ]; then
    exec python3 parse_solver_inputs.py
fi
