#!/bin/bash
set -eu -o pipefail

PACKAGES="python3 python3-pip python3-venv libsdl2-dev python3-sdl2"

echo "Setting up ARDOR. This may take a short while."

(which python3 &> /dev/null) || (echo -e "\033[0;31mERROR:\033[0m python3 not found.\nInstall it through your package manager: sudo apt install python3" && exit 1)

python3 -m venv venv &> /dev/null
./venv/bin/python -m pip install --upgrade pip setuptools wheel || (echo -e "\033[0;31mERROR:\033[0m Failed to install dependencies" && exit 1)

./venv/bin/python -m pip install numpy
./venv/bin/python -m pip install tdl tabulate typing

echo -e "\n\n\033[0;32mSUCCESS:\033[0m You can now run ARDOR with ./run.sh"
