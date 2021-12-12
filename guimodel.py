import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.constants import S
from tkinter.font import families
import tkinter.messagebox
import os
import time

Main_Root = tk.Tk()

class gui_model:
    
    def __init__(self):
        super().__init__()
        self.MainRoot = Main_Root
        self.TimerFunction=[]
        self.TimerFunctionArgs=[]
        
        self.Page_1_Flag = False
        self.Page_2_Flag = False
        self.Page_3_Flag = False

        self.Page_1_Flag_Last = False
        self.Page_2_Flag_Last = False
        self.Page_3_Flag_Last = False

        self.AccountInfoInputDone = False

        self.CookieLoadEndFlag = False

        self.RunInErrorCallBackFlag = False
        self.ErrorDetaillInfo=""

        self.SaveSelectPath = "./PixivImageSave"

        self.IgnoreTagTextList = []
        self.UseTagTextList = []
        self.MainTags  = ""

        self.config = {}

        self.startSelectFlag = False

        self.ProgressDisplay= 0

        self.RunStateLabelTextList = ["正在筛选画廊Tag信息","正在筛选画廊详细信息","正在保存图片"]

        self.ProgressRateDisplay = 0

        self.currentImageInfo=""

    def InitClassFunction(self):
        pass

    def TkValueCreateHandle(self):
        self.LinkButtonText = tk.StringVar()
        self.LinkButtonText.set("登录")

        self.ProgressRateDisplayText = tk.StringVar()
        self.ProgressRateDisplayText.set(f"{self.ProgressRateDisplay}%")

        self.currentImageInfoText = tk.StringVar()
        self.currentImageInfoText.set("")

        self.RunStateLabelText = tk.StringVar()
        self.RunStateLabelText.set(self.RunStateLabelTextList[self.ProgressDisplay])

        self.AccountEntryText = tk.StringVar()
        self.AccountEntryText.set("")

        self.PasswordEntryText = tk.StringVar()
        self.PasswordEntryText.set("")

        self.MainUseTagEntryText = tk.StringVar()
        self.MainUseTagEntryText.set("")

        self.RunTimeUpdateText = tk.StringVar()
        self.RunTimeUpdateText.set("")

        self.LikeCountLimitEntryText = tk.IntVar()
        self.LikeCountLimitEntryText.set(0)

        self.BookMarkCountLimitEntryText = tk.IntVar()
        self.BookMarkCountLimitEntryText.set(0)

        self.ViewCountLimitEntryText = tk.IntVar()
        self.ViewCountLimitEntryText.set(0)

        self.SearchMaxPageSetEntryText = tk.IntVar()
        self.SearchMaxPageSetEntryText.set(0)

        self.ProgressDisplayText = tk.IntVar()
        self.ProgressDisplayText.set(0)

        self.UseTargetTagListCheckButtonVar = tk.BooleanVar()
        self.UseTargetTagListCheckButtonVar.set(False)
        self.UseIgnoreTagListCheckButtonVar = tk.BooleanVar()
        self.UseIgnoreTagListCheckButtonVar.set(False)
        self.LikeCountEnableCheckbuttonVar = tk.BooleanVar()
        self.LikeCountEnableCheckbuttonVar.set(False)
        self.BookMarkCountEnableCheckbuttonVar = tk.BooleanVar()
        self.BookMarkCountEnableCheckbuttonVar.set(False)
        self.ViewCountCountEnableCheckbuttonVar = tk.BooleanVar()
        self.ViewCountCountEnableCheckbuttonVar.set(False)

        self.SearchMaxPageSetEntryText.set(1000)
        self.ProgressDisplayText.set(self.ProgressDisplay)

    def Create_MainWindows(self):
        if self.Page_1_Flag:
            self.MainRoot.geometry("290x160")
            self.MainRoot.title('PixivSelecterLogin')

        if self.Page_2_Flag:
            self.Page_1_Flag=False
            self.MainRoot.geometry("330x515")
            self.MainRoot.title('PixivSelecterConfig')

        if self.Page_3_Flag:
            self.Page_2_Flag=False
            self.MainRoot.geometry("260x160")
            self.MainRoot.title('PixivSelecterRun')

    def Create_Button(self):
        if self.Page_1_Flag:
            self.LoginButton=tk.Button(self.MainRoot,textvariable=self.LinkButtonText,command=self.LoginButton_CallBack,width=10)
            self.LoginButton.place(x=100,y=100)
        elif self.Page_2_Flag:
            self.SavePathSelectButton = tk.Button(self.MainRoot,text="选择保存路径",command=self.SavePathSelectButton_CallBack)
            self.SavePathSelectButton.place(x=70,y=460)

            self.StartSelectButton = tk.Button(self.MainRoot,text="开始色色的！",command=self.StartSelectButton_CallBack)
            self.StartSelectButton.place(x=170,y=460)

    def Create_Label(self):
        if self.Page_1_Flag:

            self.AccountLabel=tk.Label(self.MainRoot,text="账号:")
            self.PasswordLabel=tk.Label(self.MainRoot,text="密码:")
            self.PasswordLabel.place(x=42,y=20)
            self.AccountLabel.place(x=42,y=60)

        if self.Page_2_Flag:
            
            self.MainUseTagLabel=tk.Label(self.MainRoot,text="主要搜索标签:")
            self.MainUseTagLabel.place(x=20,y=20)
            self.MainUseTagLabel=tk.Label(self.MainRoot,text="次要搜索标签(可添加多个，用,号隔开):")
            self.MainUseTagLabel.place(x=20,y=50)
            self.MainUseTagLabel=tk.Label(self.MainRoot,text="屏蔽标签(可添加多个，用,号隔开):")
            self.MainUseTagLabel.place(x=20,y=145)

            self.TipsLabel=tk.Label(self.MainRoot,text="画廊热度筛选设置：")
            self.TipsLabel.place(x=20,y=245)
            self.LikeCountLabel=tk.Label(self.MainRoot,text="喜欢数:")
            self.LikeCountLabel.place(x=30,y=270)
            self.BookMarkCountLabel=tk.Label(self.MainRoot,text="订阅数:")
            self.BookMarkCountLabel.place(x=30,y=295)
            self.ViewCountLabel=tk.Label(self.MainRoot,text="浏览量:")
            self.ViewCountLabel.place(x=30,y=320)
            self.TipsOtherSettingLabel=tk.Label(self.MainRoot,text="其他设置：")
            self.TipsOtherSettingLabel.place(x=20,y=345)
            self.R18SetLabel=tk.Label(self.MainRoot,text="R18搜索设置:")
            self.R18SetLabel.place(x=25,y=370)
            self.SaveModeSetLabel=tk.Label(self.MainRoot,text="保存模式:")
            self.SaveModeSetLabel.place(x=25,y=395)
            self.SearchMaxPageSetLabel=tk.Label(self.MainRoot,text="最大搜索页数:")
            self.SearchMaxPageSetLabel.place(x=25,y=420)

        if self.Page_3_Flag:

            self.RunStateLabel=tk.Label(self.MainRoot,textvariable=self.RunStateLabelText)
            self.RunStateLabel.place(x=10,y=25)

            self.TimeDisplayLabel=tk.Label(self.MainRoot,textvariable=self.RunTimeUpdateText)
            self.TimeDisplayLabel.place(x=10,y=45)

            self.ProgressDisplayTipsLabel=tk.Label(self.MainRoot,text="当前进度：")
            self.ProgressDisplayTipsLabel.place(x=10,y=65)

            self.ProgressRateDisplayLabel =tk.Label(self.MainRoot,textvariable=self.ProgressRateDisplayText) 
            self.ProgressRateDisplayLabel.place(x=70,y=65)

            self.currentImageInfoLabel=tk.Label(self.MainRoot,text="正在处理：")
            self.currentImageInfoLabel.place(x=10,y=85)

            self.currentImageInfoTextLabel=tk.Label(self.MainRoot,textvariable=self.currentImageInfoText)
            self.currentImageInfoTextLabel.place(x=70,y=85)
            

    def Create_TextEntry(self):
        if self.Page_2_Flag:

            self.UseTagListTextEntry = tk.Text(self.MainRoot,height=4,width=40)
            self.UseTagListTextEntry.place(x=20,y=80)

            self.IgnoreTagListTextEntry = tk.Text(self.MainRoot,height=3,width=40)
            self.IgnoreTagListTextEntry.place(x=20,y=175)

    def Create_Checkbutton(self):
        if self.Page_2_Flag:

            self.LikeCountEnableCheckbutton = ttk.Checkbutton(self.MainRoot,text ="启用",variable=self.LikeCountEnableCheckbuttonVar,onvalue=True,offvalue = False)
            self.LikeCountEnableCheckbutton.place(x=160,y=270)


            self.BookMarkCountEnableCheckbutton = ttk.Checkbutton(self.MainRoot,text ="启用",variable=self.BookMarkCountEnableCheckbuttonVar,onvalue=True,offvalue = False)
            self.BookMarkCountEnableCheckbutton.place(x=160,y=295)


            self.ViewCountEnableCheckbutton = ttk.Checkbutton(self.MainRoot,text ="启用",variable=self.ViewCountCountEnableCheckbuttonVar,onvalue=True,offvalue = False)
            self.ViewCountEnableCheckbutton.place(x=160,y=320)

            self.IgnoreEnableCheckbutton = ttk.Checkbutton(self.MainRoot,text ="启用屏蔽Tag列表",variable=self.UseIgnoreTagListCheckButtonVar,onvalue=True,offvalue = False,command=self.IgnoreEnableCheckbutton_CallBack)
            self.IgnoreEnableCheckbutton.place(x=20,y=220)

            self.UseTagsEnableCheckbutton = ttk.Checkbutton(self.MainRoot,text ="启用多个Tag列表",variable=self.UseTargetTagListCheckButtonVar,onvalue=True,offvalue = False,command=self.UseTagsEnableCheckbutton_CallBack)
            self.UseTagsEnableCheckbutton.place(x=190,y=220)

    def Create_Combobox(self):
        if self.Page_2_Flag:
            self.SearchModeCombobox = ttk.Combobox(self.MainRoot,values=["全部搜索","无R18","只看R18"],state="readonly",width=10)
            self.SearchModeCombobox.current(0)
            self.SearchModeCombobox.place(x=105,y=370)

            self.SaveModeCombobox = ttk.Combobox(self.MainRoot,values=["Pixiv ID","图片"],state="readonly",width=10)
            self.SaveModeCombobox.current(1)
            self.SaveModeCombobox.place(x=105,y=395)
   
    def Create_Scale(self):
        pass

    def Create_Entry(self):
        if self.Page_1_Flag:
            
            self.AccountEntry=tk.Entry(self.MainRoot,textvariable=self.AccountEntryText,width=20)
            self.PasswordEntry=tk.Entry(self.MainRoot,textvariable=self.PasswordEntryText,width=20)
            
            self.AccountEntry.place(x=80,y=20)
            self.PasswordEntry.place(x=80,y=60)

        if self.Page_2_Flag:
            
            
            self.MainUseTagEntry = tk.Entry(self.MainRoot,textvariable=self.MainUseTagEntryText,width=20)
            self.MainUseTagEntry.place(x=110,y=20)

            self.LikeCountLimitEntry = tk.Entry(self.MainRoot,textvariable=self.LikeCountLimitEntryText,width=10)
            self.LikeCountLimitEntry.place(x=80,y=270)

            self.BookMarkCountLimitEntry = tk.Entry(self.MainRoot,textvariable=self.BookMarkCountLimitEntryText,width=10)
            self.BookMarkCountLimitEntry.place(x=80,y=295)

            self.ViewCountLimitEntry = tk.Entry(self.MainRoot,textvariable=self.ViewCountLimitEntryText,width=10)
            self.ViewCountLimitEntry.place(x=80,y=320)

            self.SearchMaxPageSetEntry = tk.Entry(self.MainRoot,textvariable=self.SearchMaxPageSetEntryText,width=10)
            self.SearchMaxPageSetEntry.place(x=105,y=420)

    def LoginButton_CallBack(self):
        if self.AccountEntryText.get() and self.PasswordEntryText.get():
            self.AccountInfoInputDone = True
            self.LoginButton["state"] = "disable"
        else:
            tk.messagebox.showerror(title = '错误',message='请输入账号密码！')
        pass

    def SavePathSelectButton_CallBack(self):
        setpath = askdirectory()
        if os.path.exists(setpath):
            self.SaveSelectPath = setpath
            tk.messagebox.showinfo("成功",f"保存文件路径设置成功！路径为:{self.SaveSelectPath}")
        else:
            pass
    
    def UseTagsEnableCheckbutton_CallBack(self):
        Entry_Text = self.UseTagListTextEntry.get("1.0",tk.END)
        if len(Entry_Text)<=1:
            self.UseTargetTagListCheckButtonVar.set(False)
            tk.messagebox.showerror(title = '错误',message='请输入需要包含的标签！')

        
    def IgnoreEnableCheckbutton_CallBack(self):
        Entry_Text = self.IgnoreTagListTextEntry.get("1.0",tk.END)
        if len(Entry_Text)<=1:
            self.UseIgnoreTagListCheckButtonVar.set(False)
            tk.messagebox.showerror(title = '错误',message='请输入需要屏蔽的标签！')

    def StartSelectButton_CallBack(self):
        self.MainTags = self.MainUseTagEntryText.get()
        if self.MainTags == "":
            tk.messagebox.showerror(title = '错误',message='请输入主要搜索标签！')
            return
        if self.SearchModeCombobox.get() == "全部搜索":
            SearchMode = "all"
        elif self.SearchModeCombobox.get() == "无R18":
            SearchMode = "safe"
        elif self.SearchModeCombobox.get() == "只看R18":
            SearchMode = "r18"

        if self.SearchMaxPageSetEntryText.get()<1:
            MaxPage = -1
        else:
            MaxPage = self.SearchMaxPageSetEntryText.get()

        if self.BookMarkCountEnableCheckbuttonVar.get():
            LimitBookMarkCount = self.BookMarkCountLimitEntryText.get()
        else:
            LimitBookMarkCount = -1

        if self.LikeCountEnableCheckbuttonVar.get():
            LimitLikeCount = self.LikeCountLimitEntryText.get()
        else:
            LimitLikeCount = -1
        
        if self.ViewCountCountEnableCheckbuttonVar.get():
            LimitViewCount = self.ViewCountLimitEntryText.get()
        else:
            LimitViewCount = -1

        if self.SaveModeCombobox.get() == "图片":
            SaveMode = 1
        else:
            SaveMode = 0


        if self.UseIgnoreTagListCheckButtonVar.get():
            self.IgnoreTagTextList = self.IgnoreTagListTextEntry.get("1.0",tk.END).replace("，",',').replace("\n","").replace(" ","").split(",")
        else:
            self.IgnoreTagTextList = []

        if self.UseTargetTagListCheckButtonVar.get():
            self.UseTagTextList = self.UseTagListTextEntry.get("1.0",tk.END).replace("，",',').replace("\n","").replace(" ","").split(",")
        else:
            self.UseTagTextList = []

        self.config = {
         "SearchMode":SearchMode,
         "MainTag":self.MainTags,
         "SearchType":"TagMode",
         "UseIgnoreList":self.UseIgnoreTagListCheckButtonVar.get(),
         "IgnoreTagTextList":self.IgnoreTagTextList,
         "UseTargetList":self.UseTargetTagListCheckButtonVar.get(),
         "UseTagTextList":self.UseTagTextList,
         "SearchMaxPages":MaxPage,
         "TargetListTagUseMinLimit":1,
         "LimitBookMarkCount":LimitBookMarkCount,
         "LimitLikeCount":LimitLikeCount,
         "LimitViewCount":LimitViewCount,
         "SaveMode":SaveMode,
         "UserSetSavePath":self.SaveSelectPath,
      }

    
        self.startSelectFlag = True
        self.Page_2_Flag = False
        self.Page_3_Flag = True
        self.StartSelectButton["state"] = "disable"
        self.MainRoot.after_cancel(self.TimeEvent)
        self.MainRoot.destroy()
        self.MainRoot = tk.Tk()
        self.TkValueCreateHandle()
        self.TimeEvent = self.MainRoot.after(5,self.TimerEvent_CallBack)
        self.MainRoot.mainloop()

        
    def TimerEvent_CallBack(self):

        for Function in self.TimerFunction:
            Function()
            
        self.RunTimeUpdateText.set(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.ProgressDisplayText.set(self.ProgressDisplay)
        self.RunStateLabelText.set(self.RunStateLabelTextList[self.ProgressDisplay])
        self.ProgressRateDisplayText.set(f"{self.ProgressRateDisplay}%")
        self.currentImageInfoText.set(self.currentImageInfo)

        self.TimeEvent = self.MainRoot.after(5,self.TimerEvent_CallBack)

    def Gui_Update(self):
        
        if self.Page_1_Flag_Last != self.Page_1_Flag:

            if not self.Page_1_Flag_Last and self.Page_1_Flag: 
                self.Create_MainWindows()
                self.Create_Button()
                self.Create_Label()
                self.Create_Entry()



        self.Page_1_Flag_Last = self.Page_1_Flag
            
            
        if self.Page_2_Flag_Last != self.Page_2_Flag:
            if self.Page_1_Flag_Last:
                self.Page_1_Flag_Last=False
                self.AccountLabel.destroy()
                self.PasswordLabel.destroy()
                self.AccountEntry.destroy()
                self.PasswordEntry.destroy()
            self.Page_2_Flag_Last = self.Page_2_Flag
            self.Create_MainWindows()
            self.Create_Button()
            self.Create_Label()
            self.Create_Entry()
            self.Create_TextEntry()
            self.Create_Combobox()
            self.Create_Checkbutton()
        
        if self.Page_3_Flag_Last != self.Page_3_Flag:
            self.Page_3_Flag_Last = self.Page_3_Flag
            self.Create_MainWindows()
            self.Create_Label()
            

    def MessageTips_Callback(self):
        if self.CookieLoadEndFlag==True:
            tk.messagebox.showinfo(title = '成功',message="载入登陆数据成功！")
            self.TimerFunction.remove(self.MessageTips_Callback)

    def MessageErrorTips_Callback(self):
        if self.RunInErrorCallBackFlag:
            tk.messagebox.showerror(title = '错误',message=self.ErrorDetaillInfo)
            os._exit(-1)

    def Gui_Create(self):
        self.InitClassFunction()
        self.TkValueCreateHandle()
        self.TimeEvent = self.MainRoot.after(5,self.TimerEvent_CallBack)
        self.MainRoot.mainloop()
