#coding=utf-8
import B
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
	req = """__VIEWSTATE=%%2FwEPDwUJMzM2NDM5OTM1DxYCHgpFcnJvckNvdW50ZmQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFJmN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkY2hrQXV0b0xvZ2luoMCy85suazYg0GQcn9hFHPIyWknVk3whxDeO9I%%2FfSEw%%3D&__EVENTVALIDATION=%%2FwEdAAVSX6Fc1%%2BWeaFp%%2FQlRb2t0n9nsvgpcFVLgi4qzbwR9V0Hjjswiyhm%%2Bg6KodwobC%%2FfOwS4xnW8ZIVB06X7opsHDkai9Oa0KM8wlAEGht%%2BZhxFjO8FoFveh0r5AAfjYTevpnwpdUdCam72d2lTTKAGFp5&ctl00%%24ContentPlaceHolder1%%24txtUserName=%s&ctl00%%24ContentPlaceHolder1%%24txtPassword=%s&ctl00%%24ContentPlaceHolder1%%24btnLogin=%%E7%%99%%BB+%%E5%%BD%%95"""%(usr, pwd)
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
	Que = Session.post("""http://222.30.60.18/Exam/ExamPaper.aspx?EPID=8""",headers ={"Content-Type":"application/x-www-form-urlencoded"} , data="""__VIEWSTATE=%2FwEPDwUKLTM3NzE3MTQyMw8WAh4GSXNFeGFtZxYCZg9kFgJmD2QWBAIBD2QWBAIFDxYCHgRUZXh0BdMBPGxpbmsgaHJlZj0iL1NjcmlwdHMvanF1ZXJ5dWkvanF1ZXJ5dWkuY3NzIiB0eXBlPSJ0ZXh0L2NzcyIgcmVsPSJzdHlsZXNoZWV0IiAvPjxsaW5rIGhyZWY9Ii9Db250ZW50L3NpdGUuY3NzIiB0eXBlPSJ0ZXh0L2NzcyIgcmVsPSJzdHlsZXNoZWV0IiAvPjxsaW5rIGhyZWY9Ii9Db250ZW50L21lbnUuY3NzIiB0eXBlPSJ0ZXh0L2NzcyIgcmVsPSJzdHlsZXNoZWV0IiAvPmQCBg8WAh8BBfYDPHNjcmlwdCBsYW5ndWFnZT0iamF2YXNjcmlwdCIgdHlwZT0idGV4dC9qYXZhc2NyaXB0IiBzcmM9Ii9TY3JpcHRzL2pxdWVyeS4xLjEwLjIubWluLmpzIj48L3NjcmlwdD48c2NyaXB0IGxhbmd1YWdlPSJqYXZhc2NyaXB0IiB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiIHNyYz0iL1NjcmlwdHMvanF1ZXJ5LnZhbGlkYXRlLm1pbi5qcyI%2BPC9zY3JpcHQ%2BPHNjcmlwdCBsYW5ndWFnZT0iamF2YXNjcmlwdCIgdHlwZT0idGV4dC9qYXZhc2NyaXB0IiBzcmM9Ii9TY3JpcHRzL2pxdWVyeXVpL2pxdWVyeXVpLm1pbi5qcyI%2BPC9zY3JpcHQ%2BPHNjcmlwdCBsYW5ndWFnZT0iamF2YXNjcmlwdCIgdHlwZT0idGV4dC9qYXZhc2NyaXB0IiBzcmM9Ii9TY3JpcHRzL21lbnUvanMvc3VwZXJmaXNoLmpzIj48L3NjcmlwdD48c2NyaXB0IGxhbmd1YWdlPSJqYXZhc2NyaXB0IiB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiIHNyYz0iL1NjcmlwdHMvZWFzeXNtYXJ0LmNvbmZpZ3VyYXRpb24uanMiPjwvc2NyaXB0PmQCAw9kFgQCAQ9kFgQCAQ8WAh4HVmlzaWJsZWcWBGYPDxYCHwEFBuWtmeaLk2RkAgEPZBYCZg8PFgIfAmhkZAICDxYCHwEFigI8dWw%2BDQo8bGk%2BPGEgaHJlZj0naHR0cDovLzIyMi4zMC42MC4xOC8nPummlumhtTwvYT48L2xpPg0KPGxpPjxhIGhyZWY9J2h0dHA6Ly8yMjIuMzAuNjAuMTgvQ291cnNlJz7or77nqIs8L2E%2BPC9saT4NCjxsaT48YSBocmVmPSdodHRwOi8vMjIyLjMwLjYwLjE4L0Rpc2N1c3MvVG9waWNzTGlzdC5hc3B4Jz7kupLliqg8L2E%2BPC9saT4NCjxsaT48YSBocmVmPSdodHRwOi8vMjIyLjMwLjYwLjE4L0V4YW0vTXlFeGFtLmFzcHgnPua1i%2BivlTwvYT48L2xpPg0KPC91bD4NCmQCAw9kFgICAQ9kFgJmD2QWBGYPZBYMAgEPFgIfAQUY5aSn5a2m6K%2Bt5paH5Zyo57q%2F5rWL6K%2BVZAIDDw8WAh8BBQI2MGRkAgUPDxYCHwEFAjUwZGQCBw8PFgIfAQUTMjAxMS0wMi0xNSAxMjowNTozMmRkAgkPDxYCHwEFBWFkbWluZGQCCw8PFgIfAQV75pys5rWL6aqM5L6b5oiR5qCh5a2m55Sf5L2%2F55So77yM5Y%2BW5Lik5qyh5Y%2BK5qC85ZCO55qE5pyA6auY5oiQ57up77yM55So5Lik5qyh5oiQ57up5LmL5oC75YiG5oqY5ZCI5Li65pyA57uI5oiQ57up55qEMjAl44CCZGQCAQ9kFgQCAg88KwAJAGQCAw88KwAJAGQYAQU%2BY3RsMDAkY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRDb250ZW50UGxhY2VIb2xkZXIxJE11bHRpVmlldzEPD2RmZEnVVH7mauPDuKreNlUlhAhtu3Fs3hyXXnqy0mFKON6j&__EVENTVALIDATION=%2FwEdAAQiHzmOhnUJtPm1SWERvzPjXNGBUCrVJ27TjLxGHHMeO1f9BD3xsjboC%2F2bAFyiwyQIGPM5hvlViWH72hQxyI9s%2FCjTrQ2I3%2F4OhfD551v2iH7HywcnBRkH2fm3MtRUIqA%3D&ctl00%24ctl00%24ContentPlaceHolder1%24ContentPlaceHolder1%24btnStart=%E5%BC%80%E5%A7%8B%E8%80%83%E8%AF%95&ctl00%24ctl00%24ContentPlaceHolder1%24ContentPlaceHolder1%24hfEPaperID=&ctl00%24ctl00%24ContentPlaceHolder1%24ContentPlaceHolder1%24hfEPID=8""").content
	K = etree.HTML(Que.decode('utf-8'))
	J =  K.xpath("//ul[@class='QuestionPreview']")
	__VIEWSTATE = K.xpath("//input[@name='__VIEWSTATE']")[0].attrib["value"]
	__EVENTVALIDATION =  K.xpath("//input[@name='__EVENTVALIDATION']")[0].attrib["value"]
	T = {}
	Mark = 0
	for i in J:
		Mark+=1
		Q = i.xpath("li/span[@class='QFormGuidMsg']")[1].text
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
			print u"题目: ",i[1][0]
			Q =  P.FindAns(i[1])
			print u"选择：", Q[1]
			print u"======================================="
			G.append(Q[0])
			M+=1
		#print M
		while time.time()-STA < wait*60:
			print u"交卷等待期间，还有%.3f秒"%(wait*60-(time.time()-STA))
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