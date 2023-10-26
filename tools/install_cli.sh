#!/bin/bash

# Get OS version 
os_name=$(cat /etc/os-release | grep "^ID_LIKE=" | cut -d "=" -f 2)

# If OS is debian-like (Debian or Ubuntu) then install venv
if [ $os_name == "debian" ]; then
    sudo apt install python3-venv
else 
    echo distribution not supported
    exit 1
fi

if [ ! -d "venv" ]; then
    python -m venv ./venv
fi

source ./venv/bin/activate

pip install build


wheel_name=$(python -m build | tail -n 1 | awk '{print $NF}')

if [ -f "dist/$wheel_name" ]; then
    pip install --force-reinstall "dist/$wheel_name"
else
    pip install "dist/$wheel_name"
fi
