#coding=utf-8
import C
import  requests
import urllib
from lxml import etree
import re
import os
import json
import AnsFind
import time
import random
import threading

Global_bg_Flag = True

def Get_Myth_Code(HTML):
	K = etree.HTML(HTML.decode('utf-8', 'ignore'))
	J =  K.xpath("//ul[@class='QuestionPreview']")
	__VIEWSTATE = K.xpath("//input[@name='__VIEWSTATE']")[0].attrib["value"]
	__EVENTVALIDATION =  K.xpath("//input[@name='__EVENTVALIDATION']")[0].attrib["value"]
	return __VIEWSTATE, __EVENTVALIDATION


def Login(usr, pwd):
	S = requests.session()
	#S.proxies = {'http':'http://127.0.0.1:8080'}  #For Debugging
	S.get("""http://222.30.60.18/Login.aspx?style=1""")
	L = S.get("""http://222.30.60.18/Login.aspx?style=1""").content
	_A, _B = Get_Myth_Code(L)
	req = urllib.urlencode({"__VIEWSTATE":_A, "__EVENTVALIDATION":_B}) + """&ctl00%%24ContentPlaceHolder1%%24txtUserName=%s&ctl00%%24ContentPlaceHolder1%%24txtPassword=%s&ctl00%%24ContentPlaceHolder1%%24btnLogin=%%E7%%99%%BB+%%E5%%BD%%95"""%(usr, pwd)
	hea = {"Content-Type":"application/x-www-form-urlencoded"}
	LS = S.post("""http://222.30.60.18/Login.aspx?style=1""", data = req, headers = hea)
	if not re.findall("""User\/GetPassword.aspx""", LS.content):
		print "Login Succ!"
		return S
	else:
		print "Login Failed"
		return None


def GetQue(Session):
	Session.get("""http://222.30.60.18/Exam/MyExam.aspx""")
	Session.get("""http://222.30.60.18/Login.aspx?style=1""")
	Que = Session.get("""http://222.30.60.18/Exam/ExamPaper.aspx?EPID=8""").content
	Session.get("""http://222.30.60.18/Login.aspx?style=1""")
	_A, _B = Get_Myth_Code(Que)
	Que = Session.post("""http://222.30.60.18/Exam/ExamPaper.aspx?EPID=8""",
		headers ={"Content-Type":"application/x-www-form-urlencoded"} , 
		data=urllib.urlencode({"__VIEWSTATE":_A, "__EVENTVALIDATION":_B}) + \
		"""&ctl00%24ctl00%24ContentPlaceHolder1%24ContentPlaceHolder1%24btnStart=%E5%BC%80%E5%A7%8B%E8%80%83%E8%AF%95&ctl00%24ctl00%24ContentPlaceHolder1%24ContentPlaceHolder1%24hfEPaperID=&ctl00%24ctl00%24ContentPlaceHolder1%24ContentPlaceHolder1%24hfEPID=8"""
		).content
	K = etree.HTML(Que.decode('utf-8'))
	J =  K.xpath("//ul[@class='QuestionPreview']")
	__VIEWSTATE = K.xpath("//input[@name='__VIEWSTATE']")[0].attrib["value"]
	__EVENTVALIDATION =  K.xpath("//input[@name='__EVENTVALIDATION']")[0].attrib["value"]
	T = {}
	Mark = 0
	for i in J:
		Mark+=1
		Q = i.xpath("li/span[@class='QFormGuidMsg']")[1].text if (i.xpath("li/span[@class='QFormGuidMsg']")[1].text) and (len(i.xpath("li/span[@class='QFormGuidMsg']")[1].text) > 4) else i.xpath("li/span[@class='QFormGuidMsg']")[4].text
		H = {}
		Inps = [(j.attrib["id"], j.attrib["name"]+"#"+j.attrib['value']) for j in  i.xpath("li/span[@class='QuestionParam']/input")]
		Ans =  [(j.attrib["for"], j.text) for j in i.xpath("li/span[@class='QuestionParam']/label")]
		for j in Inps:
			H[j[1]] = [k for k in Ans if k[0] == j[0]][0][1][3:]
		T[Mark]=(Q, H)
	return T, __VIEWSTATE, __EVENTVALIDATION

def PostString(AnsArray, __VIEWSTATE, __EVENTVALIDATION):
	Tmp = [re.split("#",j) for j in AnsArray]
	K = dict(Tmp)
	Oth = urllib.urlencode({"__VIEWSTATE":__VIEWSTATE, "__EVENTVALIDATION":__EVENTVALIDATION})+"""&ctl00%24ctl00%24ContentPlaceHolder1%24ContentPlaceHolder1%24txtEPaperName=&"""
	return (Oth+urllib.urlencode(K)+"""&ctl00%24ctl00%24ContentPlaceHolder1%24ContentPlaceHolder1%24btnSubmit=%E4%BA%A4+%E5%8D%B7""")
def SubmitAns(S, AnsString):
	Que = S.post("""http://222.30.60.18/Exam/ExamPaper.aspx?EPID=8""",headers ={"Content-Type":"application/x-www-form-urlencoded"} , data=AnsString).content
	return Que
def ResParse(resPage):
	K = etree.HTML(resPage.decode('utf-8'))
	J =  K.xpath(u"//span[@id='ContentPlaceHolder1_ContentPlaceHolder1_lbTotalMark']")[0].text
	return J
	

def Main(usr, pwd, wait):
	P = AnsFind.AnsFind()
	S= Login(usr,pwd)
	if S:
		G = []
		M = 0
		wait = (wait >= 0 and wait<=59) and wait or 59
		print u"将会延迟%s分钟提交"%wait

		#===========Start a background Thread=================
		t_bg = threading.Thread(target=Keep_Server_alive, args=(S, ))
		t_bg.setDaemon(True)
		t_bg.start()
		#===========Started===================================
		
		A, B, C = GetQue(S)
		STA = time.time()
		for i in A.items():
			print u"\n题目: ", unicode(i[1][0].decode("utf-8", 'ignore').encode("GBK", "ignore").decode("GBK", "ignore"))
			Q =  P.FindAns(i[1])
			print u"\n选择：", unicode(Q[1].decode("utf-8", 'ignore').encode("GBK", "ignore").decode("GBK", "ignore"))
			print u"======================================="
			G.append(Q[0])
			M+=1
		#print M
		while time.time()-STA < wait*60:
			print u"交卷等待期间，还有%.2f秒"%(wait*60-(time.time()-STA))
			time.sleep(5)
		print u"刷题结束, 得分为%s"%ResParse(SubmitAns(S, PostString(G, B, C)))
		global Global_bg_Flag
		Global_bg_Flag = False
	else:
		pass

def Keep_Server_alive(Sess):
	while Global_bg_Flag:
		Sess.get("""http://222.30.60.18/Services/HintServices.ashx?seed=%.16f&Action=Get"""%random.random())
		time.sleep(5)
	# print "Background Thread Exit"

if __name__=="__main__":
	print u"重要的事说三遍\n"
	print u"请确认自己的账号密码！首次登陆要填用户信息先去填了再说\n"
	print u"请确认自己的账号密码！首次登陆要填用户信息先去填了再说\n"
	print u"请确认自己的账号密码！首次登陆要填用户信息先去填了再说\n"
	print u"请输入学号：", ; usr = raw_input()
	print u"请输入密码：", ; pwd = raw_input()
	print u"请输入你觉得这套题让老师觉得你做多久合适的时间（单位：分钟）：", ; wait = raw_input()
	import traceback
	try:
		Main(usr, pwd, int(wait))
	except:
		print u"发生错误，请咨询身边的程序猿/喵/汪并提供下面的信息"
		print "Caught Traceback:"
		print traceback.format_exc()

	raw_input("Mission Complete. Press Enter to Continue")