#coding=utf-8
import B
import requests
import time, re, json
from lxml import etree
import bar

#=====some const========
Home = "http://192.168.8.119/"
log_in = "http://192.168.8.119/login"
Base = "http://192.168.8.119/ol/"
Refresh = "http://192.168.8.119/ol/studycourse/update"
Finish = "http://192.168.8.119/ol/studycourse/finish"
Check = "http://192.168.8.119/ol/studycourse/check"
Keep_alive = 245.0 #in second
#====================
def _(string):
	if isinstance(string, unicode): 
		return string.encode('GBK') 
	else: 
		return string.decode("utf-8").encode("GBK")
def lxml_de(content):
	page = etree.HTML(content.lower().decode('utf-8', 'ignore'))
	uls = page.xpath(u"//ul")
	waiting = []
	for i in uls:
		T = i.xpath(u"div/a/div/p/span/strong")
		H = i.xpath(u"div/a")
		P = i.xpath(u"div/a/div/p/strong")
		if T != []:
			Te = T[0]
			waiting.append((H[0].attrib["href"],P[0].text,Te.text))
	return  waiting
def lxml_Qu(content):
	page = etree.HTML(content.lower().decode('utf-8', 'ignore'))
	lis = page.xpath(u"//li[@class='list-group-item']")
	all = []
	for i in lis:
		Val = i.xpath(u"input")
		Tmp = []
		for j in Val:
			Tmp.append((j.attrib["name"],j.attrib["value"]))
		all.append(Tmp)
	return all
def lxml_Name(content):
	page = etree.HTML(content.lower().decode('utf-8', 'ignore'))
	div = page.xpath(u"//div[@class='container-fluid']/div")
	try:
		res = [i.xpath(u"div")[1].text for i in div[:2]]	
		return res
	except:
		return []
	
def Login(usr,pwd):
	S = requests.Session()
	S.headers.update({"User-Agent":""" Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"""})
	S.get(Home)
	F = lxml_Name(S.post(log_in,data = {"method":"student","username":usr,"password":pwd}).content)
	return S, F
def Ref(Sess, Addr, Len):
	Count = 0
	for i in range(Len):
		Sess.get(Addr).status_code
		end = time.time()+Keep_alive
		Sess.get(Refresh)
		print "[%s]"%time.ctime(),_("四分钟后刷新，请稍候……"),_("已刷%s次，还剩%s次"%(Count, (Len-Count)))
		S = bar.SimpleProgressBar()
		S.update(100*(1-float(end-time.time())/Keep_alive))
		while time.time() < end:
			time.sleep(0.25)
			S.update(100*(1-float(end-time.time())/Keep_alive))
		S.update(100*(1-float(end-time.time())/Keep_alive))
		Sess.get(Finish)
		print "\n[%s]"%time.ctime(),_("一次刷课结束\n")
		Count+=1
def Num(Arr):
	res = []
	for i in Arr:
		QuNum = list(set([j[0] for j in i]))
		if len(QuNum) == 1:
			res.append((QuNum,[j[1] for j in i]))
		else:
			raise KeyError, "数据有误"
	return res
def Que(Sess, Addr):
	Web = Sess.get(Addr).content
	res = Sess.get(Refresh).content
	#print res
	if  res == "finish":
		
		Need = lxml_Qu(Web)
		#====find Num====
		try:
			ALL = Num(Need)
			#print ALL
		except:
			return "Error"
		#====FirstGet=====
		Ans = json.loads(Sess.post(Check, data = dict([(i[0][0],i[1][0]) for i in ALL])).content)
		Next = Ans[len(Ans)/2:len(Ans)-1]
		#====Second Get====
		if len(Next) != len(ALL):
			return "Error"
		FinalHit = Sess.post(Check, dict([(ALL[i][0][0], Next[i]) for i in range(len(ALL))]))
		if json.loads(FinalHit.content)[-1] > 0.6:
			return "课后测试已经完成\n"
		else:
			return "完成课后测试时有异常错误请手动解决\n"
	elif res == "":
		return "Error"
	else:
		return "课后测试已经完成\n"
		
#=====main=======
print _("""
;;;;;;;;;;;;;;;;;;;;;;;;;    Developed By NKUCodingcat
;;;;;;;;;;;;;;;WWW;;;;;;;
;;;;;;;;WWWWW;;;;WWWi;;;;    欢迎使用南开大学党课在线学习刷课机
;;;;;;WWWWWWj;;;;;KWWW;;;
;;;;WWWWWWW;;;;;;;;WWWK;;    能刷完所有的课时以及课后习题，但是不能刷考试
;;;iWWWWWWWWWi;;;;;KWWW;;
;;;;;;W;;;WWWWWK;;;WWWW;;    这个东西并不能节省刷的时间
;;;;;;;;;;;;WWWWWW;WWWW;;
;;;W;;;;;;;;;EWWWWWWWW;;;    所以他说要学多久就要刷多久
;;WWWWK;;;;;;;;WWWWWW;;;;
;WWWWWWWWWWWWWWWWWWWWWW;;    以及不在南开内网的孩子们就别用了
;WWW;;;WWWWWWWWW;;;;W;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;    那玩意在外网根本打不开""")

print _("""
          Ver 1.0.20150325 \n
=======================================
""")
usr = raw_input(_("请输入学号(输完按回车): "))
pwd = raw_input(_("请输入密码(输完按回车): "))
S, profile = Login(usr,pwd)
Wait_to_Ref = lxml_de(S.get("http://192.168.8.119/ol/studycourse").content)
if profile == []:
	print _("\n\n无法获取资料，密码可能有误\n")
	profile = ["",""]
print _("\n请确认资料，课程内容及进度，无误请按回车\n如果有误请退出并联系作者\n邮箱nankai.codingcat@outlook.com\n")
print _("学号："), profile[0], _("              姓名："), profile[1], _("\n")
print _("====课程名称================================学习进度====\n")
for j in Wait_to_Ref:
	print j[1],"\t",j[2]
raw_input()
print _("======开始刷======")
print _("刷的时候看着点因为保不齐进程被down，所以要是超过十分钟没反应就手动结束重新开始w\n")
try:
	for k in Wait_to_Ref:
		stu, ned = re.split(r"[\/\\]", k[2])
		print _("开始刷"),k[1]
		if int(stu) < int(ned):
			leng = (int(ned)-int(stu))/4 + 1
			Ref(S, Base+k[0], leng)
		else:
			pass
		print k[1],_("已经刷完\n")
finally:
	S.get(Finish)
for k in Wait_to_Ref:
	print _("正在完成"),k[1],_("的课后习题")
	print _(Que(S, Base+k[0]))
print _("\n任务全部完成，感谢使用，按回车退出")
raw_input()