#! /usr/bin/env bash

VENV_PATH="${1:-venv}"

function create_env {
    if ! python3 -m venv "${VENV_PATH}" --prompt venv; then
        return 1
    fi
    . ${VENV_PATH}/bin/activate
    pip install -r requirements.txt
}


if [[ ! -e "${VENV_PATH}" ]] ; then
    echo "Creating new venv '${VENV_PATH}'"
    if ! { create_env ; } ; then
        echo "Failed to create environment"
        deactivate
        # venv is safe to delete because this script has created it
        rm -rf ${VENV_PATH}
    fi
else
    echo "Reusing existing venv '${VENV_PATH}'"
    # Do not remove venv on error because then the user risks losing data
    . ${VENV_PATH}/bin/activate
fi

test ! -z "${VIRTUAL_ENV}"
