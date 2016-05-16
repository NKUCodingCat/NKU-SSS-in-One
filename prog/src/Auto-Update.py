#coding=utf-8
import C
import os, md5, json, re, requests, copy, urllib
from functools import partial
import bar
import glob
import filecmp



def MD5_Info_for_dir(RootDir, Prefix, Excepts = []):
	Q = {}
	for i in os.walk(root):
		pa, fo, fi = i
		for i in fi:
			E = os.path.relpath(pa, root)
			if E in Excepts:
				continue
			E = E+"/" if E != "." else ""
			try:
				F = re.sub(r"\\",r"/", E+i)
				Q[unicode(Prefix+F.decode("GBK"))] = unicode(md5.new(open(root+"/"+F, "rb").read()).hexdigest())
			except:
				pass
	return Q

def Diff_Dict(Remote, Local):
	Remote = copy.deepcopy(Remote)
	Remote = dict(filter(lambda x: x[0][-1] != "/", Remote.items()))
	Local = copy.deepcopy(Local)
	Local = dict(filter(lambda x: x[0][-1] != "/", Local.items()))
	for i in Remote.keys():
		if i in Local.keys():
			if Remote[i] == Local[i]:
				del Remote[i]
				del Local[i]
	Local_Less = [i for i in Remote.keys() if i not in Local.keys()]
	Local_More = [i for i in Local.keys() if i not in Remote.keys()]
	Local_Diff = [i for i in Remote.keys() if i in Local.keys()]
	return Local_Less, Local_More, Local_Diff

def Del_Prefix(Array, Prefix):
	return map(lambda x:re.sub("^"+re.escape(Prefix), "", x), Array)

def Sync(Array, Word, Prefix, Func):
	if len(Array) != 0: 
		Array = Del_Prefix(Array, Prefix)
		print Word%len(Array)
		print "\n".join(Array)
		print "\nNeed to Sync (y = yes and Other=no) ?",
		Y = raw_input()
		if Y == "y":
			for i in Array:
				Func(i)

	
def File_Down(Path, NetBase, Root):
	print "Downloading %s ......"%Path
	Bar = bar.SimpleProgressBar()
	Local_File = Root+Path
	if not os.path.isdir(os.path.dirname(Local_File)):
		os.makedirs(os.path.dirname(Local_File))
	try:
		
		urllib.urlretrieve(NetBase%Path.encode('utf-8'), Local_File, reporthook=lambda x, y, z: Bar.update(x*y*100.0/z) if z>524288 else None)
		print "\n"

	except:
		#raise
		print u"Error Occured When Updating %s"%(Root+Path)
	

if __name__ == "__main__":
	root = os.path.split(os.path.realpath(__file__))[0]
	root = os.path.dirname(root)
	root = os.path.dirname(root)
	Prefix = "NKU-SSS-in-One-master/"
	print u"downloading MD5 Info ......."
	try:
		P = json.loads(json.loads(requests.get("https://python-nkusss.rhcloud.com/UPD-SSS-in-One", verify = False).content)[0][-1])
	except:
		#raise
		print u"Download MD5 Info from Remote Server Failed!"
	else:
		print u"Calculating MD5 Info for all Files "
		print glob.glob(root+"/prog/logs/*")
		Q = MD5_Info_for_dir(root, Prefix, map(lambda x:os.path.relpath(x, root), glob.glob(root+"/prog/logs/*")))
		L, M, D = Diff_Dict(P, Q)
		print u"\n=========================="
		Update  = partial(File_Down, NetBase = "https://python-nkusss.rhcloud.com/data/ext/NKU-SSS-in-One-master/%s", Root = root+"/")
		Sync(L, "==========================\nThere %s files not found in Local", Prefix, Update)
		Sync(M, "==========================\nThere %s files not found in Remote", Prefix, lambda x:os.remove(root+"/"+x))
		Sync(D, "==========================\nThere %s files not same as the file in Local", Prefix, Update)
	print "Update Complete,Please Restart The Program, Thank you"
	raw_input("Press Enter to exit")
