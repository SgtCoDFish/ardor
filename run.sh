#!/bin/bash
set -eu -o pipefail

(test -d venv/bin &> /dev/null) || (echo -e "\033[0;31mERROR:\033[0m You must run ./install-macos.sh or ./install-ubuntu.sh first" && exit 1)

./venv/bin/python ardor.py
