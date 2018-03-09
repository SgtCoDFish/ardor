#!/bin/bash
set -eu -o pipefail

echo "Setting up ARDOR. This may take a short while."

(which python3 &> /dev/null) || (echo -e "\033[0;31mERROR:\033[0m python3 not found.\nOn Linux: Install using your system package manager - e.g. sudo apt install python3\nOn macOS: Install homebrew if you don't have it, and install python through homebrew" && exit 1)

python3 -m venv venv &> /dev/null
./venv/bin/python -m pip install --upgrade pip setuptools wheel &> /dev/null
./venv/bin/python -m pip install numpy &> /dev/null
./venv/bin/python -m pip install tdl tabulate typing &> /dev/null

echo -e "\033[0;32mSUCCESS:\033[0m You can now run ARDOR with ./run.sh"
