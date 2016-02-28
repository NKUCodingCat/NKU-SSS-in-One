#!/bin/bash -x 
source "$(cd "$(dirname "$0")"; pwd)/clean/bin/activate"
python "$(cd "$(dirname "$0")"; pwd)/prog/Launcher.py"
deactivate
exit
