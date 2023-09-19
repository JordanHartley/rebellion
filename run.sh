#!/bin/bash
source "$PWD/venv/bin/activate"
python . $@
deactivate
echo "deactivated venv - now using:"
pip -V