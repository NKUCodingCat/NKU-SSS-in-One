#coding=utf-8
import PJ
import os, re, StringIO, time, urllib
import requests
from PIL import Image
from xkocr import OCR


class Xuanke(PJ.PJ):
	"""docstring for Xuanke"""
	def __init__(self):
		PJ.PJ.__init__(self)
		self.OCR_OBJ = OCR.Val_to_Str(os.path.split(os.path.realpath(__file__))[0]+"/dump-fuck.txt")
		self.Xuanke_Target_url = "http://222.30.32.10/xsxk/swichAction.do"
		self.Xuanke_Valcode_url = "http://222.30.32.10/SelectValidateCode"
		self.Xuanke_Inquire_Course_url = "http://222.30.32.3/apps/xksc/search.asp"
		self.Inquire_Session = requests.session()
		self.Xuanke_Name_Cache = {}

	def CheckLogin(self):
		try:
			NULL_F = self.Session.get("http://222.30.32.10/xsxk/sub_xsxk.jsp")
		except:
			
			return False
		else:
			if NULL_F.url == "http://222.30.32.10/stdlogin.jsp":
				NULL_F = NULL_F.content
				return False
			else:
				NULL_F = self.Session.get("http://222.30.32.10/xsxk/selectMianInitAction.do").content
				return True
	
	def Xuanke(self, Array_of_Course):
		self.Course_Cache_Refersh()
		if len(Array_of_Course)>4:
			return {"Err":True, "Val":"Course Array Too Large"}
		ValData = self.Session.get(self.Xuanke_Valcode_url)
		ValData_F = ValData.content
		if ValData.url == "http://222.30.32.10/stdlogin.jsp":
			return {"Err":True, "Val":"Please Login at First!"}
		try:
			IM_Sel_Valcode = Image.open(StringIO.StringIO(ValData_F))
		except:
			IM_Sel_Valcode = None
		Code = self.OCR_OBJ.IM_to_Str_MatDiff(IM_Sel_Valcode) if IM_Sel_Valcode else ""
		postdata="operation=xuanke&index=&code=%s"%Code
		for i in range(4):
			if i<len(Array_of_Course):
				postdata += ("&xkxh"+str(i+1)+"="+Array_of_Course[i])
			else:
				postdata += ("&xkxh"+str(i+1)+"=")
		postdata += "&departIncode=%25&courseindex="
		Data = self.Session.post(self.Xuanke_Target_url, postdata, headers = {"Content-Type":"application/x-www-form-urlencoded"}).content.decode("gbk").encode('utf-8')
		Return_Status = re.findall(u'"BlueBigText">[\s\S]*</font>', Data)
		if Return_Status:
			Return_Status = Return_Status[0][14:][:-10]
		else:
			Return_Status = ""
		if re.findall(r'无效', Return_Status):
			return {"Err":True, "Val":"Invalid Course Number"}
		if re.findall(r'正确的验证码', Data):
			return {"Err":True , "Val":"OCR for ValidateCode Fail"}
		return {"Err":False, "Val":(Return_Status, self.CheckSelected(Array_of_Course))}

	def Course_Cache_Get(self, Course_Code):
		return self.Xuanke_Name_Cache[Course_Code]["value"] if Course_Code in self.Xuanke_Name_Cache.keys() else None 

	def Course_Cache_Set(self, Course_Code, value, TTL=3600):
		self.Xuanke_Name_Cache[Course_Code] = {"value":value, "TTL":time.time()+TTL}

	def Course_Cache_Refersh(self):
		for i in self.Xuanke_Name_Cache.keys():
			if self.Xuanke_Name_Cache[i]["TTL"] < time.time():
				del self.Xuanke_Name_Cache[i]

	def Get_Course_Name(self, Course_Code):
		Name = self.Course_Cache_Get(Course_Code)
		if Name:
			return Name
		else:
			formdata='strsearch='+Course_Code+'&radio=2&Submit=%CC%E1%BD%BB'
			try:
				Data = self.Inquire_Session.post(self.Xuanke_Inquire_Course_url, data = formdata, headers ={'Content-Type': 'application/x-www-form-urlencoded'}).content.decode("gb2312")
			except:
				C_Name = "教务处网站无法使用，不能保证课程序号的正确性，请谨慎抢课"
			else:  
				pos = Data.find('</TD></TR><TR><TD>')
				if pos == -1:
					C_Name = "Wrong Course"
				else:
					Data = Data[pos:]
					C_Name = re.findall(u"[0-9\u4e00-\u9fa5\uFF00-\uFFEF\-]+", Data)[1].encode('utf8')
					self.Course_Cache_Set(Course_Code, C_Name, 600)
			return C_Name

	def CheckSelected(self, Array_of_Course):
		Tmp_Dict = {"Selected":[], "UnSelected":[]}
		WEB = self.Session.get("http://222.30.32.10/xsxk/selectedAction.do?operation=kebiao").content
		for Course_Code in Array_of_Course:
			# print Course_Code
			if re.findall(re.escape(self.Get_Course_Name(Course_Code).decode("utf-8", 'ignore').encode('gbk')), WEB):
				Tmp_Dict["Selected"].append(Course_Code)
			else:
				Tmp_Dict["UnSelected"].append(Course_Code)
		# print Tmp_Dict
		return Tmp_Dict
		
	def CheckSystemStatus(self):
		try:
			Xuanke_sys_Status = self.Session.get('''http://222.30.32.10/xsxk/selectMianInitAction.do''').content.decode("gbk").encode('utf-8')
		except:
			raise
		if re.findall(u'''<input type="button" name="xuanke"''', Xuanke_sys_Status):
			return True
		else:
			return False

	

if __name__ == '__main__':
	import time
	X = Xuanke()
	OCR_OBJ2 = OCR.Val_to_Str()
	if not X.Login("1111111", "000000", OCR_OBJ2.IM_to_Str_MatDiff(Image.open(X.vcode)))["Err"]:
		NULL_F = X.Session.get("http://222.30.32.10/xsxk/sub_xsxk.jsp").content
		NULL_F = X.Session.get("http://222.30.32.10/xsxk/selectMianInitAction.do").content
		for i in range(5):
			print X.Xuanke(["0777", "0077", "0765"])
			time.sleep(5)
