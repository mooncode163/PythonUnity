# 导入selenium的浏览器驱动接口


import sys
import os
import json
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
 
import AppInfo 
import sqlite3
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from Common import Source 
from AppStore.AppStoreBase import AppStoreBase 
from AppStore.GooglePlayApi import mainGooglePlayApi
from AppInfo.AppInfo import mainAppInfo
from Project.Resource import mainResource

from Common.WebDriver.WebDriverCmd import CmdType
from Common.WebDriver.WebDriverCmd import WebDriverCmd 
from Common.WebDriver.WebDriverCmd import CmdInfo 

# 要想调用键盘按键操作需要引入keys包

# 导入chrome选项


# pip3 install pywin32

# sys.path.append('../common')


class AppStoreGoogleInternal(AppStoreBase):  
    listCountry = ["zh-CN","en-US", "en-ZA","en-SG","en-IN","en-CA","en-AU","en-GB"]  
    listCountryLanguage = ["cn","en", "en","en","en", "en","en","en"] 

    # listCountry = ["en-AU","en-GB"]  
    # listCountryLanguage = ["en","en"] 
    # https://developers.google.cn/android-publisher/api-ref/rest/v3/AppImageType?hl=zh-cn  tvBanner
    # phoneScreenshots
    # listDisplay = ["PHONE_SCREENSHOTS", "SEVEN_INCH_SCREENSHOTS","TEN_INCH_SCREENSHOTS","ICON","FEATURE_GRAPHIC"]  
    listDisplay = ["phoneScreenshots", "sevenInchScreenshots","tenInchScreenshots","icon","featureGraphic"]  
 
    listDisplayName = ["iphone_6_5", "iphone","ipadpro","icon","adhome"] 
    apptype = ""
    appkey = ""

    def GoHome(self,isHD):  
        # appid = AppInfo.GetAppId(isHD, source.APPSTORE)
        url = "https://play.google.com/apps/publish/?account=5674304593297259399#ApiAccessPlace"
        # url ="https://appstoreconnect.apple.com/apps/"+appid+"/appstore/ios/version/deliverable"
        print(url)
        self.driver.get(url)
        time.sleep(1)
        self.Login("chyfemail163@gmail.com", "qianlizhiwai1")
  
    
    def Login(self,user,password):
        self.urlold = self.driver.current_url
        print("Login urlold=",self.urlold) 

        webcmd = WebDriverCmd(self.driver)

        # 等待网页加载成功
        key = "//input[@type='email']"
        item = webcmd.Find(key,True)
        webcmd.AddCmd(CmdType.INPUT,key,user)
        webcmd.Run(True)
 
        key = "//span[contains(text(),'下一步')]"
        webcmd.AddCmd(CmdType.CLICK_Action,key)
        webcmd.Run(True)

        time.sleep(1)
     
 
 
        # 等待登录成功
        while True:
            time.sleep(1)  
            self.urlnew = self.driver.current_url
            print("Login urlnew=",self.urlnew)
            if self.urlnew!=self.urlold:
                print("Login Finish =",self.urlnew)
                break
  


    
# 3452644866 qq31415926
    def CreateApp(self, isHD):
        # ad.GoHome(isHD)
        time.sleep(1)
        print(" gp CreateApp") 

         
#  https://developers.google.cn/android-publisher/api-ref/rest/v3/AppImageType?hl=zh-cn
    def UploadScreenShot(self,isHD):  
        # isHD = True
        package = mainAppInfo.GetAppPackage(Source.ANDROID,isHD,Source.GP)
        version = mainAppInfo.GetAppVersion(Source.ANDROID,isHD)
        
        total_screenshot = 5
        idx_country =0
        idx_display =0
        for country in self.listCountry:
            idx_display = 0
            for type in self.listDisplay: 
                for i in range(total_screenshot):
                    applan = self.listCountryLanguage[idx_country]
                    filepath = mainResource.GetOutPutScreenshot(isHD)+"/"+applan+"/"+self.listDisplayName[idx_display]+"/"+str(i+1)+".jpg"
                    if self.listDisplayName[idx_display]=="icon":
                        filepath = mainResource.GetOutPutIconPathWin32( mainResource.GetProjectOutPut(), Source.TAPTAP, isHD)+"\\icon_android_512.png"
                        if i>0:
                            continue

                    if self.listDisplayName[idx_display]=="adhome":
                        filepath = mainResource.GetOutPutAdPathWin32(mainResource.GetProjectOutPut(), Source.TAPTAP, isHD) + "\\"+applan+"\\"+"ad_home_1024x500.png"
                        if i>0:
                            continue
                        
                    print("UploadScreenShot filepath=",filepath)
                    if os.path.exists(filepath):
                        mainGooglePlayApi.DeleteAllScreenShot(package, version, country, type)
                        mainGooglePlayApi.UploadOneScreenShot(package, filepath, country, type) 

                idx_display+=1
            
            idx_country+=1

    def UpdateAppInfo(self,isHD):  
        
        package = mainAppInfo.GetAppPackage(Source.ANDROID,isHD,Source.GP)
        version = mainAppInfo.GetAppVersion(Source.ANDROID,isHD)
        idx = 0
        print("google UpdateAppInfo=",package) 

        for country in self.listCountry:
            lan = self.listCountryLanguage[idx]
            name= mainAppInfo.GetAppName(Source.IOS, isHD,lan,Source.GP) 
            description = mainAppInfo.GetAppDetail(isHD,lan) 
            promotionalText =  mainAppInfo.GetAppPromotion(isHD, lan)  
            mainGooglePlayApi.UpdateAppInfo(package,country,name,description,promotionalText,str(isHD),lan) 
            idx+=1

    def UpdateApk(self,isHD): 
        package = mainAppInfo.GetAppPackage(Source.ANDROID,isHD,Source.GP)
        apk = mainResource.GetOutPutApkPath(Source.GP, isHD)
        mainGooglePlayApi.UploadApk(package,apk) 

    def Run(self,type, isHD):     
        if type == "createapp":
            self.Init()
            self.GoHome(isHD) 
            self.CreateApp(isHD)
            time.sleep(3)
            # ad.CreateApp(True)


        if type == "UploadScreenShot":
            if isHD:
                self.UploadScreenShot(True)
            else:
                self.UploadScreenShot(False)
                time.sleep(3)
                # ad.UpdateApp(True)

        if type == "UpdateAppInfo":
            if isHD:
                self.UpdateAppInfo(True)
            else:
                self.UpdateAppInfo(False)
                time.sleep(3)
                # ad.UpdateApp(True)


        if type == "UpdateApk":
            if isHD:
                self.UpdateApk(True)
            else:
                self.UpdateApk(False)
                time.sleep(3)
                # ad.UpdateApp(True)

        # ad.Quit(300)


mainAppStoreGoogleInternal = AppStoreGoogleInternal()
    
 
