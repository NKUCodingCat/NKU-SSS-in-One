#coding=utf-8

import B
import os, sys
import json
import re
import subprocess
import time
import datetime

Root = os.path.abspath(os.path.split(os.path.realpath(__file__))[0]+"/")
LogRoot = Root+"/logs/"
print os.path.exists(LogRoot)
CFG = json.loads(open(Root+"/LauncherConfig.json","r").read())


def Start(Prog):
	
	try:
		FilePath = Root+Prog["file"]
		StartPath = Root+"/python27.exe"
	except UnicodeDecodeError:
		FilePath = (Root.decode("GBK")+Prog["file"]).encode("GBK")
		StartPath = (Root.decode("GBK")+"/python27.exe").encode("GBK")
	FilePath = os.path.abspath(FilePath)
	StartPath = os.path.abspath(StartPath)
	if not os.path.isfile(FilePath):
		print FilePath
		print u"该程序文件不存在，请按Enter退出"
		raw_input()
		return 
	print u"启动中。。。。。。。"
	if not (getattr(sys, "getwindowsversion", None)):
		#not a windows
		#print FilePath
		os.system("%s \"%s\""%("python", FilePath))
	
	else:
		#on windows
		subprocess.call("\"%s\" \"%s\""%(StartPath, FilePath))
		
def choo():
	a = 0
	print u"""
	
请注意：如果重启程序多次仍然发现有奇怪的问题，请先尝试运行自动更新升级到最新版再试一次，么么哒

如果不能更新，请尝试着下载最新版喵~在下面可以选择下载最新版~

有任何奇怪的问题的话请发邮件到nankai.codingcat@outlook.com并且附上prog文件夹中logs下最新的log文件，如有可能截图请一起提供截图~~
		
		——也爱你们的喵
	
	"""
	for i in CFG["prog"]:
		a += 1
		print "  %s - %s"%(a, i["name"])
	print u"请输入所需要的软件并按Enter：",
	In = raw_input()
	try:
		Start(CFG["prog"][int(In)-1])
	except IndexError:
		#raise
		print u"输入错误, 请按Enter退出"
		raw_input()
	except :
		print u"有错误发生, 按enter退出"
		raw_input()

class Unbuffered(object):
	def __init__(self, stream, *other_streams):
		self.stream = stream
		self.others = other_streams
		for j in self.others:
			j.write("==============Log record begin @ %s==============="%time.ctime())

	def write(self, data):
		self.stream.write(data)
		self.stream.flush()
		for i in self.others:
			i.write(data)
			i.flush()




		
if __name__ == "__main__":
	try:
		H = open("%s/%s.log"%(LogRoot, datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d_%H-%M-%S")), "w")
		sys.stdout = Unbuffered(sys.stdout, H)
		choo()
	except:
		traceback.print_exc() 
	finally:
		H.close()
	

	
