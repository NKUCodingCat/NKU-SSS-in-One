#coding=utf-8
import FindChr
import numpy
import DiffMat
import os, zlib, base64, difflib, json, re

class Val_to_Str():
	def __init__(self, Fil = os.path.split(os.path.realpath(__file__))[0]+"/dump.txt"):
		self.DB = json.loads(open(Fil).read())
		for i in self.DB.keys():
			self.DB[i] = self.base64_zlib_json_load(self.DB[i])
		self.DB = reduce(lambda x, y:x.extend(y) or x, map(lambda x:map(lambda x, y:[x, y], [x[0], ]*len(x[1]), x[1]), self.DB.items()))
		self.DB_Matrix = map(lambda x: [x[0], numpy.array(map(lambda x: map(lambda x: int(x),list(x)), re.split('\/', x[1])))], self.DB)
		#print min([i[1].shape[0]*i[1].shape[1] for i in self.DB_Matrix])


	def base64_zlib_json_load(self, String):
		return json.loads(zlib.decompress(base64.b64decode(String)))
	
	def IM_to_Str(self, im):
		
		CHRS = FindChr.CutBox(im)
		RES = ""
		for i in CHRS:
			D = "/".join([("%s"*len(j))%tuple(j) for j in i])
			RES+=  max(map(lambda x,y: [y, difflib.SequenceMatcher(None, x, y[1]).ratio()], [D ,]*len(self.DB), self.DB), key = lambda x:x[1])[0][0]
		return RES

	def IM_to_Str_MatDiff(self, im):
		CHRS = FindChr.CutBox(im)
		RES = ""
		for i in CHRS:
			D = numpy.where(numpy.array(i) == 255, 1, 0)
			G = map(lambda x,y: [y, DiffMat.Diff_Matrix(x, y[1])], [D ,]*len(self.DB_Matrix), self.DB_Matrix)
			Q = sorted(G, key = lambda x:(x[1][0]+x[1][1]))[-1]
			RES += Q[0][0]
		return RES


if __name__ == '__main__':
	import requests
	from PIL import Image, ImageDraw, ImageFont
	import StringIO
	import time
	import re
	V = Val_to_Str()
	postdata = {
			"operation":"",
			"usercode_text":"4878481",
			"userpwd_text":"12214144",
			"checkcode_text":"",
			"submittype":"\xC8\xB7 \xC8\xCF"
		}
	F = 0
	SU = 3000
	i = 0
	while i < SU:
		try:
			i += 1
			G = requests.session()
			S = Image.open(StringIO.StringIO(G.get("http://222.30.32.10/ValidateCode", timeout = 3).content))
			STA = time.time()
			postdata["checkcode_text"] = V.IM_to_Str_MatDiff(S)
			print time.time()-STA, "\t%s/%s"%(i,SU), 
			if re.findall(u"正确的验证码".encode("GBK"), G.post("http://222.30.32.10/stdloginAction.do", data = postdata, timeout = 3).content):
				F += 1
				print False
			else:
				print True
		except KeyboardInterrupt:
			break
		except:
			raise
			print "Network Error"
	print u"错误%s/总计%s"%(F, SU)