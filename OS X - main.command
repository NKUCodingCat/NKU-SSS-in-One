/usr/bin/env python2.6 -x "$0" ;exit
#coding:utf-8
import os, sys
from subprocess import call
root = os.path.split(os.path.realpath(__file__))[0]
print root
for pycmd in ('python2.7', 'python2', 'python'):
	if os.system('which %s' % pycmd) == 0:
		cmd = "/usr/bin/env %s '%s/prog/Launcher.py'" % (pycmd, root)
		break
try:
	retcode = call(cmd, shell=True)
	if retcode < 0:
		print >>sys.stderr, "Child was terminated by signal", -retcode
	else:
		print >>sys.stderr, "Child returned", retcode
except OSError as e:
	print >>sys.stderr, "Execution failed:", e
