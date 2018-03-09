#!/bin/bash
set -eu -o pipefail

echo "Setting up ARDOR. This may take a short while."

(which python3 &> /dev/null) || (echo -e "\033[0;31mERROR:\033[0m python3 not found.\nInstall homebrew if you don't have it, and install python through homebrew using brew install python3" && exit 1)

python3 -m venv venv &> /dev/null
./venv/bin/python -m pip install --upgrade pip setuptools wheel &> /dev/null
./venv/bin/python -m pip install numpy &> /dev/null
./venv/bin/python -m pip install tdl tabulate typing &> /dev/null

echo -e "\033[0;32mSUCCESS:\033[0m You can now run ARDOR with ./run.sh"
