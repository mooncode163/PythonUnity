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
from Common.File.FileTransfer  import mainFileTransfer 

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
import pyautogui 
 
# from PIL import Image

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
  

    def OnMouseClickScreen(self,x,y):
                # 获取当前屏幕分辨率
        screenWidth, screenHeight = pyautogui.size()

        # 获取当前鼠标位置
        # currentMouseX, currentMouseY = pyautogui.position()

        # 2秒钟鼠标移动坐标为100,100位置  绝对移动
        #pyautogui.moveTo(100, 100,2)
        # pyautogui.moveTo(x=100, y=100,duration=2, tween=pyautogui.linear)

        pyautogui.moveTo(x, y)
        # 鼠标左击一次
        pyautogui.click()
        time.sleep(1)

    def GetAppleCode(self):
 
        # mac mini 分辨率 2560x1080
        x =1460
        y = 680
        self.OnMouseClickScreen(x,y)


        savefilepath = 'screenshot.png'
  
        try:
            # im = pyautogui.screenshot('screenshot.png',region=(0,0, 300, 400))
            im = pyautogui.screenshot(savefilepath)
        except:
            print("pyautogui.screenshot error")
          


        x = 1220
        y = 540
        w = 200
        h = 50
        region = str(x)+","+str(y)+","+str(w)+","+str(h)
        print("region=",region)


        # try:
        #     tangle=(x,y,x+w,y+h)
        #     print("GetAppleCode tangle=",tangle)
        #     # print(tangle)#(276, 274, 569, 464)
        #     #打开123.png图片
        #     img = Image.open(savefilepath)
        #     #在123.png图片上 截取验证码图片
        #     frame = img.crop(tangle)
        #     #保存
        #     frame.save(savefilepath)
        # except:
        #     print("image convert error")



        # url = 'http://127.0.0.1:8887/upload' 
        # url = 'http://127.0.0.1:8887/GetAppleCode' 
        url = 'http://mooncore.cn:5000/GetAppleCode' 
        
        code = mainFileTransfer.Upload(url, savefilepath)
        code = code.replace(" ","")
        print("AppleCode code=",code," len=",len(code))
        while len(code)<=3:
            code = mainFileTransfer.Upload(url, savefilepath)
            code = code.replace(" ","")
            print("wait for AppleCode code=",code)
            time.sleep(1)



        # 点击完成
        # mac mini 分辨率 2560x1080
        x =1460
        y = 600
        self.OnMouseClickScreen(x,y)
             
            

        return code


    def Login(self,user,password):
        mainAppInfo.SetSmsCode("")
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
        if Platform.isMacSystem():
            # mac 输入双重验证
            test = 0
            time.sleep(3)
            code = self.GetAppleCode()

       

        else:

            # 输入短信验证码

            # <a class="si-link ax-outline tk-subbody lite-theme-override" id="didnt-get-code" href="#">
            #                 没有收到验证码？
            #             </a>
            key = "//a[@id='no-trstd-device-pop']"
            item = webcmd.Find(key,True) 
            if item is not None:
                webcmd.AddCmd(CmdType.CLICK, key) 
                webcmd.Run(True)

    # <a class="si-link link ax-outline tk-subbody-headline" id="use-phone-link" href="#" aria-describedby="usePhoneSMSInfo">
    #                                                 发送短信给我
    #                                             </a>

            key = "//a[@id='use-phone-link']"
            item = webcmd.Find(key,True) 
            if item is not None:
                webcmd.AddCmd(CmdType.CLICK, key) 
                webcmd.Run(True)

            code = self.GetSmsCode()
            print("Login GetSmsCode=",code)

        
        # 输入code
            # <input maxlength="1" autocorrect="off" autocomplete="off" autocapitalize="off" spellcheck="false" type="tel" id="char0" class="form-control force-ltr form-textbox char-field" aria-label="输入验证码 位 1" placeholder="" data-index="0">
        for i in range(6):
            idkey = "char"+str(i)
            key = "//input[@id='"+idkey+"']"
            item = webcmd.Find(key,False)
            # webcmd.SetInputText(key,code[i])
            code_i = code[i]
            print("input code_i=",code_i)
            item.send_keys(code_i)
        

        

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
            

            

    def ShowWebHome(self):
        url = "https://appstoreconnect.apple.com"
        self.driver.get(url)
        time.sleep(4)
    
# 3452644866 qq31415926
    def CreateApp(self, isHD): 
        appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)
        package = mainAppInfo.GetAppPackage(Source.IOS,isHD)
        if appid!="0": 
            self.FillAppInfo(isHD)
            # self.UpdateAppInfo(isHD)
            # self.UploadScreenShot(isHD)
            # self.Init()
            # self.GoHome(isHD) 
            
            return

        # mainAppConnectApi.GetAppProfile(package,appid)
        # package = mainAppInfo.GetAppPackage(Source.IOS,isHD)
        bundleid = mainAppConnectApi.GetBundleIdByPackage(package)
        webcmd = WebDriverCmd(self.driver)
        url = "https://appstoreconnect.apple.com/apps" 
        self.driver.get(url)
        time.sleep(2)
        self.urlold = self.driver.current_url



        webcmd.AddCmdWait(CmdType.CLICK, "//button[@id='new-app-btn-icon']")
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
        # time.sleep(2)
        key = ".//option[@value='"+package+"']"
        subitem = webcmd.FindChild(item,key,True)
        webcmd.DoCmd(subitem,CmdType.CLICK) 
        time.sleep(1)

        webcmd.AddCmd(CmdType.INPUT, "//input[@id='sku']",mainAppInfo.GetAppSKU(isHD))  

        # item=webcmd.AddCmd(CmdType.CLICK_SCRIPT, "//button[@type='primary'] and text()='创建'")
        # webcmd.Run(True)  
        # webcmd.WaitKeyBoard("q")

        # 等待创建成功
        while True:
            time.sleep(1)  
            self.urlnew = self.driver.current_url
            print("CreateApp urlnew=",self.urlnew)
            if self.urlnew!=self.urlold:
                print("CreateApp Finish =",self.urlnew)
                break


        time.sleep(2)

        # https://appstoreconnect.apple.com/apps/1525843317/appstore/ios/version/inflight
        url = self.driver.current_url
        print(url)
        head = "/apps/"
        idx = url.find(head)+len(head)
        url = url[idx:]
        idx = url.find("/")
        appid = url[0:idx]
        print("appid create =",appid)
        if len(appid)>2:
            mainAppInfo.SetAppId(isHD,Source.IOS,Source.APPSTORE,appid)
            self.FillAppInfo(isHD)

    def FillAppPrivacy(self, isHD):
        appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)  
        webcmd = WebDriverCmd(self.driver) 
 # key = "//a[text()='App 隐私']"
        # webcmd.AddCmd(CmdType.CLICK, key)
        # webcmd.Run(True)
        url = "https://appstoreconnect.apple.com/apps/"+appid+"/appstore/privacy"
        self.driver.get(url)
        time.sleep(2)

        # try:
        # <button class="sc-bwzfXH tb-btn--primary uTxCW" type="primary">开始</button>
        key = "//button[text()='开始']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)
                # <label for="collectData_no"><span><strong>否</strong>，我们不会从此 App 中收集数据</span></label>
        key = "//label[@for='collectData_no']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)
                # <button class="sc-bwzfXH tb-btn--primary uTxCW" type="primary" data-id="mainbutton">存储</button>
        key = "//button[text()='存储']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)
        time.sleep(2)
                # <div class="buttons___1H5xc" id="heading-buttons"><button class="sc-bwzfXH tb-btn--disabled uTxCW" type="disabled">发布</button></div>
        key = "//button[text()='发布']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)
        time.sleep(2)

        key = "//button[text()='发布']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)

    def FillAppInfo2(self, isHD):
        appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)  
        webcmd = WebDriverCmd(self.driver) 
 # <li class="  sc-EHOje tb-nav-active   jvzENE"><a href="/apps/1552686772/appstore/info" class="tb-nav-active" aria-current="page">App 信息</a></li>
        # key = "//a[text()='App 信息']"
        # webcmd.AddCmd(CmdType.CLICK, key)
        # webcmd.Run(True)
        url = "https://appstoreconnect.apple.com/apps/"+appid+"/appstore/info"
        self.driver.get(url)
        time.sleep(2)

        
            # 内容版权
            # <button class="inline___3EHpT btn-link___7P55x" data-state="" type="button">编辑</button>
        key = "//button[text()='设置内容版权信息']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)

            # <label for="contentRights_no">不，它不包含、显示或访问第三方内容</label>
        key = "//label[@for='contentRights_no']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)

            # <button class="sc-bwzfXH tb-btn--disabled uTxCW" type="disabled">完成</button>
        key = "//button[text()='完成']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)

            # <div class="buttons___1H5xc" id="heading-buttons"><button class="sc-bwzfXH tb-btn--disabled uTxCW" type="disabled">存储</button></div>
        key = "//button[text()='存储']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)


    def FillAppPrice(self, isHD):
        appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)  
        webcmd = WebDriverCmd(self.driver) 
 # 价格与销售范围
        # <li class="  sc-EHOje tb-nav-active   jvzENE"><a href="/apps/1552686772/appstore/pricing" class="tb-nav-active" aria-current="page">价格与销售范围</a></li>
        # key = "//a[text()='价格与销售范围']"
        # webcmd.AddCmd(CmdType.CLICK, key)
        # webcmd.Run(True)
        url = "https://appstoreconnect.apple.com/apps/"+appid+"/appstore/pricing"
        self.driver.get(url)
        time.sleep(2)

            # <select><option value="-1" disabled="">选取</option><option value="0">CNY 0.00 (免费)</option
        key = "//select"
        # key = "//option[text()='选取']"
        webcmd.AddCmdWait(CmdType.CLICK, key)
        webcmd.Run(True)


        key = "//option[contains(text(),'CNY 0.00')]"
        webcmd.AddCmdWait(CmdType.CLICK, key)
        webcmd.Run(True)
        
        #     # <div class="buttons___1H5xc" id="heading-buttons"><button class="tb-btn--disabled sc-bwzfXH tb-btn--primary uTxCW" type="primary">存储</button></div>
        key = "//button[text()='存储']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)
        time.sleep(3)

    def FillAppInfo(self, isHD):
        appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)  
        webcmd = WebDriverCmd(self.driver) 

        # App 隐私
        try:
            self.FillAppPrivacy(isHD)       
        except Exception as e:  
                        print("FillAppPrivacy eror=",e)

        try:
            self.FillAppPrice(isHD)       
        except Exception as e:  
                        print("FillAppPrice eror=",e)

        try:
            self.FillAppInfo2(isHD)       
        except Exception as e:  
                        print("FillAppInfo2 eror=",e)


        # base appinfo

        url = "https://appstoreconnect.apple.com/apps/"+appid+"/appstore/ios/version/inflight" 
        self.driver.get(url)
        time.sleep(2)
        
        key = "//input[@id='versionString']"
        # 
        webcmd.Find(key,True)
        version = mainAppInfo.GetAppVersion(Source.IOS, isHD)
        print("FillAppInfo version =",appid)
        webcmd.AddCmd(CmdType.INPUT_CLEAR, key)
        webcmd.Run(True) 
        webcmd.AddCmd(CmdType.INPUT,key,version)
        # webcmd.SetInputText(key,version)
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


        key = "//button[text()='存储']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)
 
 
  
        # try:
        # App 信息
       

        # except Exception as e:  
        #                 print("App 信息 eror=",e)
        # IDFA
        # webcmd.AddCmd(CmdType.CLICK, "//input[@id='usesIdfa_true']") 
        # webcmd.AddCmd(CmdType.CLICK, "//input[@id='attributesAppInstallationToPreviousAd_undefined']")
        # webcmd.AddCmd(CmdType.CLICK, "//input[@id='honorsLimitedAdTracking_undefined']")  

        # webcmd.Run(True)

# https://developer.apple.com/documentation/appstoreconnectapi/create_an_app_store_version
    def CreateNewVersion(self, isHD): 
        appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)
        mainAppConnectApi.CreateNewVersion(appid,mainAppInfo.GetAppVersion(Source.IOS,isHD),mainAppInfo.GetAppPackage(Source.IOS,isHD))
 
        # webcmd = WebDriverCmd(self.driver)
        # # url = "https://appstoreconnect.apple.com/apps/1230426472/appstore/ios/version/deliverable"
        # url = "https://appstoreconnect.apple.com/apps/"+appid+"/appstore/ios/version/deliverable"
        # self.driver.get(url)
        # time.sleep(2)

        # webcmd.AddCmd(CmdType.CLICK, "//button[@id='IOS_app_versions-add-button']")
        # webcmd.AddCmd(CmdType.INPUT, "//input[@id='versionString']",AppInfo.GetAppVersion(Source.IOS,isHD))
        # webcmd.AddCmd(CmdType.CLICK, "//button[@data-id='create-new-version']")
        # webcmd.Run(True)

# 提交app
# doc : https://developer.apple.com/documentation/appstoreconnectapi/create_an_app_store_version_submission
    def SubmitApp(self, isHD): 
        self.SubmitAppByWeb(isHD)
        return

        appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)
        package = mainAppInfo.GetAppPackage(Source.IOS,isHD)
        mainAppConnectApi.SubmitApp(appid,package)

    def SubmitAppByWeb(self, isHD):   
        self.Init()
        self.GoHome(isHD)
        appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE) 
        url = "https://appstoreconnect.apple.com/apps/"+appid+"/appstore/ios/version/inflight" 
        self.driver.get(url)
        time.sleep(2)


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



    def UpdateIAPInfo(self,isHD):  
        if not Platform.isWindowsSystem():
            mainUpdateAppstore.UpdateIAPInfo(isHD)

# https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations/{id}
    def UpdateAppInfo(self,isHD,isUpdateName = True): 
         
        if not Platform.isWindowsSystem():
            # self.UpdateAppstore(isHD)
            self.UpdateIAPInfo(isHD)
        


        appid = mainAppInfo.GetAppId(isHD,Source.APPSTORE)
        version = mainAppInfo.GetAppVersion(Source.IOS,isHD)
        idx = 0
        print("UpdateAppInfo 1 appid="+appid+ " isHD="+str(isHD))
        for country in self.listCountry:
            lan = self.listCountryLanguage[idx]
            name= mainAppInfo.GetAppName(Source.IOS, isHD,lan)
            subtitle= mainAppInfo.GetAppSubtitle(isHD,lan)
            # policyUrl= mainAppInfo.GetAppPrivacyUrl(isHD)
            policyUrl= mainAppStoreAcount.GetPrivacy(Source.APPSTORE,mainAppInfo.GetAppStoreAcount(isHD,Source.APPSTORE))
            policyText =""

            description = mainAppInfo.GetAppDetail(isHD,lan)
            keywords = mainAppInfo.GetAso(isHD,Source.APPSTORE,lan)
            marketingUrl = mainAppInfo.GetAppSoftwareUrl(isHD)
            promotionalText =  mainAppInfo.GetAppPromotion(isHD, lan) 
            supportUrl =  mainAppInfo.GetAppSupportUrl(isHD)
            whatsNew = mainAppInfo.GetAppUpdate(isHD,lan) 
            print("UpdateAppInfo  whatsNew="+whatsNew+ " lan="+lan)
            mainAppConnectApi.UpdateAppInfo(appid,version,country,description,keywords,marketingUrl,promotionalText,supportUrl,whatsNew)
            if isUpdateName:
                try: 
                    test = 0
                    mainAppConnectApi.UpdateAppName(appid,version,country,name,policyText,policyUrl,subtitle)
                except Exception as e:  
                    print("UpdateAppName eror=",e)
            
            idx+=1



    # 根据包名注册bundleid
    def CreateBundleID(self,isHD):
        print("CreateBundleID   enter=") 
        # isHD = True
        appid = mainAppInfo.GetAppId(isHD,Source.APPSTORE)
        package = mainAppInfo.GetAppPackage(Source.IOS,isHD)
        # package = "com.moonma.fillfood.pad2"
        
        print("CreateBundleID   package=",package," appid=",appid)
        mainAppConnectApi.CreateBundleID(package) 
        # mainAppConnectApi.GetAppProfile(package,appid)
        # mainAppConnectApi.GetBundleIdOfPackage(package) 
         
    def DownloadProfile(self,isHD): 
        # isHD = True
        appid = mainAppInfo.GetAppId(isHD,Source.APPSTORE)
        package = mainAppInfo.GetAppPackage(Source.IOS,isHD) 
        print("DownloadProfile   package=",package," appid=",appid) 
        mainAppConnectApi.GetAppProfile(package,appid) 

    def UploadScreenShot(self,isHD):
        self.UpdateAppInfo(isHD)
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
                        print("UploadScreenShot exist filepath=",filepath)
                        mainAppConnectApi.UploadScreenShot(appid, version, country, type, filepath)

                idx_display+=1
            
            idx_country+=1


        # self.UpdateAppInfo(isHD)
        # return

    def DeleteAllScreenShot(self,isHD):  
        print("DeleteAllScreenShot isHD=",isHD)
        if not Platform.isWindowsSystem():
            mainUpdateAppstore.DeleteAllScreenshots(isHD)
            self.UpdateAppInfo(isHD)
            return

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
                self.CreateBundleID(isHD)
             
            self.Init()
            self.GoHome(isHD) 

            if isHD:
                self.CreateApp(True)
            else:
                self.CreateApp(False)

                self.ShowWebHome()

                self.CreateApp(True)
               

          
            
            # mainAppConnectApi.CreateProfile(mainAppInfo.GetAppPackage(Source.IOS,True))
        if type == "new_version":
            # isHD = True
            try:
                self.CreateNewVersion(isHD)
            except Exception as e:  
                print("CreateNewVersion eror=",e)

            try:
                self.UpdateAppInfo(isHD,False)
            except Exception as e:  
                print("UpdateAppInfo eror=",e)
 
         
        if type == "UploadScreenShot":
            self.UploadScreenShot(isHD)

        if type == "CreateBundleID":
            self.CreateBundleID(False)
            self.CreateBundleID(True)

        if type == "DownloadProfile":
            self.DownloadProfile(False)
            self.DownloadProfile(True)

        if type == "DeleteAllScreenShot":
            self.DeleteAllScreenShot(isHD)


        if type == "UpdateAppInfo":
            self.UpdateAppInfo(False)
            self.UpdateAppInfo(True)

        if type == "UpdateIAPInfo":
            self.UpdateIAPInfo(False)
            self.UpdateIAPInfo(True)

        if type == "SubmitApp":
            self.SubmitApp(isHD)


 
        if type == "update":
            if isHD:
                self.UpdateApp(True)
            else:
                self.UpdateApp(False)
                time.sleep(3)
                # ad.UpdateApp(True)

        # ad.Quit(300)
 

mainAppStoreApple = AppStoreApple()

    
 
