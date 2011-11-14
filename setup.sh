#!/bin/bash
set -o errexit
set -o nounset
set -o verbose

# Usage setup.sh [user-name] [password]

readonly DIR="$(readlink -f -- "$(dirname -- "${0}")")"
readonly PASSWORD="${2}"
readonly PYTHON='python2.7'
readonly USERNAME="${1}"
readonly WIKI='studact'

cd "${DIR}/lib"

svn checkout \
    http://svn.wikimedia.org/svnroot/pywikipedia/trunk/pywikipedia \
    pywikipedia

cd pywikipedia

${PYTHON} generate_family_file.py \
    http://elearn.cs.man.ac.uk/studact/index.php/Main_Page "${WIKI}"

expect -c "
    spawn ${PYTHON} generate_user_files.py
    expect \"What do you do? \"
    send \"1\\n\"
    expect -indices -re \"(\\\\d+): ${WIKI}\"
    expect -re \".*\\\\): \"
    send \"\$expect_out(1,string)\\n\"
    expect -re \".*: \"
    send \"\\n\"
    expect -re \".*: \"
    send \"${USERNAME}\\n\"
    expect -re \".*\? \"
    send \"E\\n\"
    expect eof"

expect -c "
    spawn ${PYTHON} login.py
    expect -re \".*: \"
    send \"${PASSWORD}\\n\"
    expect eof"

