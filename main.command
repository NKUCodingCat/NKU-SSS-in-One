#!/bin/bash -x 
if [ ! -w "$(cd "$(dirname "$0")"; pwd)"]; then 
	echo "Please run this command file in a directory which you have full write premission"
	exit
fi
source "$(cd "$(dirname "$0")"; pwd)/clean/bin/activate"
python "$(cd "$(dirname "$0")"; pwd)/prog/Launcher.py"
deactivate
exit
