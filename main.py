import json
from time import time
import tkinter.messagebox
import time

import selenium
from guimodel import gui_model
from PixivImageSelecter import Pixiv_Select
import threading
import os

First_in = False
History_Use = False

def Update_Data():
  global History_Use
  if History_Use:
    gui.startSelectFlag=True
  gui.Page_1_Flag = PixivSelect.CookieUpdateFlag
  if not gui.startSelectFlag:
    gui.Page_2_Flag = PixivSelect.CookieLoadSuccessFlag
  PixivSelect.useraccount = gui.AccountEntryText.get()
  PixivSelect.userpassword = gui.PasswordEntryText.get()
  PixivSelect.GuiInputDoneFlag = gui.AccountInfoInputDone
  gui.CookieLoadEndFlag = PixivSelect.CookieLoadSuccessFlag
  gui.RunInErrorCallBackFlag = PixivSelect.ErrorStopFlag
  gui.ErrorDetaillInfo = PixivSelect.ErrorDetailInfo
  gui.ProgressDisplay = PixivSelect.ProgressDisplay
  gui.ProgressRateDisplay = PixivSelect.ProgressRateDisplay
  gui.currentImageInfo=PixivSelect.currentImageInfo

  Run_PixivSelect(gui.startSelectFlag)

def Run_PixivSelect(flag):
  global First_in,History_Use
  if flag and not First_in:
    First_in = True
    if not History_Use:
      PixivSelect.PixivImageSearchConfig = gui.config
    else:
      gui.Page_3_Flag=True

    PixivSelect.MainTarget_Tag = PixivSelect.PixivImageSearchConfig["MainTag"]
    PixivSelect.Ignore_Tags = PixivSelect.PixivImageSearchConfig["IgnoreTagTextList"]
    PixivSelect.Target_Tags = PixivSelect.PixivImageSearchConfig["UseTagTextList"]
    Pixiv_Select_thread = threading.Thread(target=PixivSelect.Pixiv_ImageSeach)
    Pixiv_Select_thread.setDaemon(True)
    Pixiv_Select_thread.start()

if __name__ == "__main__":

    tkinter.messagebox.showinfo(title = '提示',message='需要搭配VPN食用！')
    gui = gui_model()
    
    PixivSelect = Pixiv_Select()

    check_cookie_thread = threading.Thread(target=PixivSelect.Check_Cookies_File)
    check_cookie_thread.setDaemon(True)
    check_cookie_thread.start()

    
    if os.path.exists("./History_Config.json") and os.path.exists("./History_Data.json"):
        ContinueLastTaskFlag = tkinter.messagebox.askyesno(title = '提示',message='是否继续上次任务？')
        if ContinueLastTaskFlag:
          History_Use=True
          with open("./History_Config.json","r") as f:
           config = f.readlines()
          with open("./History_Data.json","r") as f:
           data = f.readlines()
          PixivSelect.PixivImageSearchConfig = json.loads("".join(config)) 
          data = json.loads("".join(data)) 
          PixivSelect.ImageTagSelectPass_ID_List = data["ImageTagSelectPass_ID_List"]
          PixivSelect.id_SaveList = data["id_SaveList"]
          PixivSelect.ProgressDisplay = data["Progress"]
          PixivSelect.PageNow = data["SearchPage"]
          PixivSelect.RateCountNow = data["RateCount"]
        else:
          os.remove("./History_Config.json")
          os.remove("./History_Data.json")
          pass

    
    gui.TimerFunction.append(Update_Data)
    gui.TimerFunction.append(gui.Gui_Update)
    gui.TimerFunction.append(gui.MessageTips_Callback)
    gui.TimerFunction.append(gui.MessageErrorTips_Callback)
    gui.Gui_Create()





    
    


    