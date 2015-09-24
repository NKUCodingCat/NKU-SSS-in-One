#!/usr/bin/env python
#-*- coding:utf-8 -*-

import C

import os, sys
if sys.version_info[0] == 2:
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    from tkFileDialog import *
    #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  #Python 3.x
    from tkinter import *
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    from tkinter.filedialog import *
    #import tkinter.filedialog as tkFileDialog
    #import tkinter.simpledialog as tkSimpleDialog    #askstring()

import PIL.Image, PIL.ImageTk
import time
import csv
from os.path import expanduser
import PJ



class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, vcode, master=None):
        Frame.__init__(self, master)
        self.master.title('一键评教-NKUCodingCat')
        self.master.geometry('227x343')
        self.Valicode = vcode
        self.createWidgets()


    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.Log = Text(self.top)
        self.Log.place(relx=0.05, rely=0.676, relwidth=0.90, relheight=0.283)

        self.style.configure('TLabel1.TLabel', anchor='w')
        self.Label1 = Label(self.top, text=u'学号', style='TLabel1.TLabel')
        self.Label1.place(relx=0.1, rely=0.07, relwidth=0.25, relheight=0.073)

        self.style.configure('TLabel2.TLabel', anchor='w')
        self.Label2 = Label(self.top, text=u'密码', style='TLabel2.TLabel')
        self.Label2.place(relx=0.1, rely=0.187, relwidth=0.25, relheight=0.073)

        self.style.configure('TLabel3.TLabel', anchor='w')
        self.Label3 = Label(self.top, text=u'验证码', style='TLabel3.TLabel')
        self.Label3.place(relx=0.1, rely=0.303, relwidth=0.25, relheight=0.073)

        self.Text1Var = StringVar(value='')
        self.Text1 = Entry(self.top, textvariable=self.Text1Var)
        self.Text1.place(relx=0.388, rely=0.07, relwidth=0.568, relheight=0.073)

        self.Text2Var = StringVar(value='')
        self.Text2 = Entry(self.top, textvariable=self.Text2Var)
        self.Text2.place(relx=0.388, rely=0.187, relwidth=0.568, relheight=0.073)

        self.Text3Var = StringVar(value='')
        self.Text3 = Entry(self.top, textvariable=self.Text3Var)
        self.Text3.place(relx=0.388, rely=0.303, relwidth=0.568, relheight=0.073)
        self.Text3.bind("<KeyPress-Return>", self.Command1_Cmd)
        self.Text3.bind("<KP_Enter>", self.Command1_Cmd)

        self.Command1 = Button(self.top, text=u'开始评教', command=self.Command1_Cmd)
        self.Command1.place(relx=0.05, rely=0.513, relwidth=0.30, relheight=0.12)

        self.Command2 = Button(self.top, text=u'退出', command=self.Command2_Cmd)
        self.Command2.place(relx=0.75, rely=0.513, relwidth=0.20, relheight=0.12)
        
        self.Command3 = Button(self.top, text=u'导出成绩', command=self.Command3_Cmd)
        self.Command3.place(relx=0.40, rely=0.513, relwidth=0.30, relheight=0.12)
        

        #self.Text4Var = Text(value='Text4')
        self.photo=PIL.Image.open(self.Valicode)
        self.im = PIL.ImageTk.PhotoImage(self.photo)
        self.V_Pic= Label(self.top,image = self.im)
        self.V_Pic.place(relx=0.176, rely=0.42, relwidth=0.604, relheight=0.073)
        


class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        self.P = PJ.PJ()
        self.vcode = self.P.vcode
        self.isLogin = False
        Application_ui.__init__(self, self.vcode , master)
        if not self.P.NetWork:
           self.InsLog(u"不能连接到选课系统,请检查网络并重启")

    def ReloadAll(self):
        self.Text3.delete(0, 'end')
        self.P.RefreshAll()
        self.Valicode = self.P.vcode
        self.photo=PIL.Image.open(self.Valicode)
        self.im = PIL.ImageTk.PhotoImage(self.photo)
        self.V_Pic= Label(self.top,image = self.im)
        self.V_Pic.place(relx=0.176, rely=0.42, relwidth=0.604, relheight=0.073)

    def InsLog(self, Text):
        T = time.strftime("%H:%M:%S")
        self.Log.insert(1.0, "%s - %s"%(T, Text if Text[-1] == "\n" else Text+"\n" ))
        self.Log.delete(20.0,END)
        self.Log.update()
        
    def Log_in(self):
        usr = str(self.Text1.get())
        pwd = str(self.Text2.get())
        vc = str(self.Text3.get())
        self.InsLog(u"测试网络连接。。。。。。")
        if not self.P.NetWork:
            self.InsLog(u"不能连接到选课系统,请检查网络并重启")
            return False
        Login_Status = self.P.Login(usr, pwd, vc)
        self.InsLog(u"登录中。。。。。。。")
        self.isLogin = not Login_Status["Err"]
        if Login_Status["Err"]:
            self.InsLog("Error Occured! "+Login_Status["Val"])
            self.ReloadAll()
            return False
        return True
        
    def Command3_Cmd(self, event=None):
        if self.isLogin:
            pass
        else:
            if not self.Log_in():
                return 
        opt = {
            'defaultextension' : '.csv',
            'filetypes'        : [('all files', '.*'), ('text files', '.csv')],
            'initialdir'       : expanduser("~"),
            'initialfile'      : "%s-%s-scorelist.csv"%(time.strftime("%Y-%m-%d"), str(self.Text1.get()) if str(self.Text1.get()) else "No_usrname") ,
            'parent'           :  top, 
            'title'            : "导出成绩列表至 ..."
        }
        
        A = self.P.Score_Spider()
        if A["Err"]:
            self.InsLog(A["Val"])
        else:
            F_Name = asksaveasfile(mode='w', **opt)
            if not F_Name:
                return
            f_csv = csv.writer(F_Name, lineterminator='\n')
            f_csv.writerows(A["Val"])
            self.InsLog("成绩列表已经导出至%s"%F_Name.name)
        
    def Command2_Cmd(self, event=None):
        #TODO, Please finish the function here!
        self.top.quit()

    def Command1_Cmd(self, event=None):
        #TODO, Please finish the function here!
        if self.isLogin:
            pass
        else:
            if not self.Log_in():
                return 
        self.InsLog(u"开始评教，请稍候。。。。。。")
        try:
            PJ_Status = self.P.PJ(self.InsLog)
        except:
            self.InsLog("Error Occured! "+"Unknown Error")
            self.InsLog("请登录选课系统查看评教状况")
            return
        else:
            if PJ_Status["Err"]:
                self.InsLog("Error Occured! "+PJ_Status["Val"])
                if PJ_Status["Val"] == "Please Login First!":
                    self.isLogin = False
            else:
                self.InsLog("Success! "+PJ_Status["Val"])
            return 

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()

