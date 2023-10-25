#!/bin/bash

if [ ! -d "venv" ]; then
    python -m venv ./venv
fi

source ./venv/bin/activate

pip install build

# Last line of build contains path of wheel as last word (5th field)
# wheel_name=$(python -m build | tail -n 1 | cut --delimiter=" " -f 5)
wheel_name=$(python -m build | tail -n 1 | awk '{print $NF}')

if [ -f "dist/$wheel_name" ]; then
    pip install --force-reinstall "dist/$wheel_name"
else
    pip install "dist/$wheel_name"
fi
