#!/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import division
Ver = 'Ver 2.0 Basic (20150305)'

import C

import httplib
import re
import os, sys
import PIL.Image, PIL.ImageTk
import urllib2
import urllib
import cookielib
import time

#----------------------------------------------------
addr="http://222.30.32.10/ValidateCode"

hosturl="http://222.30.32.10/"

posturl="http://222.30.32.10/stdloginAction.do"

UpUrl = 'http://222.30.32.10/xsxk/swichAction.do'

HEADERS = ''

Login_S = False
StopSignal = False

STUDENT_ID=''
PASSWORD=''

headers= {
'Accept':' application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, */*',
'Referer':' http://222.30.32.10/xsxk/swichAction.do',
'Accept-Language':' zh-CN',
'Content-Type':' application/x-www-form-urlencoded',
'Accept-Encoding':' gzip, deflate',
'User-Agent':' Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)',
'Host':' 222.30.32.10',
'Pragma':' no-cache',
'Cookie':''
}

HEADERS = headers
PROCESSING = False
Cache = {}

#--------------------------------------------------------------------------------------------
def ReLoadData():
	global HEADERS
	global PROCESSING
	global Login_S
	global headers
	try:
		conn=httplib.HTTPConnection("222.30.32.10",timeout=10)
		conn.request("GET","/")
		res=conn.getresponse()
		cookie=res.getheader("Set-Cookie")
		conn.close()
	except:
		return False
	headers= {
	'Accept':' application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, */*',
	'Referer':' http://222.30.32.10/xsxk/swichAction.do',
	'Accept-Language':' zh-CN',
	'Content-Type':' application/x-www-form-urlencoded',
	'Accept-Encoding':' gzip, deflate',
	'User-Agent':' Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)',
	'Host':' 222.30.32.10',
	'Pragma':' no-cache',
	'Cookie':cookie
	}
	#get ValidateCode
	try:
		conn=httplib.HTTPConnection("222.30.32.10",timeout=10)
		conn.request("GET","http://222.30.32.10/ValidateCode","",headers)
		res=conn.getresponse()
		f=open("ValidateCode.jpg","w+b")
		f.write(res.read())
		f.close()
		conn.close()
	except:
		return False

	HEADERS = headers
	PROCESSING = False
	Login_S = False
	return True

#----------------------------------------------------

try:
	from tkinter import *
except ImportError:  #Python 2.x
	PythonVersion = 2
	from Tkinter import *
	from tkFont import Font
	from ttk import *
	#Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
	from tkMessageBox import *
	#Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
	#import tkFileDialog
	#import tkSimpleDialog
else:  #Python 3.x
	PythonVersion = 3
	from tkinter.font import Font
	from tkinter.ttk import *
	from tkinter.messagebox import *
	#import tkinter.filedialog as tkFileDialog
	#import tkinter.simpledialog as tkSimpleDialog	#askstring()

class Application_ui(Frame):
	#这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master.title('一键刷课 for NKU V2.0 Basic')
		self.master.geometry('640x480')
		self.createWidgets()

	def createWidgets(self):
		self.top = self.winfo_toplevel()

		self.style = Style()

		self.style.configure('TStuID.TLabel', anchor='w')
		self.StuID = Label(self.top, text='学号：', style='TStuID.TLabel')
		self.StuID.place(relx=0.038, rely=0.034, relwidth=0.089, relheight=0.053)

		self.style.configure('TStu_PWD.TLabel', anchor='w')
		self.Stu_PWD = Label(self.top, text='密码：', style='TStu_PWD.TLabel')
		self.Stu_PWD.place(relx=0.038, rely=0.119, relwidth=0.089, relheight=0.053)

		self.style.configure('TV_code.TLabel', anchor='w')
		self.V_code = Label(self.top, text='验证码：', style='TV_code.TLabel')
		self.V_code.place(relx=0.038, rely=0.305, relwidth=0.089, relheight=0.053)

		self.IDVar = StringVar(value='')
		self.ID = Entry(self.top, textvariable=self.IDVar)
		self.ID.place(relx=0.15, rely=0.034, relwidth=0.239, relheight=0.053)

		self.PassWordVar = StringVar(value='')
		self.PassWord = Entry(self.top, textvariable=self.PassWordVar, show='*')
		self.PassWord.place(relx=0.15, rely=0.119, relwidth=0.239, relheight=0.053)
		self.PassWord.bind("<KeyPress-Return>",self.Login_Cmd)

		self.vcodeVar = StringVar(value='')
		self.vcode = Entry(self.top, textvariable=self.vcodeVar)
		self.vcode.place(relx=0.15, rely=0.305, relwidth=0.239, relheight=0.053)
		self.vcode.bind("<KeyPress-Return>",self.Login_Cmd)

		self.style.configure('TLogin.TButton')
		self.Login = Button(self.top, text='登录', command=self.Login_Cmd, style='TLogin.TButton')
		self.Login.place(relx=0.07, rely=0.39, relwidth=0.129, relheight=0.09)

		self.style.configure('TRe.TButton')
		self.Re = Button(self.top, text='刷新验证码', command=self.Refresh_Cmd)
		self.Re.place(relx=0.22, rely=0.39, relwidth=0.15, relheight=0.09)

		self.style.configure('TLabel1.TLabel', anchor='w')
		self.Label1 = Label(self.top, text='  课号1', style='TLabel1.TLabel')
		self.Label1.place(relx=0.488, rely=0.017, relwidth=0.089, relheight=0.053)

		self.Text1Var = StringVar(value='')
		self.Text1 = Entry(self.top, textvariable=self.Text1Var)
		self.Text1.place(relx=0.601, rely=0.017, relwidth=0.114, relheight=0.053)

		self.style.configure('TLabel2.TLabel', anchor='w')
		self.Label2 = Label(self.top, text='  课号2', style='TLabel2.TLabel')
		self.Label2.place(relx=0.488, rely=0.085, relwidth=0.089, relheight=0.053)

		self.Text2Var = StringVar(value='')
		self.Text2 = Entry(self.top, textvariable=self.Text2Var)
		self.Text2.place(relx=0.601, rely=0.085, relwidth=0.114, relheight=0.053)

		self.style.configure('TLabel3.TLabel', anchor='w')
		self.Label3 = Label(self.top, text='  课号3', style='TLabel3.TLabel')
		self.Label3.place(relx=0.488, rely=0.153, relwidth=0.089, relheight=0.053)

		self.Text3Var = StringVar(value='')
		self.Text3 = Entry(self.top, textvariable=self.Text3Var)
		self.Text3.place(relx=0.601, rely=0.153, relwidth=0.114, relheight=0.053)

		self.style.configure('TLabel4.TLabel', anchor='w')
		self.Label4 = Label(self.top, text='  课号4', style='TLabel4.TLabel')
		self.Label4.place(relx=0.488, rely=0.22, relwidth=0.089, relheight=0.053)

		self.Text4Var = StringVar(value='')
		self.Text4 = Entry(self.top, textvariable=self.Text4Var)
		self.Text4.place(relx=0.601, rely=0.22, relwidth=0.114, relheight=0.053)

		self.style.configure('TLabel5.TLabel', anchor='w')
		self.Label5 = Label(self.top, text='  课号5', style='TLabel5.TLabel')
		self.Label5.place(relx=0.488, rely=0.288, relwidth=0.089, relheight=0.053)

		self.Text5Var = StringVar(value='')
		self.Text5 = Entry(self.top, textvariable=self.Text5Var)
		self.Text5.place(relx=0.601, rely=0.288, relwidth=0.114, relheight=0.053)

		self.style.configure('TLabel6.TLabel', anchor='w')
		self.Label6 = Label(self.top, text='  课号6', style='TLabel6.TLabel')
		self.Label6.place(relx=0.488, rely=0.356, relwidth=0.102, relheight=0.053)

		self.Text6Var = StringVar(value='')
		self.Text6 = Entry(self.top, textvariable=self.Text6Var)
		self.Text6.place(relx=0.601, rely=0.356, relwidth=0.114, relheight=0.053)

		self.style.configure('TLabel7.TLabel', anchor='w')
		self.Label7 = Label(self.top, text='  课号7', style='TLabel7.TLabel')
		self.Label7.place(relx=0.751, rely=0.017, relwidth=0.089, relheight=0.053)

		self.Text7Var = StringVar(value='')
		self.Text7 = Entry(self.top, textvariable=self.Text7Var)
		self.Text7.place(relx=0.864, rely=0.017, relwidth=0.114, relheight=0.053)

		self.style.configure('TLabel8.TLabel', anchor='w')
		self.Label8 = Label(self.top, text='  课号8', style='TLabel8.TLabel')
		self.Label8.place(relx=0.751, rely=0.085, relwidth=0.089, relheight=0.053)

		self.Text8Var = StringVar(value='')
		self.Text8 = Entry(self.top, textvariable=self.Text8Var)
		self.Text8.place(relx=0.864, rely=0.085, relwidth=0.114, relheight=0.053)

		self.style.configure('TLabel9.TLabel', anchor='w')
		self.Label9 = Label(self.top, text='  课号9', style='TLabel9.TLabel')
		self.Label9.place(relx=0.751, rely=0.153, relwidth=0.089, relheight=0.053)

		self.Text9Var = StringVar(value='')
		self.Text9 = Entry(self.top, textvariable=self.Text9Var)
		self.Text9.place(relx=0.864, rely=0.153, relwidth=0.114, relheight=0.053)

		self.style.configure('TLabel10.TLabel', anchor='w')
		self.Label10 = Label(self.top, text='  课号10', style='TLabel10.TLabel')
		self.Label10.place(relx=0.751, rely=0.22, relwidth=0.089, relheight=0.053)

		self.Text10Var = StringVar(value='')
		self.Text10 = Entry(self.top, textvariable=self.Text10Var)
		self.Text10.place(relx=0.864, rely=0.22, relwidth=0.114, relheight=0.053)

		self.style.configure('TLabel11.TLabel', anchor='w')
		self.Label11 = Label(self.top, text='  课号11', style='TLabel11.TLabel')
		self.Label11.place(relx=0.751, rely=0.288, relwidth=0.089, relheight=0.053)

		self.Text11Var = StringVar(value='')
		self.Text11 = Entry(self.top, textvariable=self.Text11Var)
		self.Text11.place(relx=0.864, rely=0.288, relwidth=0.114, relheight=0.053)

		self.style.configure('TLabel12.TLabel', anchor='w')
		self.Label12 = Label(self.top, text='  课号12', style='TLabel12.TLabel')
		self.Label12.place(relx=0.751, rely=0.356, relwidth=0.089, relheight=0.053)

		self.Text12Var = StringVar(value='')
		self.Text12 = Entry(self.top, textvariable=self.Text12Var)
		self.Text12.place(relx=0.864, rely=0.356, relwidth=0.114, relheight=0.053)

		self.Var = StringVar()
		self.style.configure('TOption1.TRadiobutton')
		self.Option1 = Radiobutton(self.top, text='队列模式', value=0, variable=self.Var, style='TOption1.TRadiobutton')
		self.Option1.place(relx=0.488, rely=0.475, relwidth=0.127, relheight=0.036)

		self.style.configure('TOption2.TRadiobutton')
		self.Option2 = Radiobutton(self.top, text='轮询模式', value=1, variable=self.Var, style='TOption2.TRadiobutton')
		self.Option2.place(relx=0.488, rely=0.424, relwidth=0.127, relheight=0.036)
		self.Var.set(1)

		self.style.configure('TStart.TButton')
		self.Start = Button(self.top, text='开始抢课', command=self.Start_Cmd, style='TStart.TButton')
		self.Start.place(relx=0.638, rely=0.424, relwidth=0.139, relheight=0.087)

		self.style.configure('TStop.TButton')
		self.Stop = Button(self.top, text='停止抢课', command=self.Stop_Cmd, style='TStop.TButton')
		self.Stop.place(relx=0.801, rely=0.424, relwidth=0.139, relheight=0.087)

		self.Log = Text(self.top)
		self.Log.place(relx=0.038, rely=0.576, relwidth=0.565, relheight=0.409)
		self.Log.update()

		self.style.configure('TLabel13.TLabel', anchor='w')
		self.Label13 = Label(self.top, text='当前状态', style='TLabel13.TLabel')
		self.Label13.place(relx=0.025, rely=0.525, relwidth=0.102, relheight=0.036)

		self.style.configure('TLabel14.TLabel', anchor='w')
		self.Label14 = Label(self.top, text='已经抢到', style='TLabel14.TLabel')
		self.Label14.place(relx=0.626, rely=0.542, relwidth=0.089, relheight=0.036)

		self.Log2 = Text(self.top)
		self.Log2.place(relx=0.626, rely=0.576, relwidth=0.352, relheight=0.341)
		self.Log2.update()

		self.style.configure('TVersion.TLabel', anchor='w')
		self.Version = Label(self.top, text=Ver, style='TVersion.TLabel')
		self.Version.place(relx=0.638, rely=0.932, relwidth=0.35, relheight=0.053)

		Network=True
		if not ReLoadData():
			Network=False

		self.photo=PIL.Image.open("ValidateCode.jpg")
		self.im = PIL.ImageTk.PhotoImage(self.photo)
		self.V_Pic= Label(self.top,image = self.im)
		self.V_Pic.place(relx=0.05, rely=0.203, relwidth=0.327, relheight=0.053)

		if not Network:
			self.Log.insert(1.0,"网络连接错误，无法连接到选课系统。请检查网络连接！\n")
			self.Log.update()


class Application(Application_ui):
	#这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
	def __init__(self, master=None):
		Application_ui.__init__(self, master)



	def Login_Cmd(self, event=None):
		global HEADERS
		global STUDENT_ID
		global PASSWORD
		self.headers = HEADERS
		ID=self.ID.get()
		passwd=self.PassWord.get()
		v_code=self.vcode.get()

		try:
			logindata="operation=&usercode_text="+ID+"&userpwd_text="+passwd+"&checkcode_text="+v_code+"&submittype=%C8%B7+%C8%CF"
			conn=httplib.HTTPConnection("222.30.32.10",timeout=10)
			conn.request("POST","http://222.30.32.10/stdloginAction.do",logindata,self.headers)
			res=conn.getresponse()
			response=res.read()
			content=response.decode("gb2312")
			conn.close()
		except:
			self.Log.insert(1.0,"网络连接错误，无法连接到选课系统。请检查网络连接！\n")
			if ReLoadData():
				self.Refresh()
			else:
				return

		global Login_S
		Login_S = False
		self.err_code="未知错误"

		if content.find("stdtop") != -1:
			Login_S = True
			header = self.headers
			STUDENT_ID=ID
			PASSWORD=passwd
			self.Log.insert(1.0,"登录成功！\n")

		get_v_code=True
		if Login_S == False and (content.find(unicode("请输入正确的验证码","utf8")) != -1):
			self.err_code="验证码错误！"
			if not self.Refresh_Cmd():
				get_v_code=False
			else:
				get_v_code=True

		if Login_S == False and (content.find(u"用户不存在或密码错误") != -1):
			self.err_code="用户不存在或密码错误！"

		if Login_S == False and (content.find(u"忙") != -1 or content.find(u"负载") != -1):
			self.err_code="系统忙，请稍后再试！"


		if (Login_S != True):
			self.Log.insert(1.0,self.err_code+'\n')
			if not get_v_code:
				self.Log.insert(1.0,'验证码刷新失败！\n')
		return

	def Start_Cmd(self, event=None):
		#------------------------------------------------------------------
		global PROCESSING
		global Login_S
		global HEADERS
		global StopSignal
		#------------------------------------------------------------------
		if not self.CheckLogin():
			err_code="请先登录！"
			self.Log.insert(1.0,err_code+'\n')
			self.Log.update()
			self.Stop_Cmd()
			return
		#------------------------------------------------------------------
		course=self.GetCourseCode()
		if course==None:
			err_code="请输入课程代号\n"
			self.Log.insert(1.0,err_code)
			self.Log.update()
			self.Stop_Cmd()
			return
		illegal=self.illegal_list(course)
		if illegal[0]!=[]:
			err_code="请核对后重新开始！\n"
			self.Log.insert(1.0,err_code)
			self.Log.update()
			for i in range(len(illegal[0])):
				err_code=illegal[0][i]+' '+illegal[1][i]+'\n'
				self.Log.insert(1.0,err_code)
				self.Log.update()
			err_code="以下课号有误：\n"
			self.Log.insert(1.0,err_code)
			self.Log.update()
			self.Stop_Cmd()
			return
		#------------------------------------------------------------------
		PROCESSING=True
		if not self.CheckSystemStatus():
			self.Log.delete(20.0,END)
			self.wait_for_system()
			if not self.CheckSystemStatus():
				if not StopSignal:
					err_code="未知错误。请重新点击“开始刷课”！"
					self.Log.insert(1.0,err_code+'\n')
					self.Stop_Cmd()
					StopSignal=False
				else:
					StopSignal=False
				return
		#------------------------------------------------------------------

		#------------------------------------------------------------------
		self.Log.delete(0.0,END)
		self.Log.insert(1.0,"Starting........Connecting............\n")
		self.Log.update()
		#------------------------------------------------------------------
		use_queue=True
		mode='queue'
		count=0
		if self.Var.get()=='1' or self.Var.get()=='':
			use_queue=True
		else:
			use_queue=False
		while PROCESSING:
			count += 1
			if use_queue:
				mode='queue'
			else:
				mode='stack'
			post_course,course=self.select_course(course,mode)
			#print post_course
			#course=self.select_course(course,mode)[1]
			#print course
			try:
				fail_course=self.PostData(post_course,count)
			except KeyboardInterrupt:
				self.Log.insert(1.0,"KeyboardInterrupt\n")
			#print fail_course
			course=self.merge_course_list(course,fail_course,mode)
			#print course
			if len(course)>0:
				pass
			else:
				succ_code="刷完啦~\n"
				self.Log.insert(1.0,succ_code)
				self.Log.update()
				self.Stop_Cmd()
				StopSignal=False

	def Stop_Cmd(self, event=None):
		global PROCESSING
		global StopSignal
		if not PROCESSING:
			return
		self.Log.update()
		PROCESSING = False
		self.Log.insert(1.0,'>>>>>>已停止<<<<<<\n')
		self.Log.update()
		StopSignal=True
		return

	def Refresh_Cmd(self, event=None):
		self.vcode.delete(0,END)
		try:
			conn=httplib.HTTPConnection("222.30.32.10",timeout=3)
			conn.request("GET","http://222.30.32.10/ValidateCode","",headers)
			res=conn.getresponse()
			f=open("ValidateCode.jpg","w+b")
			f.write(res.read())
			f.close()
			conn.close()
		except:
			return False
		#self.photo.close()
		self.photo=PIL.Image.open("ValidateCode.jpg")
		self.im = PIL.ImageTk.PhotoImage(self.photo)
		self.V_Pic= Label(self.top,image = self.im)
		self.V_Pic.place(relx=0.05, rely=0.203, relwidth=0.327, relheight=0.053)
		return True

	def select_course(self, course_list, mode):
		selected_list=[]
		if mode=='queue':
			for i in range(min(4,len(course_list))):
				selected_list.append(course_list.pop(0))
			return (selected_list,course_list)
		else:
			for i in range(min(4,len(course_list))):
				selected_list.append(course_list.pop())
			return (selected_list,course_list)

	def merge_course_list(self, course_list, selected_list, mode):
		if mode=='queue':
			for i in range(len(selected_list)):
				course_list.append(selected_list.pop(0))
			return course_list
		else:
			for i in range(len(selected_list)):
				course_list.append(selected_list.pop())
			return course_list

	def PostData(self, post_course_list, count):
		self.Log.delete(20.0,END)
		self.Log2.delete(20.0,END)
		NEXT_POST = time.time()+5
		course=[]
		for i in range(4):
			course.append('')
		for i in range(len(post_course_list)):
			course[i]=post_course_list[i]
		info='第'+str(count)+'次抢课进行中……正在抢：\n'
		for i in range(len(post_course_list)):
			info += (course[i]+' '+self.GetName(course[i])+'\n')
		self.Log.insert(1.0,info)
		self.Log.update()

		postdata="operation=xuanke&index="
		for i in range(4):
			if i<len(course):
				postdata += ("&xkxh"+str(i+1)+"="+course[i])
			else:
				postdata += ("&xkxh"+str(i+1)+"=")
		postdata += "&departIncode=%25&courseindex="
		try:
			try:
				conn=httplib.HTTPConnection("222.30.32.10",timeout=5)
				conn.request("POST",UpUrl,postdata,headers)
				res=conn.getresponse()
			except:
				self.Log.insert(1.0,"网络连接错误。请检查网络连接！\n")
				return post_course_list
			#太久不管的话cookie会失效
			if res.status == 302:
				self.Log.insert(1.0,"登录超时，请重新登录\n")
				Login_S = False
				return post_course_list
			response=res.read()
			content=response.decode("gbk").encode('utf-8')
		except:
			return post_course_list
		#----------------------------------------------------------
		#----------------------抓取-------------
		reg = re.compile(u'"BlueBigText">[\s\S]*</font>')
		Data = reg.findall(content)
		#---------------截取--------------------\
		if Data != []:
			Data=Data[0]
			Data=Data[14:]
			Data=Data[:-10]
			Err = re.compile(r'无效，')
			Err = Err.findall(Data)
			#------------是否存在无效序号---------
			if Err != [ ]:
				self.Log2.insert(1.0,('有无效序号无法判断\n'))
				self.Log2.update()
				self.Log.insert(1.0,('>>>>>>已停止<<<<<<\n\nERROR!\n\n'))
				self.Log.update()
				return
		else:
			Data = ''
		#---------------End---------------------
		#----------------------------------------
		fail_course=[]
		for course_code in post_course_list:
			if not self.CheckSelected(course_code):
				fail_course.append(course_code)
			else:
				self.Log2.insert(1.0,(course_code+' '+self.GetName(course_code)+'\n'))
		self.Log2.update()
		#--------------------输出选课系统状态返回---------------------
		self.Log.insert(1.0,(Data+'\n'))
		self.Log.update()
		if len(fail_course)==0:
			self.Log.insert(1.0,('刷完啦~\n'))
			self.Log.update()
			return fail_course
		#-----------------------------------------------------------
		if PROCESSING==False:
			return fail_course
		self.Log.insert(1.0,'-----------------休眠5秒--------------------\n')
		Wait = (NEXT_POST-time.time())/20
		#-------------保持刷新防止假死------------
		if Wait>0:
			for j in range (0,20):
				self.Log.update()
				time.sleep(Wait)
				self.Log.update()
				if PROCESSING==False:
					return fail_course
		self.CacheRefresh()
		#---------------------------------------------
		return fail_course


	def GetCourseCode(self):
		course_code=[]
		tmp_code=self.Text12.get()
		if tmp_code!='':
			course_code.append(tmp_code)
		tmp_code=self.Text11.get()
		if tmp_code!='':
			course_code.append(tmp_code)
		tmp_code=self.Text10.get()
		if tmp_code!='':
			course_code.append(tmp_code)
		tmp_code=self.Text9.get()
		if tmp_code!='':
			course_code.append(tmp_code)
		tmp_code=self.Text8.get()
		if tmp_code!='':
			course_code.append(tmp_code)
		tmp_code=self.Text7.get()
		if tmp_code!='':
			course_code.append(tmp_code)
		tmp_code=self.Text6.get()
		if tmp_code!='':
			course_code.append(tmp_code)
		tmp_code=self.Text5.get()
		if tmp_code!='':
			course_code.append(tmp_code)
		tmp_code=self.Text4.get()
		if tmp_code!='':
			course_code.append(tmp_code)
		tmp_code=self.Text3.get()
		if tmp_code!='':
			course_code.append(tmp_code)
		tmp_code=self.Text2.get()
		if tmp_code!='':
			course_code.append(tmp_code)
		tmp_code=self.Text1.get()
		if tmp_code!='':
			course_code.append(tmp_code)
		return course_code

	def CheckLogin(self):
		global	Login_S
		return Login_S

	def CheckSystemStatus(self):
		global PROCESSING
		XuanKeButton = re.compile(u'''<input type="button" name="xuanke"''')
		XKButton = []
		list=''
		try:
			conn=httplib.HTTPConnection("222.30.32.10",timeout=10)
			conn.request("GET","http://222.30.32.10/xsxk/selectMianInitAction.do",list,self.headers)
			XKButton = XuanKeButton.findall(conn.getresponse().read().decode("gbk").encode('utf-8'))
			if XKButton == [] :
				return False
			else:
				return True
		except:
			self.Log.insert(1.0,"网络连接错误，无法连接到选课系统。请检查网络连接！\n")
			if ReLoadData():
				self.Refresh_Cmd()
			else:
				PROCESSING=False
				return False
		return False

	def wait_for_system(self):
		global PROCESSING
		while not self.CheckSystemStatus():
			if not PROCESSING:
				return
			self.Log.insert(1.0,"选课系统还没开~3秒后重试~\n")
			self.Log.update()
			for j in range (0,12):
				time.sleep(0.25)
				self.Log.update()
				if not PROCESSING:
					return
		return
	# =================
	def CacheRefresh(self):
		global Cache
		#print Cache
		for i in Cache.keys():
			if Cache[i]["TTL"] < time.time():
				del Cache[i]
		#print Cache
		return None
	def CacheSet(self,key,value,TTL=3600):
		global Cache
		Cache[key] = {"value":value,"TTL":time.time()+TTL}
		#print Cache
		return None
	def CacheGet(self,key):
		global Cache
		try:
			return Cache[key]["value"]
		except:
			return None
	# =================
	def GetName(self,c_code):
		if c_code == "":
			return ""
		value = self.CacheGet(c_code)
		if value:
			return value
		h={
			'Host': 'jwc.nankai.edu.cn',
			'Connection': 'keep-alive',
			'Cache-Control': 'max-age=0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Origin': 'http://jwc.nankai.edu.cn',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Referer': 'http://jwc.nankai.edu.cn/apps/xksc/index.asp',
			'Accept-Encoding': 'gzip,deflate,sdch',
			'Accept-Language': 'zh-CN,zh;q=0.8'
		}
		try:
			conct=httplib.HTTPConnection('jwc.nankai.edu.cn',timeout=3)
			formdata='strsearch='+c_code+'&radio=1&Submit=%CC%E1%BD%BB'
			conct.request('POST','http://jwc.nankai.edu.cn/apps/xksc/search.asp',formdata,h)
			contnt=conct.getresponse().read().decode("gb2312")
			conct.close()
		except:
			return "教务处网站错误"
		pos=contnt.find('</TD></TR><TR><TD>')
		if pos == -1:
			value =  "wrong_course"
		else:
			contnt=contnt[pos:]
			value = re.findall(u"[0-9\u4e00-\u9fa5\uFF00-\uFFEF\-]+",contnt)[1].encode('utf8')
		self.CacheSet(c_code,value,600)
		return value

	def illegal_list(self, check_list):
		illegal_course=[]
		illegal_info=[]
		for i in range(len(check_list)):
			name=self.GetName(check_list[i])
			if (name=="wrong_course"):
				illegal_course.append(check_list[i])
				illegal_info.append(name)
		return (illegal_course,illegal_info)

	def CheckSelected(self, course_code):
		name = self.GetName(course_code)
		try:
			conn = httplib.HTTPConnection('222.30.32.10',timeout=20)
			conn.request('GET','http://222.30.32.10/xsxk/selectedAction.do?operation=kebiao','',self.headers)
			content = conn.getresponse().read()#.decode("gb2312")
			conn.close()
		except:
			return False
		if content.find(name) != -1:
			return True
		return False

if __name__ == "__main__":
	try:
		f=open("ValidateCode.jpg","r")
	except:
		#f=open("ValidateCode","r")
		ff=open("ValidateCode.jpg","w+b")
		#d=f.read()
		#ff.write(d)
		#f.close()
		ff.close()
	top = Tk()
	Application(top).mainloop()
