#!/bin/bash
echo "installing packages in venv:"
pip -V
source $PWD/venv/bin/activate
pip install $@
echo "saving to venv's requirements.txt:"
pip freeze > requirements.txt
deactivate
echo "deactivated venv - now using:"
pip -V