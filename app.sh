#!/usr/bin/env sh
#
# This script is run by OpenShift's s2i. Here we guarantee that we run desired
# command and debug level
#

if [ "$THOTH_WORKFLOW_TASK" = "trigger_integration" ]
then
    exec python3 select_thoth_integration.py
elif [ "$THOTH_WORKFLOW_TASK" = "qeb_hwt" ]
then
    exec python3 qeb_thamos_advise.py
fi
