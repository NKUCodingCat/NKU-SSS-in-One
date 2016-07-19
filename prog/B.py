import sys
import os
import glob
import sysconfig
import re
import __builtin__

#  =================  
import datetime
import time
import functools

class IO_Logger(object):
    def __init__(self, stream, *other_streams):
        self.stream = stream
        self.others = other_streams
        for j in self.others:
            j.write("==============Log record begin @ %s with function %s===============\n"%(time.ctime(), self.stream.__repr__()))
        for i in dir(stream):
            if i[0:2] != "__" and i not in dir(self):
                setattr(self, i, getattr(stream, i))

        self.Wrapper = {
            "write"     : self.F1,
            "read"      : self.F2,
            "writelines": self.F1,
            "readlines" : self.F2
        }
        map(lambda item: setattr(self, item[0], functools.partial(item[1], item[0])), self.Wrapper.items())

        if stream != raw_input:
            self.__call__ = None

    def __call__(self, *args, **kwarg): # Patch for raw_input
        return functools.partial(self.F3, __builtin__.raw_input)(*args, **kwarg)

    def F1(self, func, data):
        for i in self.others:
            getattr(i, func)(data)
            i.flush()
        getattr(self.stream, func)(data)



    def F2(self, func, data):
        new_func = re.sub("read", "write", func)
        for i in self.others:
            getattr(i, new_func)(data)
            i.flush()
        getattr(self.stream, func)(data)

    
    def F3(self, func, *args, **kwargs):
        Tmp = func(*args, **kwargs)
        for i in self.others:
            i.write(Tmp+"\n")
            i.flush()
        return Tmp



def Patch_all_IOs(Log_file_name = None):
    global raw_input
    Root = os.path.abspath(os.path.split(os.path.realpath(__file__))[0]+"/")
    LogRoot = Root+"/logs/"
    os.mkdir(LogRoot) if not os.path.exists(LogRoot) else None
    H = open("%s/%s.log"%(LogRoot, Log_file_name or (datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d_%H-%M-%S"))), "w")
    sys.stdin = IO_Logger(sys.stdin, H)
    sys.stdout = IO_Logger(sys.stdout, H)
    sys.stderr = IO_Logger(sys.stderr, H)
    raw_input = IO_Logger(raw_input, H)

#  =================

if type(sys.stdout) != IO_Logger and sys.argv[0]:
    Patch_all_IOs("%s__%s"%(datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d_%H-%M-%S"), os.path.basename(sys.argv[0])))

try:
    sys.setdefaultencoding('UTF-8')
except AttributeError :
    i, o, e = sys.stdin, sys.stdout, sys.stderr
    r = __builtin__.raw_input
    reload(sys).setdefaultencoding('UTF-8')
    sys.stdin, sys.stdout, sys.stderr = i, o, e
    __builtin__.raw_input = r
    del(i)
    del(o)
    del(e)
    del(r)
    

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