#coding=utf-8
import C
import requests
import StringIO
import re
import base64
import sys
import sys, traceback
from lxml import etree


import binascii

class PJ():
	def __init__(self):
		self.white = 'iVBORw0KGgoAAAANSUhEUgAAAJYAAAAZCAIAAABchUC4AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3wYdAgYerV4wMwAAAD9JREFUaN7t0QENAAAIwzDAv+ejg9BJWDtJ6XJjAUIhFEKEQiiEQohQCIVQCBEKoRAKIUIhFEIhRCiEQiiEL1sX+wMvfsLvYwAAAABJRU5ErkJggg=='
		self.RefreshAll()
		self.pwdenc = RSA_password()

	def Login(self, usr, pwd, vcode):
		pwd = self.pwdenc.RSA(pwd)
		postdata = {
			"operation":"",
			"usercode_text":usr,
			"userpwd_text":pwd,
			"checkcode_text":vcode,
			"submittype":"\xC8\xB7 \xC8\xCF"
		}
		try:
			content = self.Session.post("http://222.30.32.10/stdloginAction.do", data = postdata).content.decode("gb2312")
		except Exception,e: 
			traceback.print_exc() 
			return {"Err":True, "Val":"NetWork Error!"}
		if content.find("stdtop") != -1:
			return {"Err":False, "Val":"Login Success"}
		elif (content.find(u"请输入正确的验证码") != -1):
			return {"Err":True, "Val":"Validate Code Error, Refresh the Validate Code and Retry"}
		elif (content.find(u"用户不存在或密码错误") != -1):
			return {"Err":True, "Val":"User Name or Password Error!"}
		elif (content.find(u"忙") != -1 or content.find(u"负载") != -1):
			return {"Err":True, "Val":"System Busy!"}
		else:
			return {"Err":True, "Val":"UnknownError!"}
	
	def GetVcode(self):
		Q = self.Session.get("http://222.30.32.10/ValidateCode")
		if Q.status_code != 200:
			return None
		else:
			return StringIO.StringIO(Q.content)

	
	def RefreshAll(self):
		print "Refreshed"
		self.Session = requests.session()
		#self.Session.proxies = {"http":"127.0.0.1:8888"}
		self.vcode = StringIO.StringIO(base64.b64decode(self.white))
		self.NetWork = False
		try:
			self.Session.get("http://222.30.32.10")
			M = self.GetVcode()
			if M:
				self.vcode = M
				self.NetWork = True
			else:
				pass		
		except:
			pass
	
	def PJ(self, func = (lambda obj:sys.stdout.write(obj+'\n') )):
		try:
			G = self.Session.get("http://222.30.32.10/evaluate/stdevatea/queryCourseAction.do")
		except :
			return {"Err":True, "Val":"NetWork Error!"}
		if G.url == "http://222.30.32.10/stdlogin.jsp":
			return {"Err":True, "Val":"Please Login First!"}
		else:
			try:
				num=int(re.findall(u"共 ([0-9]*) 项", G.content.decode("gb2312"))[0])
			except:
				return {"Err":True, "Val":"Remote Server does not work as expected."}
			failcount=0
			for i in range(num):
				Add = "http://222.30.32.10/evaluate/stdevatea/queryTargetAction.do?operation=target&index=%s"%str(i)
				D = self.Session.get(Add).content.decode("gb2312")
				D = D.replace(u"该教师给你的总体印象",u"该教师给你的总体印象（10）")
				item=re.findall(u"（([0-9]*)）", D)
				params="operation=Store"
				for j in range(len(item)):  
					params+=("&array["+str(j)+"]="+item[j])
				params+="&opinion="
				#print params
				E = self.Session.post("http://222.30.32.10/evaluate/stdevatea/queryTargetAction.do", headers = {"Referer":Add, "Content-Type": "application/x-www-form-urlencoded"}, data = params).content.decode("gb2312")
				if not re.findall(u"成功保存", E):
					failcount += 1
				func(u"评价第%s门课完成， 状态：%s"%(i+1, u"成功" if not re.findall("成功保存", E) else u"失败"))
			return {"Err":False, "Val":"Total: %s  Success: %s"%(num, num-failcount)}
			
	def Score_Spider(self):
		try:
			G = self.Session.get("http://222.30.32.10/xsxk/studiedAction.do")
		except :
			return {"Err":True, "Val":"NetWork Error!"}
		if G.url == "http://222.30.32.10/stdlogin.jsp":
			return {"Err":True, "Val":"Please Login First!"}
		else:
			try:
				num=int(re.findall(u"共 ([0-9]+) 页", G.content.decode("gbk", "ignore"))[0])
			except:
				traceback.print_exc(file=sys.stdout)
				return {"Err":True, "Val":"Remote Server does not work as expected."}
			T_Arr = []
			for i in range(1, num+1):
				H = self.Session.post("http://222.30.32.10/xsxk/studiedPageAction.do", data = {"index": i})
				F = etree.HTML(H.content.lower().decode("GBK", "ignore"))
				Table_row = F.xpath(u"//table")[1].xpath(u'tr')[1:]
				for row in Table_row:
					T_Arr.append([re.sub("\s+"," ",j.text).encode("GBK", "ignore") for j in row.xpath("td")])
			return {"Err":False, "Val":T_Arr}
				
			
class RSA_password():
	def __init__(self):
		pass
		
	def RSA(self, pwd):
		#  Code copy from https://github.com/yqnku/One-Key-To-Evaluation/blob/master/PingJiao.py
		
		publicKey = int("00b6b7f8531b19980c66ae08e3061c6295a1dfd9406b32b202a59737818d75dea03de45d44271a1473af8062e8a4df927f031668ba0b1ec80127ff323a24cd0100bef4d524fdabef56271b93146d64589c9a988b67bc1d7a62faa6c378362cfd0a875361ddc7253aa0c0085dd5b17029e179d64294842862e6b0981ca1bde29979",16)
		pwd = pwd[::-1]
		pwdAscii = binascii.b2a_hex(pwd)
		pwdAscii = int(pwdAscii, 16)
		password = pwdAscii ** 65537 % publicKey
		password = hex(password)[2:-1]
		if len(password) != 256:
			add = '0' * (256 - len(password))
			password = add + password
		return password