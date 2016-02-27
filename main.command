#!/bin/bash -x 
source $(dirname ${0})/clean/bin/activate
python $(dirname ${0})/prog/Launcher.py
deactivate
exit
