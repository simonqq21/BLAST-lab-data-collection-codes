#!/bin/bash
app_path=$(dirname $(realpath "$0"))
source $app_path/venv/bin/activate
sudo python3 $app_path/startup.py
exit
