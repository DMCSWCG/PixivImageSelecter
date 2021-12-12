import os
from tkinter.constants import E
from requests.sessions import RequestsCookieJar
import requests
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.support.ui import WebDriverWait       #WebDriverWait注意大小写
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import re
import random
import time


header_Template= {
	"Host": "www.pixiv.net",
	"referer": "https://www.pixiv.net/",
	"accept-language": "zh-CN,zh;q=0.9",
	"User-Agent":""
}

Chrome_User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
FireFox_User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"


SaveModeType = ["SaveID","SaveImage"]

class Pixiv_Select:
   def __init__(self):
      super().__init__()

      self.webviewerdrive_path = "./" #浏览器驱动路径

      self.webviewer_type="FireFox"
      
      self.login_host_url = "https://accounts.pixiv.net/login"
      
                                                   #此处壁纸可修改为随意标签
      self.cookies_host_url = "https://www.pixiv.net/tags/壁纸/artworks?s_mode=s_tag"
      
      self.usercookiedata_path = "./cookies.json"
      
      self.useraccount = ""
      self.userpassword= ""
      
      self.cookiedataget = RequestsCookieJar()
      
      if self.webviewer_type == "FireFox":
         header_Template["User-Agent"] = FireFox_User_Agent
         self.requests_header = header_Template
      elif self.webviewer_type == "Chrome":
         header_Template["User-Agent"] = Chrome_User_Agent
         self.requests_header = header_Template

      self.Ignore_Tags = []
      self.Target_Tags = []

      self.MainTarget_Tag = ""

      self.MainIgnore_Tag = ""

      self.PixivImageSearchMode = "all"

      self.PixivImageSearchConfig = {
         "SearchMode":self.PixivImageSearchMode,
         "MainTag":self.MainTarget_Tag,
         "SearchType":"TagMode",
         "UseIgnoreList":True,
         "IgnoreTagTextList":self.Ignore_Tags,
         "UseTargetList":False,
         "UseTagTextList":self.Target_Tags,
         "SearchMaxPages":-1,
         "TargetListTagUseMinLimit":1,
         "LimitBookMarkCount":-1,
         "LimitLikeCount":500,
         "LimitViewCount":-1,
         "SaveMode":1,
         "UserSetSavePath":""
      }

      self.id_SaveList = []

      self.ImageTagSelectPass_ID_List = []

      self.ErrorStopFlag=False

      self.CookieUpdateFlag=False

      self.GuiInputDoneFlag = False

      self.CookieLoadSuccessFlag = False

      self.ErrorDetailInfo=""

      self.ProgressDisplay=0

      self.ProgressRateDisplay=0

      self.currentImageInfo=""

      self.PageNow = 1
      self.RateCountNow=0

   def WebViewer_Create(self):
      #TODO: 创建selenium 浏览器对象

      try:
         if self.webviewer_type=="FireFox":
            options = webdriver.FirefoxOptions()
         elif self.webviewer_type=="Chrome":
            options = webdriver.ChromeOptions()
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            
         options.add_argument('--no-sandbox')    
         options.add_argument('--start-maximized')
         #options.add_argument('user-data-dir='+self.userdata_path)
         
      except Exception as e:
         self.PixivClassError_CallBack(e)
      try:
         if self.webviewer_type=="FireFox":
            driver = webdriver.Firefox(options=options)
         elif self.webviewer_type=="Chrome":
            driver = webdriver.Chrome(options=options)
      except Exception as e:
         self.PixivClassError_CallBack(e)

      return driver

   def Update_Cookies(self):
      #TODO: 封装一层方便后续修改
      self.Login_Account()

   def Login_Account(self):
      #TODO: 登陆Pixiv账号

      driver = self.WebViewer_Create()
      try:
         driver.get(self.login_host_url)
         WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,'signup-form ')))
         driver.find_element_by_xpath("(//div[@class='input-field']//input)[1]").send_keys(self.useraccount)
         driver.find_element_by_xpath("(//div[@class='input-field']//input)[2]").send_keys(self.userpassword)
         driver.find_element_by_xpath("//button[@type='submit']").click()
      except Exception as e:
         self.PixivClassError_CallBack(e)
      try:
         WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"(//div[@role='img'])[1]")))
         driver.get(self.cookies_host_url)
         time.sleep(5)
      except Exception as e:
         self.PixivClassError_CallBack(e)

      cookies = driver.get_cookies()
      jsonCookies = json.dumps(cookies)
      with open(self.usercookiedata_path, 'w+') as f:
         f.write(jsonCookies)
      driver.quit()

   def Read_Cookies_data(self):
      #TODO: 读取本地存储的Cookie文件
      
      try:
         with open(self.usercookiedata_path, "r", encoding="utf8") as fp:
               data = fp.readlines()
         cookies = json.loads(data[0])
         RCJar = RequestsCookieJar()
         for cookie in cookies:
            RCJar.set(cookie['name'], cookie['value'])
         self.cookiedataget = RCJar
         self.CookieLoadSuccessFlag = True
      except Exception as e:
         self.PixivClassError_CallBack(e)

   def Check_Cookies_File(self):
      #TODO: 检查是否存在本地Cookie文件和Cookie信息是否失效 Cookie过期时间为1天
      
      if os.path.exists(self.usercookiedata_path):
         with open(self.usercookiedata_path, "r", encoding="utf8") as fp:
            data = fp.readlines()
         cookies = json.loads(data[0])
         for cookie in cookies:
            if cookie["name"] == "first_visit_datetime_pc":
               date = cookie["value"].split("+")[0]
               now_time = time.strftime("%Y-%m-%d", time.localtime())
               if date != now_time:
                  self.CookieUpdateFlag = True
                  while not self.GuiInputDoneFlag:
                     time.sleep(0.5)   
                  self.Update_Cookies()
      else:
         self.CookieUpdateFlag = True
         while not self.GuiInputDoneFlag:
            time.sleep(0.5)   
         self.Update_Cookies()
      self.Read_Cookies_data()         

   def GetImageInfoLists_ByTag(self,Tag,Page):
      #TODO:通过指定Tag获取图片简介列表  成功：返回图片列表信息 失败：返回 None
      
      try:
         List_API_url = f"https://www.pixiv.net/ajax/search/artworks/{Tag}?word={Tag}&order=date_d&mode={self.PixivImageSearchMode}&p={Page}&s_mode=s_tag&type=all&lang=zh"
         image_data_info = requests.get(url=List_API_url,headers=self.requests_header,cookies=self.cookiedataget,timeout=30).content
         image_data_info_json = json.loads(image_data_info)
      except Exception as e:
         self.PixivClassError_CallBack(e)

      if image_data_info_json["error"] == False:
         return image_data_info_json
      self.PixivClassError_CallBack("Pixiv错误! 图片列表获取失败！")
      
   def GetImageDetailInfo_ById(self,target_id):
      
      
      try:
         LikeCount_API_Url = f"https://pixiv.net/ajax/illust/{target_id}"
         DetailInfoData = requests.get(LikeCount_API_Url,headers=self.requests_header,cookies=self.cookiedataget,timeout=30).content.decode('utf-8')
         DetailInfoData = json.loads(DetailInfoData)
         if DetailInfoData["error"]==True:
            return -1,-1,-1,""
      except Exception as e:
         self.PixivClassError_CallBack(e)

      return DetailInfoData["body"]["bookmarkCount"],DetailInfoData["body"]["likeCount"],DetailInfoData["body"]["viewCount"],DetailInfoData["body"]["illustTitle"]

   def SearchImage_ByTags_CallBack(self,StartData):
      
      Max_page = int(int(StartData["body"]["illustManga"]["total"])/60)+1
      if Max_page > 1000:
         Max_page = 1000
      if self.PixivImageSearchConfig["SearchMaxPages"] > Max_page or self.PixivImageSearchConfig["SearchMaxPages"]==-1:
         self.PixivImageSearchConfig["SearchMaxPages"] = Max_page

      
      if self.ProgressDisplay==0:
         #筛选Tags 
         
         RateCount=0
         if self.RateCountNow!=0:
            RateCount = self.RateCountNow

         Page_Start = 1
         if self.PageNow!=1:
            Page_Start = self.PageNow

         for Page_Index in range(Page_Start,self.PixivImageSearchConfig["SearchMaxPages"]+1):
            RateCount+=1
            self.PageNow = Page_Index
            if Page_Index == 1:
               Info_List = StartData["body"]["illustManga"]["data"]
            else:
               Info_List = self.GetImageInfoLists_ByTag(self.MainTarget_Tag,Page_Index)["body"]["illustManga"]["data"]
            
            for Info in Info_List:
               Pass_Flag = False
               Count = 0
               self.currentImageInfo = str(Info["id"])
               for tag in Info["tags"]:
                  
                  if self.PixivImageSearchConfig["UseIgnoreList"] == True and len(self.Ignore_Tags)>=1:
                     if tag in self.Ignore_Tags:
                        break
                  
                  if self.MainIgnore_Tag!="" and tag == self.MainIgnore_Tag:
                     break
                  
                  if self.PixivImageSearchConfig["UseTargetList"] == True and len(self.Target_Tags)>=1:
                     if tag in self.Target_Tags:
                        Count+=1

                     if Count>=self.PixivImageSearchConfig["TargetListTagUseMinLimit"]:
                        Pass_Flag = True
                  else:
                     Pass_Flag = True

               if Pass_Flag == True:
                  self.ImageTagSelectPass_ID_List.append(Info["id"])  
            self.ProgressRateDisplay = int((RateCount/self.PixivImageSearchConfig["SearchMaxPages"])*100)
         
         self.ProgressDisplay=1
         self.id_SaveList = []
         

      if self.ProgressDisplay==1:
         RateCount=0
         if self.RateCountNow!=0:
            RateCount = self.RateCountNow
         listlen = len(self.ImageTagSelectPass_ID_List)
         for image_id in self.ImageTagSelectPass_ID_List:
            self.currentImageInfo = str(image_id)
            RateCount+=1
            self.RateCountNow=RateCount
            bookmarkCount,likeCount,viewCount,ImagesTitle = self.GetImageDetailInfo_ById(image_id)
            
            if bookmarkCount== -1 and likeCount== -1 and viewCount== -1:
               self.PixivClassError_CallBack("Network Error!")
               
            if bookmarkCount>= self.PixivImageSearchConfig["LimitBookMarkCount"] and likeCount>= self.PixivImageSearchConfig["LimitLikeCount"] and viewCount>= self.PixivImageSearchConfig["LimitViewCount"]:
               self.id_SaveList.append((image_id,ImagesTitle))
            self.ImageTagSelectPass_ID_List.remove(image_id)
            
            self.ProgressRateDisplay = int((RateCount/listlen)*100)
         
         self.ProgressDisplay=2

      if self.ProgressDisplay==2:
         RateCount=0
         if self.RateCountNow!=0:
            RateCount = self.RateCountNow

         if SaveModeType[self.PixivImageSearchConfig["SaveMode"]] == "SaveID":
            if self.PixivImageSearchConfig["UserSetSavePath"] == "":
               save_path = f"./{time.strftime('%Y-%m-%d',time.localtime())}_{self.MainTarget_Tag}.txt"
            else:
               save_path = f"{self.PixivImageSearchConfig['UserSetSavePath']}\{time.strftime('%Y-%m-%d',time.localtime())}_{self.MainTarget_Tag}.txt"

            with open(save_path,"w+") as f:
               f.write(" \n".join(self.id_SaveList))
            
         elif SaveModeType[self.PixivImageSearchConfig["SaveMode"]] == "SaveImage":
            for image_detail in self.id_SaveList:
               self.currentImageInfo = str(image_detail[0])
               RateCount+=1
               self.RateCountNow = RateCount
               self.Image_Save_CallBack(image_detail[0],image_detail[1])
               self.ProgressRateDisplay = int((RateCount/len(self.id_SaveList))*100)
               self.id_SaveList.remove(image_detail)

   def Pixiv_ImageSeach(self,Mode="TagMode"):
      #TODO: 图片搜索
      
      self.Read_Cookies_data()
      if Mode == "TagMode":
         Start_Data = self.GetImageInfoLists_ByTag(self.MainTarget_Tag,1)
         self.SearchImage_ByTags_CallBack(Start_Data)

   def Image_Save_CallBack(self,id,FileTitle):
      #TODO: 保存图片

      if self.PixivImageSearchConfig["UserSetSavePath"] == "" and not os.path.exists("./PixivImageSave"):
         os.makedirs("./PixivImageSave")
      elif self.PixivImageSearchConfig["UserSetSavePath"]!="" and not os.path.exists(self.PixivImageSearchConfig["UserSetSavePath"]):
         os.makedirs(self.PixivImageSearchConfig["UserSetSavePath"])

      try:
         target_URL_data = requests.get('https://pixiv.net/ajax/illust/{}/pages'.format(id),headers=self.requests_header,cookies=self.cookiedataget,timeout=60).content.decode('utf-8')
         image_url = json.loads(target_URL_data)["body"]
      except Exception as e:
         self.PixivClassError_CallBack(e)

      if self.PixivImageSearchConfig["UserSetSavePath"] == "":
         save_path = f"./PixivImageSave/{FileTitle}"
      else:
         save_path = f"{self.PixivImageSearchConfig['UserSetSavePath']}/{FileTitle}"

      if not os.path.exists(save_path):
         os.makedirs(save_path)
      
      for url in image_url:
         try:
            image_bytes_data = requests.get(url['urls']['regular'],headers= self.requests_header,timeout=60).content
         except Exception as e:
            self.PixivClassError_CallBack(e)

         image_name = url['urls']['regular'].split('/')[-1]
         if not os.path.exists(f"{save_path}/{image_name}"):
            with open(f"{save_path}/{image_name}","wb") as fr:
               fr.write(image_bytes_data)

   def PixivClassError_CallBack(self,error_info):
      
      if self.CookieLoadSuccessFlag:
         with open("./History_Config.json","w+") as f:
            f.write(json.dumps(self.PixivImageSearchConfig))
         History_Data = {

            "ImageTagSelectPass_ID_List":self.ImageTagSelectPass_ID_List,
            "id_SaveList":self.id_SaveList,
            "Progress":self.ProgressDisplay,
            "SearchPage":self.PageNow,
            "RateCount":self.RateCountNow*0
         }
         with open("./History_Data.json","w+") as f:
            f.write(json.dumps(History_Data))
      
      self.ErrorStopFlag=True
      self.ErrorDetailInfo = str(error_info)

      while(1):
         pass
