# 导入selenium的浏览器驱动接口

  
import sqlite3
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
 
import sys
import os
import json
sys.path.append('../../') 
sys.path.append('./') 
from Project.Resource import mainResource
from Common import Source
from Common.Common import Common
from Project.Resource import mainResource 
from Common import Source
from Common.File.FileUtil import FileUtil 
from Common.File.FileBrowser import FileBrowser
from AppInfo.AppInfo import mainAppInfo

import pyperclip
from Common.WebDriver.WebDriverCmd import CmdType
from Common.WebDriver.WebDriverCmd import WebDriverCmd 
from Common.WebDriver.WebDriverCmd import CmdInfo 
 

import keyboard #Using module keyboard

from Ad.AdBase import AdBase
# from Ad.ParseAdGdt import ParseAdGdt

# 要想调用键盘按键操作需要引入keys包

# 导入chrome选项


# pip3 install pywin32

# sys.path.append('../common')


class AdGdt(AdBase):
    driver: None
    dirRoot: None
    urlCreatePlaceId: None
    osApp: None

    def saveString2File(self, str, file):
        f = open(file, 'wb')  # 若是'wb'就表示写二进制文件
        b = str.encode('utf-8', "ignore")
        f.write(b)
        f.close()

    def SetCmdPath(self, str):
        dir = FileUtil.GetLastDirofDir(str)
        dir = FileUtil.GetLastDirofDir(dir)
        dir = FileUtil.GetLastDirofDir(dir)
        self.dirRoot = dir
        print("dir = ", dir)

    def GoHome(self):
        # 加载百度页面
        # driver.get("https://developer.huawei.com/consumer/cn/")
        self.driver.get("https://adnet.qq.com/index")
        # time.sleep(5)

        # self.saveString2File(self.driver.page_source,"1.html")
        #   # 点击登录按钮
        # self.driver.find_element_by_id('switcher_plogin').click()
        # time.sleep(1)

    def Login(self, user, password):
        self.urlold = self.driver.current_url
        print("Login urlold=", self.urlold)
        # 用扫描登录 不要执行LoginQQ
        # self.LoginQQ(user, password)
        self.SaveCookie()
        # 等待登录成功
        while True:
            time.sleep(1)
            self.urlnew = self.driver.current_url
            print("Login urlnew=", self.urlnew)
            if self.urlnew != self.urlold:
                print("Login Finish =", self.urlnew)
                break

    def LoginQQ(self,user,password):
        # 3452644866 
        webcmd = WebDriverCmd(self.driver) 
        print("waiting for login")
        time.sleep(2)
        webcmd.WaitKeyBoard("q")
        return
        # return
        # driver.add_cookie("[{'domain': '.id1.cloud.huawei.com', 'expiry': 1908869785, 'httpOnly': False, 'name': 'sid', 'path': '/', 'secure': True, 'value': '2049382e3828ef4470bef8b426c4bb3370e7d9e1147f53a18839e47dad7caf10a233e61ee15337b4373e'}, {'domain': '.id1.cloud.huawei.com', 'expiry': 1908869785, 'httpOnly': False, 'name': 'hwid_cas_sid', 'path': '/', 'secure': True, 'value': '2049382e3828ef4470bef8b426c4bb3370e7d9e1147f53a18839e47dad7caf10a233e61ee15337b4373e'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_idts_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1593336984125'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_id_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': 'cf787be41ac24d65887dcd20c826ac97'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_idvc_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1593338788, 'httpOnly': False, 'name': 'HW_idn_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': 'ec569450f0ac4cd78fc72965d91ec7e8'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1608888984, 'httpOnly': False, 'name': 'HW_refts_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1593336984124'}, {'domain': '.id1.cloud.huawei.com', 'httpOnly': True, 'name': 'CAS_THEME_NAME', 'path': '/', 'secure': True, 'value': 'red'}, {'domain': 'id1.cloud.huawei.com', 'httpOnly': False, 'name': 'cookieBannerOnOff', 'path': '/', 'secure': False, 'value': 'true'}, {'domain': '.id1.cloud.huawei.com', 'httpOnly': True, 'name': 'VERSION_NO', 'path': '/', 'secure': True, 'value': 'UP_CAS_4.0.4.100'}, {'domain': 'id1.cloud.huawei.com', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/CAS', 'secure': True, 'value': '144E8B2ED3F5D9C8576742C1DDF4CF3D0DCF6949E13D6943'}]")
        self.driver.switch_to.frame("ptlogin_iframe")
        time.sleep(2)

        # key =  "//div[@id='qqLoginCt']"
        # webcmd.AddCmdWait(CmdType.CLICK,key)
        # webcmd.Run(True)

        self.driver.find_element_by_id('switcher_plogin').click()
        time.sleep(1)

        item = self.driver.find_element(
            By.XPATH, "//input[@id='u']")
        item.send_keys(user)

        item = self.driver.find_element(By.XPATH, "//input[@id='p']")
        item.send_keys(password)

        item = self.driver.find_element(
            By.XPATH, "//input[@id='login_button']")
        item.click()
        time.sleep(5)

        # cookie = self.driver.get_cookies()
        # print(cookie)
        # [{'domain': '.id1.cloud.huawei.com', 'expiry': 1908869785, 'httpOnly': False, 'name': 'sid', 'path': '/', 'secure': True, 'value': '2049382e3828ef4470bef8b426c4bb3370e7d9e1147f53a18839e47dad7caf10a233e61ee15337b4373e'}, {'domain': '.id1.cloud.huawei.com', 'expiry': 1908869785, 'httpOnly': False, 'name': 'hwid_cas_sid', 'path': '/', 'secure': True, 'value': '2049382e3828ef4470bef8b426c4bb3370e7d9e1147f53a18839e47dad7caf10a233e61ee15337b4373e'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_idts_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1593336984125'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_id_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': 'cf787be41ac24d65887dcd20c826ac97'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_idvc_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1593338788, 'httpOnly': False, 'name': 'HW_idn_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': 'ec569450f0ac4cd78fc72965d91ec7e8'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1608888984, 'httpOnly': False, 'name': 'HW_refts_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1593336984124'}, {'domain': '.id1.cloud.huawei.com', 'httpOnly': True, 'name': 'CAS_THEME_NAME', 'path': '/', 'secure': True, 'value': 'red'}, {'domain': 'id1.cloud.huawei.com', 'httpOnly': False, 'name': 'cookieBannerOnOff', 'path': '/', 'secure': False, 'value': 'true'}, {'domain': '.id1.cloud.huawei.com', 'httpOnly': True, 'name': 'VERSION_NO', 'path': '/', 'secure': True, 'value': 'UP_CAS_4.0.4.100'}, {'domain': 'id1.cloud.huawei.com', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/CAS', 'secure': True, 'value': '144E8B2ED3F5D9C8576742C1DDF4CF3D0DCF6949E13D6943'}]
 

 
    def Init(self):
        # 创建chrome浏览器驱动，无头模式（超爽）
        chrome_options = Options()
        # chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # 全屏
        self.driver.maximize_window()
        # 具体大小
        # driver.set_window_size(width, height)

        # self.GoHome()
        # self.Login()
        # time.sleep(2)
        # GoAppgallery(driver)

        #     # 快照显示已经成功登录
        # print(driver.save_screenshot('jietu.png'))
        # driver.quit()

    def Quit(self):
        self.driver.quit()

# 3452644866 qq31415926
    def CreateApp(self, isHD):
        self.driver.get("https://adnet.qq.com/medium/add")
        time.sleep(1)
        webcmd = WebDriverCmd(self.driver) 


        appChannel = Source.TAPTAP
        appid = mainAppInfo.GetAppId(isHD, Source.TAPTAP)
        if appid=="0":
            appid = mainAppInfo.GetAppId(isHD, Source.HUAWEI)
            appChannel = Source.HUAWEI

        # Android平台
        item = self.driver.find_element(
            By.XPATH, "//button[@data-id='mediumTypeSelector']")
        item.click()

        time.sleep(1)

        list = self.driver.find_elements(
            By.XPATH, "//a[@role='option']")

        if self.osApp == Source.ANDROID:
            list[0].click()

        if self.osApp == Source.IOS:
            list[1].click()

        # 应用商店

        item = self.driver.find_element(
            By.XPATH, "//button[@data-id='appStoreSelector']")
        item.click()

        time.sleep(1)

        ul_list = self.driver.find_elements(
            By.XPATH, "//ul[@class='dropdown-menu inner']")

        list = ul_list[1].find_elements(
            By.XPATH, "//a[@role='option']")
        
        idx = 0
        if appChannel == Source.TAPTAP:
            idx = 9
        else:
                # huawei
            idx = 7


        if self.osApp == Source.ANDROID:
            list[idx].click()

        if self.osApp == Source.IOS:
            list[0].click()


    # 应用分类
        item = self.driver.find_element(
            By.XPATH, "//button[@data-id='industryOneSelector']")
        item.click()
        time.sleep(1)
        ul_list = self.driver.find_elements(
            By.XPATH, "//ul[@class='dropdown-menu inner']")
        list = ul_list[2].find_elements(
            By.XPATH, "//a[@role='option']")
        list[12].click()

        item = self.driver.find_element(
            By.XPATH, "//button[@data-id='industrySecondSelector']")
        item.click()
        time.sleep(1)
        ul_list = self.driver.find_elements(
            By.XPATH, "//ul[@class='dropdown-menu inner']")
        list = ul_list[3].find_elements(
            By.XPATH, "//a[@role='option']")
        list[3].click()

        # url
        item = self.driver.find_element(
            By.XPATH, "//input[@class='form-control size-410 form-control']")
        
        
        url = ""
        if self.osApp == Source.ANDROID:
            if appChannel == Source.TAPTAP:
                url = "https://www.taptap.com/app/"+appid
            else:
                # url = "http://appstore.huawei.com/C"+appid
                # https://appgallery1.huawei.com/#/app/C100358289
                url = "https://appgallery1.huawei.com/#/app/C"+appid               

        if self.osApp == Source.IOS:
            appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)
            # https://itunes.apple.com/cn/app/id1303020002
            # https://apps.apple.com/cn/app/id668407890
            url = "https://apps.apple.com/cn/app/id"+appid
        
        item.send_keys(url)

        # name
        name = self.GetAppName(isHD)
        list = self.driver.find_elements(
            By.XPATH, "//input[@id='placementName']")
        list[0].send_keys(name)

        list = self.driver.find_elements(
            By.XPATH, "//input[@id='placementName']")
        list[1].send_keys(name)

        item = self.driver.find_element_by_id('formControlsTextarea')
        name += name
        name += name
        name += name
        name += name
        item.send_keys(name)

        item = self.driver.find_element(
            By.XPATH, "//input[@id='packageName']")
        package = mainAppInfo.GetPackage(Source.ANDROID, isHD)
        item.send_keys(package)

        key = "//button[@id='spaui-uploader_2-empty']"
        webcmd.AddCmd(CmdType.CLICK_Action,key)
        webcmd.Run(True)
        time.sleep(1)
        self.OpenFileBrowser()
        time.sleep(2)

    # 创建

        item = self.driver.find_element(
            By.XPATH, "//a[@class='btn btn-primary btn-160']")
        item.click()

    def GetAppName(self, ishd):
        name = mainAppInfo.GetAppName(self.osApp, ishd,Source.LANGUAGE_CN)
        # if self.osApp == Source.IOS:
        #     AppInfo.GetAppName(self.osApp, ishd)+self.osApp

        return name
 
  #获取cookies保存到文件
    def SaveCookie(self):
        cookies=self.driver.get_cookies()
        json_cookies=json.dumps(cookies)
        with open('e:/cookies/cookies_gdt.json','w') as f:
            f.write(json_cookies)
    #读取文件中的cookie
    def AddCookie(self):
        self.driver.delete_all_cookies()
        dict_cookies={}
        with open('e:/cookies/cookies_gdt.json','r',encoding='utf-8') as f:
            list_cookies=json.loads(f.read())
            for i in list_cookies:
                self.driver.add_cookie(i)


    def SearchApp(self, ishd):
        name = self.GetAppName(ishd)
        self.driver.get("https://adnet.qq.com/medium/list")
        time.sleep(3)

        webcmd = WebDriverCmd(self.driver) 
        key = "//input[@class='form-control']"
        item = webcmd.Find(key,True)
        time.sleep(1)
        item.send_keys(name)
        # item.send_keys("儿童写汉字")

        time.sleep(1)

        # search
        self.driver.find_element_by_id('search_medium_id').click()
        time.sleep(2)
 
        # 筛选
        item = self.driver.find_element(By.XPATH, "//button[@class='btn filter-operate']")
        # item = self.driver.find_element(By.XPATH, "//div[@class='filter-parent-control']")

        # error
        # item.click()  
        self.driver.execute_script("arguments[0].click();", item)
        time.sleep(2)

# <input type="checkbox" class="check" name="" value="IOS"> 
        if self.osApp == Source.ANDROID:
            item = self.driver.find_element(By.XPATH, "//input[@value='Android']")
            # item.click()
            self.driver.execute_script("arguments[0].click();", item)
            time.sleep(1)

        if self.osApp == Source.IOS:
            item = self.driver.find_element(By.XPATH, "//input[@value='IOS']")
            # item.click()
            self.driver.execute_script("arguments[0].click();", item)
            time.sleep(1)
         
        # 确定
        item = self.driver.find_element(By.XPATH, "//button[@class='btn btn-primary']")
        # item.click()
        self.driver.execute_script("arguments[0].click();", item)
        time.sleep(2)


        # 点击第一个
        # <span class="media-heading" title="天天开心拼图">天天开心拼图</span>
        # key = "//span[@class='media-heading' and title ='"+name+"']"
        key = "//span[@class='media-heading']"
        list = self.driver.find_elements(By.XPATH, key)
        for span in list:
            if span.get_attribute('title') == name:
                span.click()
                time.sleep(1)


    def SearchAppAddPlace(self, ishd):

        self.SearchApp(ishd)

        # 新建广告
        list = self.driver.find_elements(
            By.XPATH, "//a[@class='btn btn-default btn-120']")
        a = list[1]
        url = a.get_attribute('href')
        print(url)
        self.urlCreatePlaceId = url
        # a.click()
        # time.sleep(1)

   
    def GetAdId(self, tr, keyword):
        webcmd = WebDriverCmd(self.driver)
        adid = "0"
        key = ".//div[@class='inner']"
        list = webcmd.FindListChild(tr,key)
        # print("GetAdId list =",len(list)) 
        for div in list:
            # print("GetAdId keyword =",keyword," div.text=",div.text) 
            if div.text == keyword:
                keytmp = ".//span[@class='field-value']"
                h4 = webcmd.FindChild(tr,keytmp)
                adid = h4.text
                # print("GetAdId adid = ", adid)
        return adid

 
    def ParseAdInfo(self,ishd):
        webcmd = WebDriverCmd(self.driver)
        
        self.adIdBanner = "0" 
        self.adIdInsert = "0" 
        self.adIdVideo = "0" 
        self.adIdNative = "0" 
        self.adIdSplash = "0"  



        key = "//div[@class='media media-info-general']"
        div = webcmd.Find(key,True)
        key = ".//span[@class='text']"
        h4 = webcmd.FindChild(div,key)
        self.appName = h4.text
        print(self.appName)

        key = ".//span[@class='field-value']"
        h4 = webcmd.FindChild(div,key)
        self.appId = h4.text
        print(self.appId)

        key = "//table[@class='table media-table js-media-details']"
        table = webcmd.Find(key)

        key = ".//tr"
        list = webcmd.FindListChild(table,key)
        print("list =",len(list))
        if len(list)==0:
            print("retry get ad list")
            self.ParseAdInfo(ishd)

        for tr in list:
  # 横幅
            if self.adIdBanner == "0":
                self.adIdBanner = self.GetAdId(tr, "Banner2.0")
                # print("Banner 0:", self.adIdBanner)

            # 插屏
            if self.adIdInsert  ==  "0":
                self.adIdInsert = self.GetAdId(tr, "插屏2.0")

            # 激励视频
            if self.adIdVideo  ==  "0":
                self.adIdVideo = self.GetAdId(tr, "激励视频")
            # 原生
            if self.adIdNative  == "0":
                self.adIdNative = self.GetAdId(tr, "原生")

            # 开屏
            if self.adIdSplash  == "0":
                self.adIdSplash = self.GetAdId(tr, "开屏")
 
 

        print("Banner:", self.adIdBanner)
        print("插屏:", self.adIdInsert)
        print("激励视频:", self.adIdVideo)
        print("原生:", self.adIdNative)
        print("开屏:", self.adIdSplash)

        self.SaveAdIdToJson(self.osApp,ishd,Source.GDT)


    def SearchAppGetAdInfo(self, ishd):
        self.SearchApp(ishd)
        webcmd = WebDriverCmd(self.driver)

        # 关联广告位
        key = "//a[@style='cursor: pointer;']"
        item = webcmd.Find(key,True)
        item = webcmd.AddCmdList(CmdType.CLICK_Action, key,1,1)
        webcmd.Run(True)

        # 关联广告位
        # <a style="cursor: pointer;">关联广告位</a>
        # list = self.driver.find_elements(
        #     By.XPATH, )
        # a = list[1]
        # a.click()
        time.sleep(1)

        # table media-table js-media-details
        # table = self.driver.find_element(By.XPATH, "//table[@class='table media-table js-media-details']")
        # list = table.find_elements_by_xpath('//tbody/tr')
        # print("tr len =",len(list))
        # print(table.get_attribute('innerHTML'))
        # for tr in list:
        #     span_list = tr.find_elements_by_xpath("//span")
        #     # [@class='field-value']
        #     # print(span_list[1].text)

        self.ParseAdInfo(ishd)
        # parse = ParseAdGdt()
        # parse.ParseAdData(self.driver.page_source, ishd, self.osApp)

    def GetAdInfo(self, isHD):
        self.SearchAppGetAdInfo(isHD)

    def CreatePlaceId(self, isHD):
        self.SearchAppAddPlace(isHD)
        self.CreateAdBanner(isHD)
        self.CreateAdInsert(isHD)
        self.CreateAdVideo(isHD)
        time.sleep(1)
        self.GetAdInfo(isHD)

    def OpenFileBrowser(self):
        FileBrowser.OpenFile("F:\\sourcecode\\unity\\product\\kidsgame\\ProjectOutPut\\xiehanzi\\xiehanzi\\screenshot\\shu\\cn\\480p\\1.jpg",True)
 

    def CreateAdBanner(self, isHD):
        # self.driver.get("https://adnet.qq.com/placement/add")
        # https://adnet.qq.com/placement/60503466885129/add
        self.driver.get(self.urlCreatePlaceId)
        time.sleep(1)
        webcmd = WebDriverCmd(self.driver)

        time.sleep(3)

        # div class="card-inner"
        # list = self.driver.find_elements(
        #     By.XPATH, "//div[@class='card-inner']")
        # list[4].click()
        # time.sleep(2)
        key = "//div[@class='card-inner']"
        webcmd.AddCmdList(CmdType.CLICK_Action, key,4,2)
        webcmd.Run(True) 
 
        key = "//ul[@class='union-card-list card-list-banner list-contain-1']"
        ul = webcmd.Find(key,True) 

        # bug
        # list = ul.find_elements(By.XPATH, "//li[@class='union-card-item']")
        # ok 查找子元素li
        list = ul.find_elements_by_xpath('li')
        li = list[0]
        li.click()
        time.sleep(1)

        # item = self.driver.find_element(By.XPATH, "//input[@class='spaui-input has-normal spaui-component']")
        list = self.driver.find_elements(By.XPATH, "//input[@type='text']")
        # self.driver.execute_script("arguments[0].scrollIntoView();", item)
        # self.driver.execute_script('window.scrollTo(0,1000000)')
        time.sleep(1)
        list[1].send_keys("b")

        # upload image 
        # key = "//button[@id='spaui-uploader_2-empty']"
        # webcmd.AddCmdList(CmdType.CLICK_Action, key)
        # webcmd.Run(True) 
        # time.sleep(2)
        # self.OpenFileBrowser()
        # time.sleep(2)
        self.UploadImage(True)

        
        # <div class="text title">请上传广告位展示截图</div>


        # finish
        self.OnClickFinish()

    
    def OnClickFinish(self):
        webcmd = WebDriverCmd(self.driver)
        keyFinish = "//button[@class='union-complete-btn spaui-button spaui-button-primary spaui-component']"
        webcmd.AddCmd(CmdType.CLICK_Action, keyFinish)
        webcmd.Run(True) 

        key = "//div[@class='text title' and text()='请上传广告位展示截图']"
        if webcmd.IsElementExist(key):
            # 确定
            key = "//button[@class=' t']"
            webcmd.AddCmd(CmdType.CLICK_Action, key)
            webcmd.Run(True) 

            # 重新上传
            time.sleep(1)
            print("请上传广告位展示截图")
            self.UploadImage(False)
            webcmd.AddCmd(CmdType.CLICK_Action, keyFinish)
            webcmd.Run(True)


    def UploadImage(self, isAuto):
        print('UploadImage isAuto',isAuto)
        webcmd = WebDriverCmd(self.driver)
        if isAuto==True:
            key = "//button[@id='spaui-uploader_2-empty']"
            webcmd.AddCmd(CmdType.CLICK_Action, key)
            webcmd.Run(True) 
            time.sleep(1)
            self.OpenFileBrowser()
            time.sleep(3)
        else:
            key_press = 'q'
            while True:#making a loop
                time.sleep(1)
                print('waiting for key press = ',key_press)
                # try:  
                if keyboard.is_pressed(key_press):
                    print('You Pressed A Key!')
                    break
             

    def CreateAdInsert(self, isHD):
        webcmd = WebDriverCmd(self.driver)
        # self.driver.get("https://adnet.qq.com/placement/add")
        # https://adnet.qq.com/placement/60503466885129/add
        self.driver.get(self.urlCreatePlaceId)
        time.sleep(1)

        time.sleep(3)

        # div class="card-inner"
        key = "//div[@class='card-inner']"
        webcmd.AddCmdList(CmdType.CLICK_Action, key,5,2)
        webcmd.Run(True) 


        # <ul class="union-card-list card-list-banner list-contain-1"
        key = "//ul[@class='union-card-list card-list-cp list-contain-2']"
        ul = webcmd.Find(key,True) 

        # bug
        # list = ul.find_elements By.XPATH, "//li[@class='union-card-item']")
        # ok 查找子元素li
        list = ul.find_elements_by_xpath('li')

        list[1].click()
        time.sleep(1)

        # item = self.driver.find_element(By.XPATH, "//input[@class='spaui-input has-normal spaui-component']")
        list = self.driver.find_elements(By.XPATH, "//input[@type='text']")
        # self.driver.execute_script("arguments[0].scrollIntoView();", item)
        # self.driver.execute_script('window.scrollTo(0,1000000)')
        time.sleep(1)
        list[1].send_keys("i")

        # upload image
        # item = self.driver.find_element(
        #     By.XPATH, "//button[@id='spaui-uploader_2-empty']")
        # item.click()
        # time.sleep(1)
        # self.OpenFileBrowser()
        # time.sleep(1)
        self.UploadImage(True)

        # finish
        # item = self.driver.find_element(
        #     By.XPATH, "//button[@class='union-complete-btn spaui-button spaui-button-primary spaui-component']")
        # item.click()
        # time.sleep(1)
        # finish
        self.OnClickFinish()


    def CreateAdVideo(self, isHD):
        webcmd = WebDriverCmd(self.driver)
        # self.driver.get("https://adnet.qq.com/placement/add")
        # https://adnet.qq.com/placement/60503466885129/add
        self.driver.get(self.urlCreatePlaceId)
        time.sleep(1)

        time.sleep(3)

        # div class="card-inner" 
        key = "//div[@class='card-inner']"
        webcmd.AddCmdList(CmdType.CLICK_Action, key,2,2)
        webcmd.Run(True) 

        # item = self.driver.find_element(By.XPATH, "//input[@class='spaui-input has-normal spaui-component']")
        list = self.driver.find_elements(By.XPATH, "//input[@type='text']")
        # self.driver.execute_script("arguments[0].scrollIntoView();", item)
        # self.driver.execute_script('window.scrollTo(0,1000000)')
        time.sleep(1)
        list[1].send_keys("v")

        # upload image
        # item = self.driver.find_element(
        #     By.XPATH, "//button[@id='spaui-uploader_2-empty']")
        # item.click()
        # time.sleep(1)
        # self.OpenFileBrowser()
        # time.sleep(1)
        self.UploadImage(True)

        # finish
        # item = self.driver.find_element(
        #     By.XPATH, "//button[@class='union-complete-btn spaui-button spaui-button-primary spaui-component']")
        # item.click()
        # time.sleep(1)
        # finish
        self.OnClickFinish()


    def Run(self,type, os,isHD):       
        self.Init()
        self.GoHome()
        self.Login("3452644866","qq31415926")
 
        self.osApp = os
        if type == "createapp":
            if isHD:
                self.CreateApp(isHD)
            else:
                self.CreateApp(False)
                time.sleep(3)
                self.CreateApp(True)

        if type == "createplaceid":
            self.CreatePlaceId(False)
            time.sleep(3)
            self.CreatePlaceId(True)

        if type == "adinfo":
            self.GetAdInfo(False)
            time.sleep(3)
            self.GetAdInfo(True)

        print("AdGdt sucess")   

mainAdGdt = AdGdt()
