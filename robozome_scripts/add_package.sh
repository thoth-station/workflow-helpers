set -o allexport -o pipefail -ex

# Pre-condition:
# - Create the config file at location ${PAYLOAD_PATH}
# - Clone the github.com/operate-first/apps repo at location ${WORKING_DIR}
# - Working branch should be clean, checked out of upstream default branch.
# - Set Environment variables: ORG_NAME (=thoth-station), SOURCE_REPO (=support), ISSUE_NUMBER
#
# If you want to run this script locally, you can set the following environment variables:
# - create a data.yaml file in the root of the repo
# - ISSUE_NUMBER=123 ./add_package.sh

# get config from environment or default to data.yaml
CONFIG=${PAYLOAD_PATH:-data.yaml}
if [ -z "$WORKING_DIR" ]; then
    REPO=$(pwd)
else
    REPO=${WORKING_DIR}/apps
fi
ORG_NAME=${ORG_NAME:-thoth-station}
SOURCE_REPO=${SOURCE_REPO:-support}
if [ -z "$ISSUE_NUMBER" ]; then
    echo "ISSUE_NUMBER is not set"
    exit 1
fi

# Unpack Config file, we will need these environment variables for the remainder of the steps
PYTHON_PACKAGE_NAME=$(yq e .package_name ${CONFIG})
PYTHON_INDEX_URL=$(yq e .index_url ${CONFIG})
REASON=$(yq e .reason ${CONFIG})

echo "I started ingesting ${PYTHON_PACKAGE_NAME}..." >feedback.txt

set -o allexport
