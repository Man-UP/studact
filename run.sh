#!/bin/bash
set -o errexit
set -o nounset

readonly DIR="$(readlink -f -- "$(dirname -- "${0}")")"
readonly PYTHON='python2.7'

export PYTHONPATH="${PYTHONPATH}:${DIR}/lib/pywikipedia"

${PYTHON} "${DIR}/studact.py" "${@}"

