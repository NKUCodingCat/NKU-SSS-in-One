import C
import os, md5, json, re, requests, copy, urllib, locale, traceback
DEF_LANG, DEF_ENCODING = locale.getdefaultlocale()
from functools import partial
import bar
import glob
import filecmp



def MD5_Info_for_dir(RootDir, Prefix, Excepts = []):
	Q = {}
	for j in os.walk(root):
		pa, fo, fi = j
		for i in fi:
			E = os.path.relpath(pa, root)
			F = os.path.realpath(pa + os.sep + i)
			if F in Excepts:
				continue
			E = E+"/" if E != "." else ""
			try:
				F = re.sub(r"\\",r"/", E+i)
				Q[unicode(Prefix+F.decode(DEF_ENCODING))] = unicode(md5.new(open(root+"/"+F, "rb").read()).hexdigest())
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
	Local_File = Root+Path.decode(DEF_ENCODING)
	if not os.path.isdir(os.path.dirname(Local_File)):
		os.makedirs(os.path.dirname(Local_File))
	try:
		
		urllib.urlretrieve(NetBase%Path.encode('utf-8'), Local_File, reporthook=lambda x, y, z: Bar.update(x*y*100.0/z) if z>524288 else None)
		print "\n"

	except:
		#raise
		print u"Error Occured When Updating %s"%(Root+Path)
		traceback.print_exc()
	

if __name__ == "__main__":
	root = os.path.split(os.path.realpath(__file__))[0]
	root = os.path.dirname(root)
	root = os.path.dirname(root)
	Prefix = "NKU-SSS-in-One-master/"
	Exps = map(os.path.realpath, glob.glob(root+"/prog/logs/*"))
	
	print """\n=========================================\nGenerally speaking, there is no need for system administrator privileges when you are using this upgrading tools.\n\nBut if you get some error you cannot understand, try to\n\n        right-click main.exe and select "run with administrator privileges"(in Windows NT) \n     or "sudo bash <path/to/main.sh>/main.sh"(in *nix) \n=========================================\n"""
	raw_input("Press Enter to continue")
	
	print u"downloading MD5 Info ......."
	try:
		P = json.loads(json.loads(requests.get("https://python-nkusss.rhcloud.com/UPD-SSS-in-One", verify = False).content)[0][-1])
	except:
		print u"Download MD5 Info from Remote Server Failed!"
	else:
		print u"Calculating MD5 Info for all Files "
		
		Q = MD5_Info_for_dir(root, Prefix, Exps)
		L, M, D = Diff_Dict(P, Q)
		print u"\n=========================="
		Update  = partial(File_Down, NetBase = "https://python-nkusss.rhcloud.com/data/ext/NKU-SSS-in-One-master/%s", Root = root+"/")
		Sync(L, "==========================\nThere %s files not found in Local", Prefix, Update)
		Sync(M, "==========================\nThere %s files not found in Remote", Prefix, lambda x:os.remove(root+"/"+x.encode(DEF_ENCODING)))
		Sync(D, "==========================\nThere %s files not same as the file in Local", Prefix, Update)
	print "Update Complete,Please Restart The Program, Thank you"
	raw_input("Press Enter to exit")
