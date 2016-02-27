import sys
import os
import glob
import sysconfig
import re

reload(sys).setdefaultencoding('UTF-8')
sys.dont_write_bytecode = True

sys.path = [i for i in sys.path if not re.findall("lib-tk", i)]

sys.path += glob.glob('%s/*.egg' % os.path.dirname(os.path.abspath(__file__)))
sys.path += [os.path.abspath(os.path.join(__file__, '../packages.egg/%s' % x)) for x in ('noarch', sysconfig.get_platform().split('-')[0])]
sys.path  = [(os.path.join(__file__, "../packages.egg/noarch/lib-tk/")), ]+sys.path
sys.path += glob.glob('%s/*.zip' % os.path.dirname(os.path.abspath(__file__)))
sys.path += glob.glob('%s/*.zip/*/' % os.path.dirname(os.path.abspath(__file__)))
sys.path += glob.glob('%s/*' % os.path.dirname(os.path.abspath(__file__)))
sys.path += [os.path.dirname(os.path.abspath(__file__)), ]
# print sys.path