#!/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import division
Ver = 'Ver 3.0.1 With OCR & RSA (20150915)'

import C
import re
import os, sys
import time
import StringIO
from xkocr import OCR
from xuanke_core import Xuanke

#----------------------------------------------------

OCR_OBJ = OCR.Val_to_Str(os.path.split(os.path.realpath(__file__))[0]+"/dump-fuck.txt")


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

import PIL.Image, PIL.ImageTk 

class Application_ui(Frame):
	#这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
	def __init__(self, vcode_img, master=None):
		Frame.__init__(self, master)
		self.vcode_img = vcode_img
		self.master.title('一键刷课 for NKU V3.0 Basic')
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

		self.photo=PIL.Image.open(self.vcode_img)
		self.im = PIL.ImageTk.PhotoImage(self.photo)
		self.V_Pic= Label(self.top,image = self.im)
		self.V_Pic.place(relx=0.05, rely=0.203, relwidth=0.327, relheight=0.053)


class Application(Application_ui):
	#这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
	def __init__(self, master=None): #Done
		self.Xuanke_obj = Xuanke()
		Application_ui.__init__(self, self.Xuanke_obj.vcode , master)
		if not self.Xuanke_obj.NetWork:
           			self.InsLog(u"不能连接到选课系统,请检查网络并重启", self.Log)
		self.isInLoop = False

	def InsLog(self, Text, Target = None): #Done
		T = time.strftime("%H:%M:%S")
		Target = Target or self.Log
		Target.delete(20.0,END)
		Target.insert(1.0, "%s - %s"%(T, Text if (Text and Text[-1] == "\n") else Text+"\n" ))
		Target.update()

	def Login_Cmd(self, event=None): #Done

		ID=self.ID.get()
		passwd=self.PassWord.get()
		v_code=self.vcode.get()
		Login_Status = self.Xuanke_obj.Login(ID, passwd, v_code)
		self.InsLog(Login_Status["Val"], self.Log)

	def GetCourseCode(self): #Done
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

	def Start_Cmd(self, event=None):

		self.Log.delete(0.0, END)
		if not self.Xuanke_obj.CheckLogin():
			self.InsLog(u"尚未登录！", self.Log)
			return
		#------------------------------------------------------------------
		course=self.GetCourseCode()
		if course==None:
			self.InsLog(u"请输入课程代号", self.Log)
			return

		illegal=self.illegal_list(course)
		if illegal[0]!=[]:
			err_code="以下课号有误：\n"
			for i in range(len(illegal[0])):
				err_code+=illegal[0][i]+' '+illegal[1][i]+'\n'
			err_code+="请核对后重新开始！"
			self.InsLog(err_code, self.Log)
			return

		self.Log.insert(1.0,"Starting........Connecting............\n")
		self.Log.update()
		#------------------------------------------------------------------
		use_queue=True
		mode='queue'
		
		if self.Var.get()=='1' or self.Var.get()=='':
			use_queue=True
		else:
			use_queue=False

		#Loop of the Post
		self.isInLoop = True
		count=0
		while self.isInLoop:
			count += 1
			if use_queue:
				mode='queue'
			else:
				mode='stack'
			post_course,course=self.select_course(course,mode)
			try:
				fail_course=self.PostData(post_course,count)
			except KeyboardInterrupt:
				self.Log.insert(1.0,"KeyboardInterrupt\n")
			course=self.merge_course_list(course,fail_course,mode)
			if len(course)>0:
				pass
			else:
				succ_code="刷完啦~\n"
				self.Log.insert(1.0,succ_code)
				self.Log.update()
				self.Stop_Cmd()

	def Stop_Cmd(self, event=None):
		if not self.isInLoop:
			return
		self.Log.update()
		self.isInLoop = False
		self.Log.insert(1.0,'>>>>>>已停止<<<<<<\n')
		self.Log.update()
		return

	def Refresh_Cmd(self, event=None):
		self.vcode.delete(0,END)
		self.Xuanke_obj.RefreshAll()
		self.photo=PIL.Image.open(self.Xuanke_obj.vcode)
		self.im = PIL.ImageTk.PhotoImage(self.photo)
		self.V_Pic= Label(self.top,image = self.im)
		self.V_Pic.place(relx=0.05, rely=0.203, relwidth=0.327, relheight=0.053)
		
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
		try:
			if not self.wait_for_system():
				return post_course_list
		except:
			self.InsLog("Check System Status Error", self.Log)
			return post_course_list
		NEXT_POST = time.time()+5
		course=[]
		for i in range(4):
			course.append('')
		for i in range(len(post_course_list)):
			course[i]=post_course_list[i]
		info='第'+str(count)+'次抢课进行中……正在抢：\n'
		for i in range(len(post_course_list)):
			info += (course[i]+' '+self.Xuanke_obj.Get_Course_Name(course[i])+'\n')
		self.Log.insert(1.0,info)
		self.Log.update()
		#-------------------------
		try:
			Status = self.Xuanke_obj.Xuanke(post_course_list)
		except:
			raise
			Status = {"Err":True, "Val":"Unkown False"}

		if Status["Err"]:
			fail_course = post_course_list
			self.InsLog(Status["Val"],self.Log)
		else:
			fail_course = Status["Val"][1]["UnSelected"]
			self.InsLog(Status["Val"][0], self.Log)

			for Selected_Course in Status["Val"][1]["Selected"]:
				self.Log2.insert(1.0, Selected_Course+' '+self.Xuanke_obj.Get_Course_Name(Selected_Course)+'\n')
				self.Log2.delete(20.0,END)
				self.Log2.update()

		self.Log.insert(1.0,'-----------------休眠5秒--------------------\n')
		Wait = (NEXT_POST-time.time())/20
		#-------------保持刷新防止假死------------
		if Wait>0:
			for j in range (0,20):
				self.Log.update()
				time.sleep(Wait)
				self.Log.update()
				if self.isInLoop==False:
					return fail_course
		#---------------------------------------------
		return fail_course

	

	def wait_for_system(self):
		while not self.Xuanke_obj.CheckSystemStatus():
			if not self.isInLoop:
				return False
			self.InsLog("选课系统还没开~3秒后重试~\n", self.Log)
			for j in range (0,12):
				time.sleep(0.25)
				self.Log.update()
				if not self.isInLoop:
					self.Stop_Cmd()
					return False
		return True


	def illegal_list(self, check_list):   #Done
		illegal_course=[]
		illegal_info=[]
		for i in range(len(check_list)):
			name=self.Xuanke_obj.Get_Course_Name(check_list[i])
			if (name=="wrong_course"):
				illegal_course.append(check_list[i])
				illegal_info.append(name)
		return (illegal_course,illegal_info)


if __name__ == "__main__":
	top = Tk()
	canvas = Canvas(top,width = 640, height = 480, bg = '#E6E6E6')
	canvas.pack(expand = YES, fill = BOTH)

	Application(top).mainloop()
