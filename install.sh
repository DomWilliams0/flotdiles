#!/bin/bash

set -e

SRC_DIR="/usr/local/share"
BIN_DIR="/usr/local/bin"
PROJECT_NAME="flotdiles"
GIT_URL="https://github.com/DomWilliams0/$PROJECT_NAME"
SCRIPT_PATH="$SRC_DIR/$PROJECT_NAME/$PROJECT_NAME.py"
BIN=${BIN_DIR}/${PROJECT_NAME}
SRC=${SRC_DIR}/${PROJECT_NAME}

function show_help() {
        echo To uninstall, use \"$0 uninstall\"
        echo To view this help, use \"$0 \<anything else\>
        echo To install, use \"$0\" with no parameters
        exit 0
}

# must be root
if [ "$(id -u)" != "0" ]; then
    echo "Only root can (un)install $PROJECT_NAME"
    exit 1
fi

# uninstall
if [ "$#" -eq "1" ]; then
    if [ "$1" = "uninstall" ]; then
        echo Deleting symbolic link \(${BIN}\)
        rm -f ${BIN}

        echo Deleting source from ${SRC}
        rm -rf ${SRC}

        exit 0
    else
        show_help
    fi

elif [ "$#" -ne "0" ]; then
    show_help
fi

# project already cloned; delete
if [ -d ${SRC} ]; then
    echo Deleting current version from ${SRC}
    rm -rf ${SRC}
fi

# link already exists; delete
if [ -h ${BIN} ]; then
    echo Deleting old symbolic link \(${BIN}\)
    rm -f ${BIN}
fi

git clone ${GIT_URL} ${SRC}

echo Making executable...
chmod +x ${SCRIPT_PATH}

echo Creating symlink to executable in ${BIN_DIR}
ln -s ${SCRIPT_PATH} ${BIN}

echo Successfully installed ${PROJECT_NAME} to ${BIN_DIR}
echo You should probably \"${PROJECT_NAME} sync --pull\" and \"${PROJECT_NAME} verify\" now