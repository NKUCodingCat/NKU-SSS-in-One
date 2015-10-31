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
def Login(usr, pwd):
	S = requests.session()
	S.get("""http://222.30.60.18/Login.aspx?style=1""")
	L = S.get("""http://222.30.60.18/Login.aspx?style=1""").content
	req = """__VIEWSTATE=%%2FwEPDwUJMzM2NDM5OTM1DxYCHgpFcnJvckNvdW50ZmQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFJmN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkY2hrQXV0b0xvZ2luTRwOOUHF1qYEfIwBG726SFMFQPuk0%%2BsYVa7MyL3E8tg%%3D&__EVENTVALIDATION=%%2FwEdAAUYz4uEeAQrBwgZLj1mn1SF9nsvgpcFVLgi4qzbwR9V0Hjjswiyhm%%2Bg6KodwobC%%2FfOwS4xnW8ZIVB06X7opsHDkai9Oa0KM8wlAEGht%%2BZhxFtC%%2BvTinjyMs152E9gHMuPFAh4R0mgMTIGQBkbZlLBsA&ctl00%%24ContentPlaceHolder1%%24txtUserName=%s&ctl00%%24ContentPlaceHolder1%%24txtPassword=%s&ctl00%%24ContentPlaceHolder1%%24btnLogin=%%E7%%99%%BB+%%E5%%BD%%95"""%(usr, pwd)
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
	Que = Session.post("""http://222.30.60.18/Exam/ExamPaper.aspx?EPID=8""",headers ={"Content-Type":"application/x-www-form-urlencoded"} , data="""__VIEWSTATE=%2FwEPDwUKLTM3NzE3MTQyMw8WAh4GSXNFeGFtZxYCZg9kFgJmD2QWBAIBD2QWBAIFDxYCHgRUZXh0BZwCPGxpbmsgaHJlZj0iLi4vQ29udGVudC9ib290c3RyYXAuY3NzIiB0eXBlPSJ0ZXh0L2NzcyIgcmVsPSJzdHlsZXNoZWV0IiAvPjxsaW5rIGhyZWY9Ii9TY3JpcHRzL2pxdWVyeXVpL2pxdWVyeXVpLmNzcyIgdHlwZT0idGV4dC9jc3MiIHJlbD0ic3R5bGVzaGVldCIgLz48bGluayBocmVmPSIvQ29udGVudC9zaXRlLmNzcyIgdHlwZT0idGV4dC9jc3MiIHJlbD0ic3R5bGVzaGVldCIgLz48bGluayBocmVmPSIvQ29udGVudC9tZW51LmNzcyIgdHlwZT0idGV4dC9jc3MiIHJlbD0ic3R5bGVzaGVldCIgLz5kAgYPFgIfAQX2AzxzY3JpcHQgbGFuZ3VhZ2U9ImphdmFzY3JpcHQiIHR5cGU9InRleHQvamF2YXNjcmlwdCIgc3JjPSIvU2NyaXB0cy9qcXVlcnkuMS4xMC4yLm1pbi5qcyI%2BPC9zY3JpcHQ%2BPHNjcmlwdCBsYW5ndWFnZT0iamF2YXNjcmlwdCIgdHlwZT0idGV4dC9qYXZhc2NyaXB0IiBzcmM9Ii9TY3JpcHRzL2pxdWVyeS52YWxpZGF0ZS5taW4uanMiPjwvc2NyaXB0PjxzY3JpcHQgbGFuZ3VhZ2U9ImphdmFzY3JpcHQiIHR5cGU9InRleHQvamF2YXNjcmlwdCIgc3JjPSIvU2NyaXB0cy9qcXVlcnl1aS9qcXVlcnl1aS5taW4uanMiPjwvc2NyaXB0PjxzY3JpcHQgbGFuZ3VhZ2U9ImphdmFzY3JpcHQiIHR5cGU9InRleHQvamF2YXNjcmlwdCIgc3JjPSIvU2NyaXB0cy9tZW51L2pzL3N1cGVyZmlzaC5qcyI%2BPC9zY3JpcHQ%2BPHNjcmlwdCBsYW5ndWFnZT0iamF2YXNjcmlwdCIgdHlwZT0idGV4dC9qYXZhc2NyaXB0IiBzcmM9Ii9TY3JpcHRzL2Vhc3lzbWFydC5jb25maWd1cmF0aW9uLmpzIj48L3NjcmlwdD5kAgMPZBYEAgEPZBYEAgEPFgIeB1Zpc2libGVnFgRmDw8WAh8BBQnpmYjpnZnpn6xkZAIBD2QWAmYPDxYCHwJoZGQCAg8WAh8BBYoCPHVsPg0KPGxpPjxhIGhyZWY9J2h0dHA6Ly8yMjIuMzAuNjAuMTgvJz7pppbpobU8L2E%2BPC9saT4NCjxsaT48YSBocmVmPSdodHRwOi8vMjIyLjMwLjYwLjE4L0NvdXJzZSc%2B6K%2B%2B56iLPC9hPjwvbGk%2BDQo8bGk%2BPGEgaHJlZj0naHR0cDovLzIyMi4zMC42MC4xOC9EaXNjdXNzL1RvcGljc0xpc3QuYXNweCc%2B5LqS5YqoPC9hPjwvbGk%2BDQo8bGk%2BPGEgaHJlZj0naHR0cDovLzIyMi4zMC42MC4xOC9FeGFtL015RXhhbS5hc3B4Jz7mtYvor5U8L2E%2BPC9saT4NCjwvdWw%2BDQpkAgMPZBYCAgEPZBYCZg9kFgRmD2QWDAIBDxYCHwEFGOWkp%2BWtpuivreaWh%2BWcqOe6v%2Ba1i%2BivlWQCAw8PFgIfAQUCNjBkZAIFDw8WAh8BBQI1MGRkAgcPDxYCHwEFEzIwMTEtMDItMTUgMTI6MDU6MzJkZAIJDw8WAh8BBQVhZG1pbmRkAgsPDxYCHwEFe%2BacrOa1i%2BmqjOS%2Bm%2BaIkeagoeWtpueUn%2BS9v%2BeUqO%2B8jOWPluS4pOasoeWPiuagvOWQjueahOacgOmrmOaIkOe7qe%2B8jOeUqOS4pOasoeaIkOe7qeS5i%2BaAu%2BWIhuaKmOWQiOS4uuacgOe7iOaIkOe7qeeahDIwJeOAgmRkAgEPZBYEAgIPPCsACQBkAgMPPCsACQBkGAEFPmN0bDAwJGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkQ29udGVudFBsYWNlSG9sZGVyMSRNdWx0aVZpZXcxDw9kZmRyPGFgrTy8fUfnXEnmek0hT8VmGCrrh23nl2JsvkhbDg%3D%3D&__EVENTVALIDATION=%2FwEdAASshTcAXEQOPIqVALq0W3H%2BXNGBUCrVJ27TjLxGHHMeO1f9BD3xsjboC%2F2bAFyiwyQIGPM5hvlViWH72hQxyI9s4YAH8rYwjXJ%2Bmp1UUdLolx615cYGTsGc6ntG7Hix%2Fz0%3D&ctl00%24ctl00%24ContentPlaceHolder1%24ContentPlaceHolder1%24btnStart=%E5%BC%80%E5%A7%8B%E8%80%83%E8%AF%95&ctl00%24ctl00%24ContentPlaceHolder1%24ContentPlaceHolder1%24hfEPaperID=&ctl00%24ctl00%24ContentPlaceHolder1%24ContentPlaceHolder1%24hfEPID=8""").content
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
		A, B, C = GetQue(S)
		STA = time.time()
		for i in A.items():
			print u"\n题目: ",i[1][0].decode("utf-8", 'ignore').encode("GBK", "ignore")
			Q =  P.FindAns(i[1])
			print u"\n选择：", unicode(Q[1].decode("utf-8", 'ignore'))
			print u"======================================="
			G.append(Q[0])
			M+=1
		#print M
		while time.time()-STA < wait*60:
			print u"交卷等待期间，还有%.2f秒"%(wait*60-(time.time()-STA))
			S.get("""http://222.30.60.18/Services/HintServices.ashx?seed=%.16f&Action=Get"""%random.random())
			time.sleep(5)
		print u"刷题结束, 得分为%s"%ResParse(SubmitAns(S, PostString(G, B, C)))
	else:
		pass
if __name__=="__main__":
	print u"重要的事说三遍\n"
	print u"请确认自己的账号密码！首次登陆要填用户信息先去填了再说\n"
	print u"请确认自己的账号密码！首次登陆要填用户信息先去填了再说\n"
	print u"请确认自己的账号密码！首次登陆要填用户信息先去填了再说\n"
	print u"请输入学号：", ; usr = raw_input()
	print u"请输入密码：", ; pwd = raw_input()
	print u"请输入你觉得这套题让老师觉得你做多久合适的时间（单位：分钟）：", ; wait = raw_input()
	Main(usr, pwd, int(wait))
	raw_input("Mission Complete. Press Any Key to Continue")