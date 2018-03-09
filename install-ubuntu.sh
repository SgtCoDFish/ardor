#!/bin/bash
set -eu -o pipefail

PACKAGES="python3 python3-pip python3-venv libsdl2-dev python3-sdl2"

echo "Setting up ARDOR. This may take a short while."

(dpkg -l | grep python3 &> /dev/null) || (echo -e "\033[0;31mERROR:\033[0m python3 not found.\nInstall using your system package manager - e.g. sudo apt-get install $PACKAGES" && exit 1)
(dpkg -l | grep python3-pip &> /dev/null) || (echo -e "\033[0;31mERROR:\033[0m python3-pip not found.\nInstall using your system package manager - e.g. sudo apt-get install $PACKAGES" && exit 1)
(dpkg -l | grep python3-venv &> /dev/null) || (echo -e "\033[0;31mERROR:\033[0m python3-venv not found.\nInstall using your system package manager - e.g. sudo apt-get install $PACKAGES" && exit 1)
(dpkg -l | grep libsdl2-dev &> /dev/null) || (echo -e "\033[0;31mERROR:\033[0m libsdl2-dev not found.\nInstall using your system package manager - e.g. sudo apt-get install $PACKAGES" && exit 1)
(dpkg -l | grep python3-sdl2 &> /dev/null) || (echo -e "\033[0;31mERROR:\033[0m python3-sdl2 not found.\nInstall using your system package manager - e.g. sudo apt-get install $PACKAGES" && exit 1)

python3 -m venv venv &> /dev/null
./venv/bin/python -m pip install --upgrade pip setuptools wheel || (echo -e "\033[0;31mERROR:\033[0m Failed to install dependencies" && exit 1)

./venv/bin/python -m pip install numpy
./venv/bin/python -m pip install tdl tabulate typing

echo -e "\n\n\033[0;32mSUCCESS:\033[0m You can now run ARDOR with ./run.sh"
