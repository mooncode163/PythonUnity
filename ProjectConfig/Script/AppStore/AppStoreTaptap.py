# 导入selenium的浏览器驱动接口
import sys
import os
import json
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径


sys.path.append('../../') 
sys.path.append('./') 

from Common.WebDriver.WebDriverCmd import CmdType
from Common.WebDriver.WebDriverCmd import WebDriverCmd 
from Common.WebDriver.WebDriverCmd import CmdInfo 

from AppStore.AppStoreBase import AppStoreBase

from Project.Resource import mainResource
from Common import Source 
from Common.File.FileUtil import FileUtil 
from Common.File.FileBrowser import FileBrowser
from AppInfo.AppInfo import mainAppInfo
from Common.Platform import Platform


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains 


import time
import sqlite3 

import pyperclip

# 要想调用键盘按键操作需要引入keys包

# 导入chrome选项


# pip3 install pywin32

# sys.path.append('../common')


class AppStoreTaptap(AppStoreBase):

    LAN_KEY_default = "default"
    LAN_KEY_CN = "zh_CN"
    LAN_KEY_EN = "en_US" 
    fileCookie = "e:/cookies/cookies_taptap.json" 
    def GoHome(self, isHD, login):
        # self.AddCookie(self.fileCookie)
        # self.driver.get("https://www.taptap.com/developer")
        # self.driver.get("https://www.taptap.com/developer/dashboard/14628/apps")
        # app
        # https://www.taptap.com/developer/dashboard/14628?app_id=56016
        # https://www.taptap.com/developer/dashboard/14628/apps
        appid = mainAppInfo.GetAppId(isHD, Source.TAPTAP)
        print("GoHome appid=", appid, " isHD="+str(isHD))
        # url = "https://www.taptap.com/developer/dashboard/14628?app_id="+appid
        url = "https://www.taptap.com/developer/dashboard/14628/apps"
        #
        print(url)
        self.driver.get(url)
        # self.AddCookie()
        # time.sleep(1)
        # self.AddCookie()
        # self.driver.get(url)
        # return
        if login == True:
            # <div class="icon-font ic_qq"></div>
            # 跳转qq登录
            item = self.driver.find_element(
                By.XPATH, "//div[@class='icon-font ic_qq']")
            item.click()
            time.sleep(1)

    def Login(self, user, password):
        self.urlold = self.driver.current_url
        print("Login urlold=", self.urlold)
        webcmd = WebDriverCmd(self.driver)

        # <span data-v-5bf2336f="">创建游戏</span> 
        # key = "//span[contains(text(),上传APK)]"
        #  <input class="checkbox phone-login__check" type="checkbox" name="read" id="is-agree-login-or-register">
        # key = "//input[@id='is-agree-login-or-register']"
        key = "//label[@for='is-agree-login-or-register']"
        # item = webcmd.Find(key,True)
        # if item is not None:
        #     print("find agree-login-or-register")
        #     webcmd.DoCmd(item,CmdType.CLICK_SCRIPT)

 

        # 等待选择qq
        while True:
            time.sleep(1)
            self.urlnew = self.driver.current_url
            print("select qq urlnew=", self.urlnew)
            if self.urlnew != self.urlold:
                print("select qq Finish =", self.urlnew)
                break

        # webcmd.WaitKeyBoard("q")


        # # 选择 qq登陆
        # key = "//a[@data-social-provider='qq']"  
        # webcmd.AddCmd(CmdType.CLICK_SCRIPT,key)
        # webcmd.Run(True)


        # # global-tip-modal-1791e1fb5e2
        # key = "//section[contains(@id,'global-tip-modal-')]"  
        # section = webcmd.Find(key,True)

        # key = ".//button[@class='btn btn-primary' and @data-default-text='确定']"
        # item = webcmd.FindChild(section,key,False)
        # if item is not None:
        #     print("find button 确定")
        #     webcmd.DoCmd(item,CmdType.CLICK)
        # # <button class="btn btn-primary" data-default-text="确定">确定</button>

        #     # 等待勾选
        #     webcmd.WaitKeyBoard("q")

        #     time.sleep(2)



        
        self.urlold = self.driver.current_url
        self.LoginQQ(user, password) 

        # 等待登录成功
        while True:
            time.sleep(1)
            self.urlnew = self.driver.current_url
            print("Login urlnew=", self.urlnew)
            if self.urlnew != self.urlold:
                print("Login Finish =", self.urlnew)
                break


# 3452644866 qq31415926
    def SelectLanguage(self,webcmd, lan):
      #   <div role="tab" aria-disabled="false" aria-selected="true" class="ant-tabs-tab-active ant-tabs-tab"> 简体中文(默认*) </div>
        key = "//div[@role='tab' and contains(text(),'简体中文')]"
        if lan==self.LAN_KEY_EN:
            key = "//div[@role='tab' and contains(text(),'English')]"

        webcmd.AddCmd(  CmdType.CLICK_Action, key)
        webcmd.Run(True)  

    def UploadIcon(self, webcmd,isHD,lan):
        # bug 上传图片之前先要重新选择语言 不然无法弹出文件浏览器
        # self.SelectLanguage(webcmd,lan)
       # icon
            # <input type="file" name="image" data-valid-width="512" data-valid-height="512" data-taptap-ajax="upload" data-target="#icon-zh_CN" data-target-input="#icon-input-zh_CN" data-url="https://www.taptap.com/ajax/image">
            # "//input[@type='file' and @data-target='#icon-zh_CN']"
        key = "//div[@id='submitApp_translations.zh_CN.icon']"
        if lan==self.LAN_KEY_EN:
            key = "//div[@id='submitApp_translations.en_US.icon']"
 
            # key ="//img[@id='icon-" +   lanKeys[lan]+"']"
            # key = "//input[@type='file' and  @name='image']"
            # key = "//span[@class='fileinput-button fixed-size square icon']"
            
            # "//input[@name='anti_addiction_read']"
        print(key) 
        item_root = webcmd.Find(key)

        key = ".//div[@class='ant-upload-drag-container']"
        item_div = webcmd.FindChild(item_root,key)
                
        # item = self.driver.find_element(By.XPATH, key) 
        # item_div = webcmd.AddCmd2(CmdType.CLICK_Action, key)
        self.SetItemVisible(item_div)
        webcmd.DoCmd(item_div,CmdType.CLICK)
        # webcmd.Run(True)  
        # self.driver.execute_script("arguments[0].click();", item)
        time.sleep(2)

        icon = mainResource.GetOutPutIconPathWin32( mainResource.GetProjectOutPut(), Source.TAPTAP, isHD)+"\\icon_android_512.png"
        print(icon)
        if Platform.isMacSystem(): 
            icon = icon.replace("\\","/")
            icon = FileUtil.GetLastDirofDir(icon)
            test = 0

            # webcmd.Run(True)
        self.OpenFileBrowser(icon, True)
        time.sleep(1)

        # 等待上传完成
        key = ".//span[@class='upload_img']" 
        # print(key)
        item = webcmd.FindChild(item_div,key,True)
        

    def UploadTitle(self, webcmd,isHD,lan,applan):
        # 名称
        # key = "//input[@type='text' and @name='translations[" + lan+"][title]']"
        # if lan==self.LAN_KEY_default:
        #     key = "//input[@type='text' and @name='title']"
        key = "//input[@type='text' and @class='form_in ant-input']"
 
       
        title = self.GetAppName(isHD, applan,Source.TAPTAP) 
        # pyperclip.copy(title)
        print("title =",title," lan=",applan)
        detail = self.GetAppDetail(isHD, applan)
        print("detail =",detail," lan=",applan)
        list = webcmd.FindList(key)
        print("list input =",len(list)," lan=",applan)
        if lan==self.LAN_KEY_EN:
            webcmd.DoCmd(list[1],CmdType.INPUT,title)
        else:
            webcmd.AddCmd(CmdType.INPUT, key, title, 1)
        # pyperclip.paste()
        # webcmd.AddCmd2(CmdType.CLICK, key)
        # webcmd.AddCmd2(CmdType.CTR_V, key) 
        webcmd.Run(True)


        # 介绍
        # key = "//textarea[@class='form_in ant-input' and contains(@placeholder,'optional')]" 
        key = "//textarea[@class='form_in ant-input']" 
        # print(key)
        list = webcmd.FindList(key)
        print("detail list input =",len(list)," lan=",applan)
        if lan==self.LAN_KEY_EN:
            webcmd.DoCmd(list[2],CmdType.INPUT,detail)
            time.sleep(1)
        else:
            webcmd.AddCmd(CmdType.INPUT, key, detail, 2)
        # pyperclip.copy(title) 

        # pyperclip.paste()
        # webcmd.AddCmd2(CmdType.CLICK, key)
        # webcmd.AddCmd2(CmdType.CTR_V, key) 
        webcmd.Run(True)

    def UploadAdHome(self, webcmd,isHD,lan,applan):
        # bug 上传图片之前先要重新选择语言 不然无法弹出文件浏览器
        # self.SelectLanguage(webcmd,lan)
        # adhome
            # self.SelectLanguage(webcmd,lan)
            # self.driver.switch_to.window(self.driver.window_handles[0])
   
        key = "//div[@id='submitApp_translations.zh_CN.banner_4.android.developer.img']"
        if lan==self.LAN_KEY_EN:
            key = "//div[@id='submitApp_translations.en_US.banner_4.android.developer.img']"
 
        print(key)
   
        item_root = webcmd.Find(key)

        key = ".//div[@class='ant-upload-drag-container']"
        item_div = webcmd.FindChild(item_root,key)
                
        # item = self.driver.find_element(By.XPATH, key) 
        # item_div = webcmd.AddCmd2(CmdType.CLICK_Action, key)
        self.SetItemVisible(item_div)
        webcmd.DoCmd(item_div,CmdType.CLICK)
        time.sleep(1)

        pic = mainResource.GetOutPutAdPathWin32(mainResource.GetProjectOutPut(), Source.TAPTAP, isHD) + "\\"+applan+"\\"+"ad_home_1920x1080.png"
        # pic = mainResource.GetOutPutScreenshotPathWin32(mainResource.GetProjectOutPut(), Source.TAPTAP, True) + "\\"+applan+"\\1080p\\"+"1.jpg"
        pic = os.path.normpath(pic)
        print(pic)
        if Platform.isMacSystem(): 
            pic = pic.replace("\\","/")
            pic = FileUtil.GetLastDirofDir(pic)
            test = 0

        self.OpenFileBrowser(pic, True)
        time.sleep(1)

        # 等待上传完成
        key = ".//span[@class='upload_img']" 
        # print(key)
        item = webcmd.FindChild(item_div,key,True)


        # bug 上传图片之前先要重新选择语言 不然无法弹出文件浏览器
        # self.SelectLanguage(webcmd,lan) 
        key = "//div[@id='submitApp_translations.zh_CN.banner_4.ios.developer.img']"
        if lan==self.LAN_KEY_EN:
            key = "//div[@id='submitApp_translations.en_US.banner_4.ios.developer.img']"

        item_root = webcmd.Find(key)

        key = ".//div[@class='ant-upload-drag-container']"
        item_div = webcmd.FindChild(item_root,key)
        self.SetItemVisible(item_div)
        webcmd.DoCmd(item_div,CmdType.CLICK)
        time.sleep(1)
 
        # print(pic)            
        self.OpenFileBrowser(pic, True)
        time.sleep(1)   

        # 等待上传完成
        key = ".//span[@class='upload_img']" 
        # print(key)
        item = webcmd.FindChild(item_div,key,True)

    def GetLanguageIndex(self,lan):
        index = 0
        for tmp in self.lanKeys:

            if lan==tmp:
                break
                 
            index=index+1

        return index

    def GetItemOfScreenShot(self,lan):
        # en-contents
        # chs-contents
        key = "//div[@id='submitApp_translations.zh_CN.screenshots']"
        if lan==self.LAN_KEY_EN:
            key = "//div[@id='submitApp_translations.en_US.screenshots']"
 

        div = self.driver.find_element(By.XPATH, key) 
        

        # key = ".//input[@type='file' and @data-target='#screenshots']" 
        # item_add = div.find_element(By.XPATH, key)  
        # item_add = None
        # index = 0
        # list = self.driver.find_elements(By.XPATH, key)  
        # for tmp in list:
        #     print("screenshot tag index=",index) 
        #     if index==self.GetLanguageIndex(lan):
        #         item_add = tmp
        #     index=index+1

        return div

    def GetImageScreenShot(self, isHD,lan,idx):
        pic_name = mainResource.GetOutPutScreenshotPathWin32(mainResource.GetProjectOutPut(), Source.TAPTAP, isHD) + "\\"+lan+"\\1080p\\"+str(idx+1)
        pic = pic_name+".jpg"

        if Platform.isMacSystem():
            pic = pic.replace("\\","/")

        # if not os.path.exists(pic):
        #     pic = pic_name+".jpg"
        
        return pic

    def UploadScreenShot(self, webcmd,isHD,lan,applan):
        # screenshot
        for i in range(0, 1):
            # bug 上传图片之前先要重新选择语言 不然无法弹出文件浏览器
            # self.SelectLanguage(webcmd,lan)
            time.sleep(1)
 
            # 将 滚动条 底部对齐


            # lan_shot = "chs-contents"
            # key = "//div[@id='"+lan_shot+"']"
            # div = self.driver.find_element(By.XPATH, key) 
            # if div==None:
            #     print("not find screenshot div")
            #     return

            # 查找子元素
            # 当您启动XPath表达式时//，它会从文档的根目录中搜索，忽略您的父元素。你应该在表达前加上.

            # element2 = driver.find_element_by_xpath("//div[@title='div2']")
            # element2.find_element_by_xpath(".//p[@class='test']").text 

            # key = ".//input[@type='file' and @data-target='#screenshots']" 
            # item = div.find_element(By.XPATH, key)  
            item_root = self.GetItemOfScreenShot(lan) 

            key = ".//div[@class='ant-upload-drag-container']"
            item_div = webcmd.FindChild(item_root,key)
                    
            # item = self.driver.find_element(By.XPATH, key) 
            # item_div = webcmd.AddCmd2(CmdType.CLICK_Action, key)
            self.SetItemVisible(item_div)
            webcmd.DoCmd(item_div,CmdType.CLICK)
 
            time.sleep(1)  

            # pic = mainResource.GetOutPutScreenshotPathWin32(mainResource.GetProjectOutPut(), Source.TAPTAP, isHD) + "\\"+applan+"\\1080p\\"+str(i+1)+".jpg"
            pic = self.GetImageScreenShot(isHD,applan,i)
            if not os.path.exists(pic):
                pic =self.GetImageScreenShot(isHD,Source.LANGUAGE_CN,i)

            if Platform.isMacSystem():
                # apk = FileUtil.GetLastDirofDir(apk)
                pic = pic.replace("\\","/")
                pic = FileUtil.GetLastDirofDir(pic)
                test = 0

            flag = os.path.exists(pic)
            if flag:
                print(pic)
                self.OpenFileBrowser(pic, True)
                time.sleep(2)



            # 等待上传完成
            key = ".//span[@class='upload_img']" 
            # print(key)
            item = webcmd.FindChild(item_root,key,True)

    def CreateApp(self, isHD):
        appid = mainAppInfo.GetAppId(isHD, Source.TAPTAP)
        if len(appid)>1:
            self.FillAppInfo(isHD,appid)
            return

        # url = "https://www.taptap.com/developer/app-create/14628"
        url = "https://developer.taptap.com/14628/create-app"
        self.driver.get(url)
        time.sleep(1)
        webcmd = WebDriverCmd(self.driver)

        # <span data-v-5bf2336f="">创建游戏</span> 
        # key = "//span[contains(text(),上传APK)]"
        # key = "//span[text()='创建游戏']"
        # item = webcmd.Find(key,True)


        # name
        # <input data-v-194bf4a0="" type="text" maxlength="50" class="ant-input ant-input-lg">
        name = self.GetAppName(isHD, Source.LANGUAGE_CN,Source.TAPTAP) 
        print(name)

        print("\r\n")
        print("\r\n")


        detail = self.GetAppDetail(isHD, Source.LANGUAGE_CN)
        print(detail)

        key = "//input[@class='ant-input ant-input-lg']"
        # 等待网页加载完成
        item = webcmd.Find(key,True)

        webcmd.AddCmd(CmdType.INPUT,key,name)

        webcmd.Run(True)


        # 上传icon
        key = "//div[@class='tds-upload-item__operations']"
        webcmd.AddCmd(CmdType.CLICK,key)
        webcmd.Run(True)

        # key = "//svg[@id='iconshanchu_Delete']"
        # # 等待
        # item = webcmd.Find(key,True)
        # webcmd.AddCmd(CmdType.CLICK,key)
        # webcmd.Run(True)

        # iconyanjingzhengkai_EyeOpen1
        key = "//div[@class='tds-upload__icon']"
        # 等待
        item = webcmd.Find(key,True)
        webcmd.DoCmd(item,CmdType.CLICK)

        # icon end

        icon = mainResource.GetOutPutIconPathWin32( mainResource.GetProjectOutPut(), Source.TAPTAP, isHD)+"\\icon_android_512.png"
        print(icon)
        if Platform.isMacSystem(): 
            icon = icon.replace("\\","/")
            icon = FileUtil.GetLastDirofDir(icon)
            test = 0

            # webcmd.Run(True)
        self.OpenFileBrowser(icon, True)
        time.sleep(1)

        # self.UpLoadApk(isHD)

        # wait save
        self.urlold = self.driver.current_url
        while True:
            time.sleep(1)
            self.urlnew = self.driver.current_url
            print("wait save urlnew=", self.urlnew)
            if self.urlnew != self.urlold:
                print("wait save Finish =", self.urlnew)
                break

        # https://developer.taptap.com/14628/app/214597/submit-records?panel=update
        url = self.driver.current_url
 
        
        strfind = "app/"
        idx = url.find(strfind)+len(strfind)
        appid = url[idx:]
        strend = "/"
        idx = appid.find(strend)
        appid = appid[0:idx]
        print(appid)
        mainAppInfo.SetAppId(isHD, Source.ANDROID, Source.TAPTAP, appid)

        # url = "https://www.taptap.com/developer/fill-form/14628"
        # self.driver.get(url)
        # time.sleep(1)

        self.FillAppInfo(isHD,appid)

    def FillAppInfo(self, isHD,appid): 
        # url = "https://developer.taptap.com/14628/app/214597/update-app?panel=appInfo"
        url = "https://developer.taptap.com/14628/app/"+str(appid)+"/update-app?panel=appInfo"
        self.driver.get(url)
        time.sleep(1)

        webcmd = WebDriverCmd(self.driver)
        
                # 等待文件長傳結束
        key = "//span[text()='游戏资料']"
        item = webcmd.Find(key,True)
        
       
        self.lanKeys =[self.LAN_KEY_CN,self.LAN_KEY_EN]
        applans = [Source.LANGUAGE_CN,Source.LANGUAGE_EN]

        detail = self.GetAppDetail(isHD, Source.LANGUAGE_CN)
        print(detail)

        # <textarea data-v-b0e9536c="" class="ant-input"></textarea>
        key = "//textarea[@class='ant-input']"
        webcmd.AddCmd(CmdType.INPUT,key,detail)

        webcmd.Run(True)


        # screenshot 
        # key = "//div[@class='tds-upload__icon']"
        # # 等待
        # item = webcmd.Find(key,True)
        # webcmd.DoCmd(item,CmdType.CLICK)

        return
        # addlans = ("chs","en")
        # addlans = ("default","chs")
        addlans = ["chs"]
        #
        webcmd.AddCmd(CmdType.CLICK, "//div[@id='submitApp_developer_type']", "", 1)
        webcmd.Run(True)

        list = self.driver.find_elements(
            By.XPATH, "//li[@class='ant-select-dropdown-menu-item']")
        list[2].click()
        time.sleep(1)


        # 类型
        webcmd.AddCmd(CmdType.CLICK, "//div[@id='submitApp_category']", "", 1)
        webcmd.Run(True)

        # list = self.driver.find_elements( By.XPATH, "//li[@class='ant-select-dropdown-menu-item']")
        key = "//li[@class='ant-select-dropdown-menu-item' and contains(text(),'休闲') ]"
        # webcmd.DoCmd(list[1],CmdType.CLICK)
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)
        time.sleep(1)

        # 兼容性
        key = "//div[@id='submitApp_lang']"
        item_div = webcmd.Find(key)

        key = ".//span[contains(text(),'简体中文')]"
        subitem = webcmd.FindChild(item_div,key)
        webcmd.DoCmd(subitem,CmdType.CLICK)

        key = ".//span[contains(text(),'English')]"
        subitem = webcmd.FindChild(item_div,key)
        webcmd.DoCmd(subitem,CmdType.CLICK)
         
        # 有内购 
        key = "//div[@id='submitApp_in_app_purchase']"
        item_div = webcmd.Find(key)

        key = ".//span[contains(text(),'否')]"
        subitem = webcmd.FindChild(item_div,key)
        webcmd.DoCmd(subitem,CmdType.CLICK)

        # 需要网络
        # ><input name="network" type="radio" class="ant-radio-input" value="yes">
        key = "//input[@name='network' and @type='radio' and @value='yes']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)


        # 添加多语言

        key = "//div[@id='AnchorGameData']"
        item_div = webcmd.Find(key)

       


        for lan in range(0, len(self.lanKeys)): 

            self.SelectLanguage(webcmd,self.lanKeys[lan])
 
            self.UploadTitle(webcmd,isHD,self.lanKeys[lan],applans[lan])
  
            self.UploadIcon(webcmd,isHD,self.lanKeys[lan])
            
            self.UploadAdHome(webcmd,isHD,self.lanKeys[lan],applans[lan])


            self.UploadScreenShot(webcmd,isHD,self.lanKeys[lan],applans[lan])
 
            
            
            # break
 

        # 游戏状态 [Android]
        # 兄弟节点
        key = "//span[@class='th_middle' and contains(text(),'测试')]/../span[@class='tap-radio_point']"
        # brother
        # <span data-v-8bce4f2c="" class="tap-radio_point"></span>
        # webcmd.AddCmd(CmdType.CLICK, key) 
        webcmd.Run(True)

        self.SubmitApp(True)

    def GoToAPPPage(self, isHD):
        appid = mainAppInfo.GetAppId(isHD, Source.TAPTAP)
        # url = "https://www.taptap.com/developer/dashboard/14628?app_id="+appid
        url = "https://developer.taptap.com/14628/app/"+appid+"/update-app?panel=basicInfo"
        print(url)
        self.driver.get(url)
        time.sleep(1)

    def GotoUploadPage(self, isHD):
        appid = mainAppInfo.GetAppId(isHD, Source.TAPTAP)
        # url = "https://www.taptap.com/developer/dashboard/14628?app_id="+appid
        url = "https://developer.taptap.com/14628/app/"+appid+"/update-app?panel=uploadAPK"
        print(url)
        self.driver.get(url)
        time.sleep(1)

    def UpLoadApk(self, isHD):
        webcmd = WebDriverCmd(self.driver)

        self.urlold = self.driver.current_url
        old_window = self.driver.current_window_handle
        print("urlold=", self.urlold)

        # key = "//span[contains(text(),上传APK)]"
        key = "//span[text()='上传APK']"
        item = webcmd.Find(key,True)
       
        webcmd.AddCmd(CmdType.CLICK_Action,key)
        webcmd.Run(True)

        key = "//span[text()='确 定']" 
        webcmd.AddCmd(CmdType.CLICK_Action,key)
        webcmd.Run(True)
        
        # key =  "//div[@class='container--form upload-apk-wrapper old-style']"
        # item = webcmd.Find(key)
        # key = ".//button[@class='btn--edit ant-btn ant-btn-primary']"
        # subitem = webcmd.FindChild(item,key) 
        # webcmd.DoCmd(subitem,CmdType.CLICK)
        
        
        # # <a data-toggle="modal" data-target=".confirm-upload-apk" class="btn btn-primary">上传APK</a>
        # # item = self.driver.find_element(
        # #     By.XPATH, "//a[@data-target='.confirm-upload-apk']")
        # # # item = self.driver.find_element(By.XPATH, "//a[@data-toggle='modal']")
        # # item.click()
        # time.sleep(2)

        # # <a id="selectfiles" href="javascript:void(0);" class="btn btn-primary" style="position: relative; z-index: 1;">开始上传APK</a>
        # item = self.driver.find_element(By.XPATH, "//a[@id='selectfiles']")
        # item.click()
        # time.sleep(2)

        # 手动点击上传
        # webcmd.WaitKeyBoard("q")
        apk = mainResource.GetOutPutApkPathWin32(mainResource.GetProjectOutPut(), Source.TAPTAP, isHD)
        if not os.path.exists(apk):
            apk = mainResource.GetOutPutApkPathWin32(mainResource.GetProjectOutPut(), Source.HUAWEI, isHD)

        if Platform.isMacSystem():
            apk = FileUtil.GetLastDirofDir(apk)

        # F:\\sourcecode\\unity\\product\\kidsgame\\ProjectOutPut\\xiehanzi\\hanziyuan\\screenshot\\shu\\cn\\480p\\1.jpg
        self.OpenFileBrowser(apk, True)
        time.sleep(1)


        # 等待文件長傳結束
        key = "//a[@title='基础信息']"
        item = webcmd.Find(key,True)
      

        # 檢查是否文件長傳結束
        # while True:
        #     time.sleep(2)
        #     # for win in self.driver.window_handles:
        #     #     if win!=old_window:
        #     #         self.driver.switch_to.window(win)
        #     #         self.urlold = self.driver.current_url
        #     #         old_window = win
        #     #         print("urlold 2=",self.urlold)

        #     # self.driver.switch_to.window(self.driver.windowop_handles[0])
        #     self.urlnew = self.driver.current_url
        #     print("urlnew=", self.urlnew)
        #     if self.urlnew != self.urlold:
        #         print("new page =", self.urlnew)
        #         print("apk upload finish")
        #         break

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

    def SubmitApp(self,isYes):
        # 未成年人防沉迷
        # <input required="" type="radio" name="anti_addiction_read" value="1">
        item = self.driver.find_element(
            By.XPATH, "//input[@name='anti_addiction_read']")
        item.click()
        time.sleep(1)
        # <input required="required" type="radio" name="anti_addiction_status" value="1">
        item = self.driver.find_element(
            By.XPATH, "//input[@name='anti_addiction_status']")
        item.click()
        time.sleep(1)

        # 等待后台apk解析
        time.sleep(10)

        if isYes:
            # 提交审核
            # <button id="postAppSubmitV2" type="submit" value="submit" class="leave_current_page btn btn-primary btn-lg">保存并提交审核</button>
            item = self.driver.find_element(
                By.XPATH, "//button[@id='postAppSubmitV2']")
            item.click()
            time.sleep(1)

            # 确定

            # section = self.driver.find_element(By.XPATH, "//section[@class='modal fade taptap-modal global-tip-modal in']")
            # # <button class="btn btn-primary" data-default-text="确定">确定</button>
            # # item = self.driver.find_element(By.XPATH, "//button[@data-default-text='确定']")
            # item = section.find_element(By.XPATH, "//button[@data-default-text='确定']")
            list = self.driver.find_elements(
                By.XPATH, "//button[@data-default-text='确定']")
            item = list[1]
            print("确定")
            self.driver.execute_script("arguments[0].click();", item)
            time.sleep(1)

    def UpdateApp(self, isHD):
        appid = mainAppInfo.GetAppId(isHD, Source.TAPTAP)
        # dir = self.rootDirProjectOutPut

        if appid == "0":
            self.SearchApp(isHD)
            time.sleep(1)

        self.GotoUploadPage(isHD)
        # print("UpdateApp appid=",appid," isHD="+isHD)
        # https://www.taptap.com/developer/app-update/56016/14628
        time.sleep(2)
        old_window = self.driver.current_window_handle
        # key = "//a[@data-taptap-btn='updateAppData']"
        # if self.IsElementExist(key):
        #     item = self.driver.find_element(By.XPATH, key)
        #     item.click()
        #     time.sleep(2)
        # else:
        #     print("updateAppData button not find ")
        #     print("updateAppData current_url=", self.driver.current_url)
        #     self.UpdateApp(isHD)

        # 跳转到新的页面
        # print("self.driver.current_url=", self.driver.current_url)
        # self.driver.switch_to.window(self.driver.window_handles[0])
        # for win in self.driver.window_handles:
        #     if win != old_window:
        #         self.driver.switch_to.window(win)
        # time.sleep(1)
        # print("self.driver.current_url 2=", self.driver.current_url)
        webcmd = WebDriverCmd(self.driver)
 

        #  <div data-v-f6e15f96="" class="apk-upload-mask"></div>
        key = "//div[@class='apk-upload-mask']"
        
        item = webcmd.Find(key,True)
        webcmd.DoCmd(item,CmdType.CLICK)

        self.UpLoadApk(isHD)

        # https://www.taptap.com/developer/fill-form/14628?apk_id=496448&app_id=56016

        self.SubmitApp(True)

    def SearchApp(self, ishd):
        name = self.GetAppName(ishd, Source.LANGUAGE_CN,Source.TAPTAP)
        webcmd = WebDriverCmd(self.driver)

        self.driver.get(
            "https://developer.taptap.com/14628/all-app")
        time.sleep(2)

        key = "//input[@class='ant-select-search__field']"
        webcmd.AddCmd(CmdType.INPUT,key,name)

        webcmd.Run(True)

        time.sleep(1)
# <li role="option" class="ant-select-dropdown-menu-item" unselectable="on" style="user-select: none;"> 诗词大挑战HD（测试版） </li>
        key = "//div[@class='ant-select-dropdown-content']"
        div = webcmd.Find(key)

        # 202132
        
      
        list = div.find_elements_by_xpath("ul/li")
        for li in list:
            title = li.text
            print(title)
            if title.find(name) == 0:
                webcmd.DoCmd(li,CmdType.CLICK)
                # app_id=56016
                # url = li.get_attribute('href')
                # strfind = "app_id="
                # idx = url.find(strfind)+len(strfind)
                # print(url)
                # appid = url[idx:]
                # print(appid)
                # mainAppInfo.SetAppId(ishd, Source.ANDROID, Source.TAPTAP, appid)
                break


# 主函数的实现
    def Run(self,type, isHD):      
        self.Init()
        print("AppStoreTaptap Run isHD=",str(isHD))
        # try: 
        self.GoHome(isHD, True)
        self.Login("651577315", "qq31415926")
        # except Exception as e:  
        #     print("Login eror=",e)

 
        if type == "createapp":
            self.CreateApp(isHD)
            time.sleep(3)
            # ad.CreateApp(True)

        if type == "update":
            if isHD == True:
                self.UpdateApp(True)
            else:
                self.UpdateApp(False)
                time.sleep(3)
                # self.UpdateApp(True)

        if type == "getappid":
            self.SearchApp(False)
            time.sleep(3)
            self.SearchApp(True)

        # ad.Quit(30)

        print("AppStoreTaptap sucess")

mainAppStoreTaptap = AppStoreTaptap()
