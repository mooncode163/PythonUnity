# 导入selenium的浏览器驱动接口


import sys
import os
import json
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
  
import sqlite3
import time
import platform 

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from Common import Source  
from AppStore.AppStoreBase import AppStoreBase
from AppStore.AppConnectApi import mainAppConnectApi
from AppInfo.AppInfo import mainAppInfo
from Project.Resource import mainResource
from Project.UpdateAppstore import mainUpdateAppstore
from Common.Platform import Platform
from Common.File.FileUtil import FileUtil 


from Common.WebDriver.WebDriverCmd import CmdType
from Common.WebDriver.WebDriverCmd import WebDriverCmd 
from Common.WebDriver.WebDriverCmd import CmdInfo 

from AppStore.AppStoreAcount import mainAppStoreAcount
from AppStore.UploadAssetApple import mainUploadAssetApple 

# pip3 install pyjwt
# pip3 install cryptography
if 'Darwin' not in platform.system():
    # mac arm openssl  cryptography不兼容
    import jwt

import datetime 
import time
import requests
import gzip


# 要想调用键盘按键操作需要引入keys包

# 导入chrome选项


# pip3 install pywin32

# sys.path.append('../common')

# connectcli -k MVG9NGFVX7 -i 69a6de89-f844-47e3-e053-5b8c7c11a4d1 devices
# connectcli -k MVG9NGFVX7 -i 69a6de89-f844-47e3-e053-5b8c7c11a4d1 createprofile -n fillcoloanimal -b 249GXC99SV  -c 3K9293L64L  -t IOS_APP_STORE
class AppStoreApple(AppStoreBase):  
    API_KEY_ID="MVG9NGFVX7"
    API_USER_ID="69a6de89-f844-47e3-e053-5b8c7c11a4d1" 
    listCountry = ["zh-Hans","en-US", "en-CA","en-AU","en-GB"]  
    listCountryScreentShot = ["zh-Hans","en-US"]  
    listCountryLanguage = ["cn","en", "en","en","en"] 

    # listCountry = ["en-AU","en-GB"]  
    # listCountryLanguage = ["en","en"] 
    listDisplay = ["APP_IPHONE_65", "APP_IPHONE_55","APP_IPAD_PRO_3GEN_129","APP_IPAD_PRO_129"]  
    listDisplayName = ["iphone_6_5", "iphone","ipadpro","ipadpro"] 
 
    def GoHome(self,isHD):  
        # appid = AppInfo.GetAppId(isHD, Source.APPSTORE)
        url = "https://appstoreconnect.apple.com/login"
        # url ="https://appstoreconnect.apple.com/apps/"+appid+"/appstore/ios/version/deliverable"
        print(url)
        self.driver.get(url)
        time.sleep(1)
        self.Login("chyfemail163@163.com","Moonqianlizhiwai1")
  
    
    def Login(self,user,password):
        webcmd = WebDriverCmd(self.driver)
        self.urlold = self.driver.current_url
        print("Login urlold=",self.urlold) 

        # 等待网页加载成功
        key = "//iframe[@id='aid-auth-widget-iFrame']"
        while True:
            # self.driver.switch_to.frame('aid-auth-widget-iFrame')
            time.sleep(1)
            print("web is loading...")
            if self.IsElementExist(key)==True:
                print("web loading finish")
                break

        self.driver.switch_to.frame('aid-auth-widget-iFrame')
        time.sleep(1)

        key = "//input[@id='account_name_text_field']"
        webcmd.AddCmdWait(CmdType.CLICK, key) 
        webcmd.AddCmd(CmdType.INPUT, key,user) 
        webcmd.Run(True)
 
        key = "//button[@id='sign-in']"
        webcmd.AddCmd(CmdType.CLICK, key) 
        webcmd.Run(True)
 

        key = "//input[@id='password_text_field']"
        webcmd.AddCmd(CmdType.INPUT, key,password) 
        webcmd.Run(True)
 
        key = "//button[@id='sign-in']"
        webcmd.AddCmd(CmdType.CLICK, key) 
        webcmd.Run(True)

        # item = self.driver.find_element(By.XPATH, "//input[@id='password_text_field']")
        # item.send_keys(password)
        # item.click()
        # time.sleep(1)

        # item = self.driver.find_element(By.XPATH, "//button[@id='sign-in']")
        # item.click() 
        # time.sleep(1)
 
        key = "//button[contains(@id,'trust-browser')]"
        item = webcmd.Find(key,True)
        if item is not None:
            webcmd.AddCmd(CmdType.CLICK, key) 
            webcmd.Run(True)

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
        appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)
        package = mainAppInfo.GetAppPackage(Source.IOS,isHD)
        if appid!="0": 
            self.UpdateAppInfo(isHD)
            self.UploadScreenShot(isHD)
            # self.Init()
            # self.GoHome(isHD) 
            # self.FillAppInfo(isHD)
            return

        # mainAppConnectApi.GetAppProfile(package,appid)
        # package = mainAppInfo.GetAppPackage(Source.IOS,isHD)
        bundleid = mainAppConnectApi.GetBundleIdByPackage(package)
        webcmd = WebDriverCmd(self.driver)
        url = "https://appstoreconnect.apple.com/apps" 
        self.driver.get(url)
        time.sleep(2)
 



        webcmd.AddCmdWait(CmdType.CLICK, "//span[@id='new-app-btn-icon']")
        webcmd.AddCmd(CmdType.CLICK, "//button[@id='new-app-btn']")
        webcmd.AddCmdWait(CmdType.CLICK, "//input[@name='appStoreVersionsIOS']") 
        webcmd.AddCmd(CmdType.INPUT, "//input[@id='name']",mainAppInfo.GetAppName(Source.IOS, isHD,Source.LANGUAGE_EN)) 
        webcmd.AddCmd(CmdType.INPUT, "//input[@id='sku']",mainAppInfo.GetAppSKU(isHD)) 
 

 
        key = "//select[@name='primaryLocale']"
        item=webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)
        if item==None:
            item = webcmd.Find(key)

        key = ".//option[@value='en-US']"
        subitem = webcmd.FindChild(item,key)
        webcmd.DoCmd(subitem,CmdType.CLICK)
  

        item=webcmd.AddCmd(CmdType.CLICK, "//select[@name='bundleId']")
        webcmd.Run(True) 
        key = ".//option[@value='"+package+"']"
        subitem = webcmd.FindChild(item,key)
        webcmd.DoCmd(subitem,CmdType.CLICK) 
  
        webcmd.AddCmd(CmdType.INPUT, "//input[@id='sku']",mainAppInfo.GetAppSKU(isHD))  

        # item=webcmd.AddCmd(CmdType.CLICK_SCRIPT, "//button[@type='primary'] and text()='创建'")
        # webcmd.Run(True)  
        webcmd.WaitKeyBoard("q")

        time.sleep(5)

        # https://appstoreconnect.apple.com/apps/1525843317/appstore/ios/version/inflight
        url = self.driver.current_url
        print(url)
        head = "/apps/"
        idx = url.find(head)+len(head)
        url = url[idx:]
        idx = url.find("/")
        appid = url[0:idx]
        print("appid create =",appid)
        mainAppInfo.SetAppId(isHD,Source.IOS,Source.APPSTORE,appid)
        
        self.FillAppInfo(isHD)

     
    def FillAppInfo(self, isHD):
        appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)  
        url = "https://appstoreconnect.apple.com/apps/"+appid+"/appstore/ios/version/inflight" 
        self.driver.get(url)
        time.sleep(2)
        webcmd = WebDriverCmd(self.driver) 
        webcmd.AddCmdWait(CmdType.INPUT, "//input[@id='versionString']",mainAppInfo.GetAppVersion(Source.IOS, isHD))
        webcmd.Run(True) 
        webcmd.AddCmd(CmdType.INPUT, "//input[@id='copyright']","moonma")  
        webcmd.Run(True) 
        # 截图
        # <input id="choose-file" type="file" multiple="" class="choose-file-input___33eoI">
        
        # 分级
        webcmd.AddCmd(CmdType.CLICK, "//button[@type='button' and text()='编辑']") 
        key = "//input[@type='radio' and @value='NONE' and contains(@id,'_NONE')]"
        webcmd.AddCmd(CmdType.CLICK_List_ALL,key)
        # <input type="radio" name="violenceCartoonOrFantasy" id="violenceCartoonOrFantasy_NONE" value="NONE">
        webcmd.AddCmd(CmdType.CLICK, "//input[@id='unrestrictedWebAccess_false']")
        webcmd.AddCmd(CmdType.CLICK, "//input[@id='gamblingAndContests_false']")
        webcmd.AddCmd(CmdType.CLICK, "//button[@type='primary' and text()='完成']") 


        webcmd.AddCmd(CmdType.CLICK, "//input[@id='demoAccountRequired']") 
        webcmd.AddCmd(CmdType.INPUT, "//input[@id='contactFirstName']","YuanFang") 
        webcmd.AddCmd(CmdType.INPUT, "//input[@id='contactLastName']","Chen")
        webcmd.AddCmd(CmdType.INPUT, "//input[@id='contactPhone']","+8617370716836")
        webcmd.AddCmd(CmdType.INPUT, "//input[@id='contactEmail']","chyfemail163@163.com") 


        # IDFA
        webcmd.AddCmd(CmdType.CLICK, "//input[@id='usesIdfa_true']") 
        webcmd.AddCmd(CmdType.CLICK, "//input[@id='attributesAppInstallationToPreviousAd_undefined']")
        webcmd.AddCmd(CmdType.CLICK, "//input[@id='honorsLimitedAdTracking_undefined']")  

        webcmd.Run(True)

    def CreateNewVersion(self, isHD): 
        appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)
        webcmd = WebDriverCmd(self.driver)
        # url = "https://appstoreconnect.apple.com/apps/1230426472/appstore/ios/version/deliverable"
        url = "https://appstoreconnect.apple.com/apps/"+appid+"/appstore/ios/version/deliverable"
        self.driver.get(url)
        time.sleep(2)

        webcmd.AddCmd(CmdType.CLICK, "//button[@id='IOS_app_versions-add-button']")
        webcmd.AddCmd(CmdType.INPUT, "//input[@id='versionString']",AppInfo.GetAppVersion(Source.IOS,isHD))
        webcmd.AddCmd(CmdType.CLICK, "//button[@data-id='create-new-version']")
        webcmd.Run(True)

# 提交app
    def SubmitApp(self, isHD): 
        appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)
        webcmd = WebDriverCmd(self.driver)
        # url = "https://appstoreconnect.apple.com/apps/1230426472/appstore/ios/version/inflight"
        url = "https://appstoreconnect.apple.com/apps/"+appid+"/appstore/ios/version/inflight"
        self.driver.get(url)
        time.sleep(2)
 
        webcmd.AddCmd(CmdType.CLICK, "//button[@type='primary']")
        webcmd.Run(True)

    def UpdateApp(self, isHD): 
        appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)
        webcmd = WebDriverCmd(self.driver)
        time.sleep(2)
      
  
#   https://appstoreconnect.apple.com/apps/1230426472/appstore/ios/version/inflight
  
 
        apk = common.GetOutPutApkPathWin32(mainr.GetProjectOutPut(),Source.TAPTAP,isHD)
        # F:\\sourcecode\\unity\\product\\kidsgame\\ProjectOutPut\\xiehanzi\\hanziyuan\\screenshot\\shu\\cn\\480p\\1.jpg
        self.OpenFileBrowser(apk,True)

      


        while True:
            time.sleep(2)
            # for win in self.driver.window_handles:
            #     if win!=old_window:
            #         self.driver.switch_to.window(win)
            #         self.urlold = self.driver.current_url
            #         old_window = win
            #         print("urlold 2=",self.urlold)
                    

            # self.driver.switch_to.window(self.driver.window_handles[0])  
            self.urlnew = self.driver.current_url
            print("urlnew=",self.urlnew)
            if self.urlnew!=self.urlold:
                print("new page =",self.urlnew)
                break

        # <div class="progress"><div class="progress-bar" style="width: 82%;" aria-valuenow="82"></div></div>
        # while True:
        #     item = self.driver.find_element(By.XPATH, "//div[@class='progress']")
        #     if item is not None:
        #         value = item.get_attribute('aria-valuenow')
        #         int_v = int(value)
        #         if int_v>=100:
        #             break
        
        # time.sleep(1)

        # 手动等待上传
        # time.sleep(60*2)


        # https://www.taptap.com/developer/fill-form/14628?apk_id=496448&app_id=56016


        # 未成年人防沉迷
        # <input required="" type="radio" name="anti_addiction_read" value="1">
        item = self.driver.find_element(By.XPATH, "//input[@name='anti_addiction_read']")
        item.click()
        time.sleep(1)
        # <input required="required" type="radio" name="anti_addiction_status" value="1">
        item = self.driver.find_element(By.XPATH, "//input[@name='anti_addiction_status']")
        item.click()
        time.sleep(1)

        # 提交审核
        # <button id="postAppSubmitV2" type="submit" value="submit" class="leave_current_page btn btn-primary btn-lg">保存并提交审核</button>
        item = self.driver.find_element(By.XPATH, "//button[@id='postAppSubmitV2']")
        item.click()
        time.sleep(2)

        # 确定

        
        # section = self.driver.find_element(By.XPATH, "//section[@class='modal fade taptap-modal global-tip-modal in']")
        # # <button class="btn btn-primary" data-default-text="确定">确定</button>
        # # item = self.driver.find_element(By.XPATH, "//button[@data-default-text='确定']")
        # item = section.find_element(By.XPATH, "//button[@data-default-text='确定']")
        list = self.driver.find_elements(By.XPATH, "//button[@data-default-text='确定']")
        item = list[1]
        print("确定") 
        self.driver.execute_script("arguments[0].click();", item)
        time.sleep(1)


    def GetAppName(self, ishd):
        name = mainAppInfo.GetAppName(Source.ANDROID, ishd,Source.LANGUAGE_CN)
        # if self.osApp == Source.IOS:
        #     mainAppInfo.GetAppName(self.osApp, ishd)+self.osApp

        return name
 
    def SearchApp(self, ishd):
        name = self.GetAppName(ishd)
        
        # self.driver.get("https://adnet.qq.com/medium/list")
        time.sleep(2)
  
        div = self.driver.find_element(
            By.XPATH, "//div[@class='developer-search-app']")
        time.sleep(1) 

        item = div.find_element_by_xpath("input")
        item.send_keys(name)
        # item.send_keys("儿童写汉字")

        time.sleep(1)


        div = self.driver.find_element(By.XPATH, "//div[@class='dropdown search-app-dropdown']")
        item = div.find_element_by_xpath("ul/li/a")
        # app_id=56016
        url = item.get_attribute('href')
        strfind = "app_id="
        idx =  url.find(strfind)+len(strfind)
        print(url)
        appid = url[idx:] 
        print(appid)
        mainAppInfo.SetAppId(ishd,Source.ANDROID,Source.TAPTAP,appid)

    def UpdateAso(self, ishd):
        print("UpdateAso")

    def UpdateAppstore(self,isHd):
        mainUpdateAppstore.Run(isHd)

# https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations/{id}
    def UpdateAppInfo(self,isHD):  
        if not Platform.isWindowsSystem():
            self.UpdateAppstore(isHD)

        appid = mainAppInfo.GetAppId(isHD,Source.APPSTORE)
        version = mainAppInfo.GetAppVersion(Source.IOS,isHD)
        idx = 0
        print("UpdateAppInfo 1 appid="+appid+ " isHD="+str(isHD))
        for country in self.listCountry:
            lan = self.listCountryLanguage[idx]
            name= mainAppInfo.GetAppName(Source.IOS, isHD,lan)
            subtitle= mainAppInfo.GetAppSubtitle(isHD,lan)
            policyUrl= mainAppInfo.GetAppPrivacyUrl(isHD)
            policyText =""

            description = mainAppInfo.GetAppDetail(isHD,lan)
            keywords = mainAppInfo.GetAso(isHD,Source.APPSTORE,lan)
            marketingUrl = mainAppInfo.GetAppSoftwareUrl(isHD)
            promotionalText =  mainAppInfo.GetAppPromotion(isHD, lan) 
            supportUrl =  mainAppInfo.GetAppSupportUrl(isHD)
            whatsNew = mainAppInfo.GetAppUpdate(isHD,lan)
            print("mainAppConnectApi UpdateAppInfo  appid="+appid)
            mainAppConnectApi.UpdateAppInfo(appid,version,country,description,keywords,marketingUrl,promotionalText,supportUrl,whatsNew)
            mainAppConnectApi.UpdateAppName(appid,version,country,name,policyText,policyUrl,subtitle)
            
            idx+=1




    def CreateBundleID(self,isHD):
        print("CreateBundleID   enter=") 
        # isHD = True
        appid = mainAppInfo.GetAppId(isHD,Source.APPSTORE)
        package = mainAppInfo.GetAppPackage(Source.IOS,isHD)
        # package = "com.moonma.fillfood.pad2"
        
        print("CreateBundleID   package=",package)
        mainAppConnectApi.CreateBundleID(package) 
        # mainAppConnectApi.GetAppProfile(package,appid)
         

    def UploadScreenShot(self,isHD):

        appid = mainAppInfo.GetAppId(isHD,Source.APPSTORE)
        package = mainAppInfo.GetAppPackage(Source.IOS,isHD)
      

        # isHD = True
        
        version = mainAppInfo.GetAppVersion(Source.IOS,isHD)
        total_screenshot = 5
        idx_country =0
        idx_display =0
        
        for country in self.listCountryScreentShot:
            idx_display = 0
            for type in self.listDisplay: 

                # try: 
                #     mainAppConnectApi.DeleteAllScreenShot(appid, version, country, type)
                # except Exception as e:  
                #     print("DeleteAllScreenShot eror=",e)

                
                for i in range(total_screenshot):
                    filepath = mainResource.GetOutPutScreenshot(isHD)+"/"+self.listCountryLanguage[idx_country]+"/"+self.listDisplayName[idx_display]+"/"+str(i+1)+".jpg"
                    print("UploadScreenShot filepath=",filepath)
                    if os.path.exists(filepath):
                        mainAppConnectApi.UploadScreenShot(appid, version, country, type, filepath)

                idx_display+=1
            
            idx_country+=1


        self.UpdateAppInfo(isHD)
        # return

    def DeleteAllScreenShot(self,isHD):  
        print("DeleteAllScreenShot isHD=",isHD)
        # isHD = True
        appid = mainAppInfo.GetAppId(isHD,Source.APPSTORE)
        version = mainAppInfo.GetAppVersion(Source.IOS,isHD)
        total_screenshot = 5
        idx_country =0
        idx_display =0
        for country in self.listCountry:
            idx_display = 0
            for type in self.listDisplay: 
                try: 
                    mainAppConnectApi.DeleteAllScreenShot(appid, version, country, type)
                except Exception as e:  
                    print("DeleteAllScreenShot eror=",e)

                idx_display+=1
            
            idx_country+=1


    def Run(self,type, isHD):     

        name = mainAppInfo.GetAppStoreAcount(isHD,Source.APPSTORE)
        mainAppConnectApi.API_KEY_ID = mainAppStoreAcount.GetiOSAPI_KEY_ID(name)
        mainAppConnectApi.API_USER_ID = mainAppStoreAcount.GetiOSAPI_USER_ID(name) 
        mainAppConnectApi.teamID = mainAppStoreAcount.GetiOSteamID(name) 
        mainAppConnectApi.CertificateID = mainAppStoreAcount.GetiOSCertificateID(name) 

        mainUploadAssetApple.KEY_ID = mainAppConnectApi.API_KEY_ID
        mainUploadAssetApple.ISSUER_ID = mainAppConnectApi.API_USER_ID
        mainUploadAssetApple.PRIVATE_KEY = mainAppConnectApi.GetKEY_PRIVATE()
        mainUploadAssetApple.tokenKey = mainAppConnectApi.GetToken()
         
        if type == "createapp":
            appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)
            
            if appid=="0" or appid=="":
                self.Init()
                self.GoHome(isHD) 
            
            if isHD:
                self.CreateApp(True)
            else:
                self.CreateApp(False)
                self.CreateApp(True)
               

          
            
            # mainAppConnectApi.CreateProfile(mainAppInfo.GetAppPackage(Source.IOS,True))
        if type == "new_version":
            # isHD = True
            mainAppConnectApi.CreateNewVersion(mainAppInfo.GetAppId(isHD,Source.APPSTORE),mainAppInfo.GetAppVersion(Source.IOS,isHD),mainAppInfo.GetAppPackage(Source.IOS,isHD))
 
        if type == "UploadScreenShot":
            self.UploadScreenShot(isHD)

        if type == "CreateBundleID":
            self.CreateBundleID(False)
            self.CreateBundleID(True)

        if type == "DeleteAllScreenShot":
            self.DeleteAllScreenShot(isHD)


        if type == "UpdateAppInfo":
            self.UpdateAppInfo(False)
            self.UpdateAppInfo(True)

 
        if type == "update":
            if isHD:
                self.UpdateApp(True)
            else:
                self.UpdateApp(False)
                time.sleep(3)
                # ad.UpdateApp(True)

        # ad.Quit(300)
 

mainAppStoreApple = AppStoreApple()

    
 
