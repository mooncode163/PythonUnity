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

import pyperclip

from Project.Resource import mainResource
from Common import Source 
from Common.File.FileUtil import FileUtil 
from AppInfo.AppInfo import mainAppInfo
  
import time; 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver

# 要想调用键盘按键操作需要引入keys包

# 导入chrome选项


# pip3 install pywin32

# sys.path.append('../common')


class AsoQimai:

    defaultLanguage = "美式英语"
    fileCookie = "e:/cookies/cookies_huawei.json" 
    def Init(self):
        # 创建chrome浏览器驱动，无头模式（超爽）
        chrome_options = Options()
        # chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # 全屏
        self.driver.maximize_window()
        # 具体大小
        # driver.set_window_size(width, height)

        
        # self.Login()
        # time.sleep(2)
        # GoAppgallery(driver)

        #     # 快照显示已经成功登录
        # print(driver.save_screenshot('jietu.png'))
        # driver.quit()

    def GoHome(self, isHD): 
        url = "https://www.qimai.cn"
        print(url)
        self.driver.get(url)
        self.urlold = self.driver.current_url
        time.sleep(3)
 

# 
    def Login(self, user, password):
        # 3452644866

        # 等待扫码登录
        while True:
            time.sleep(1)
            self.urlnew = self.driver.current_url
            if self.urlnew != self.urlold:
                break
            print("waiting for login self.urlnew=",self.urlnew)

        return

        # driver.add_cookie("[{'domain': '.id1.cloud.huawei.com', 'expiry': 1908869785, 'httpOnly': False, 'name': 'sid', 'path': '/', 'secure': True, 'value': '2049382e3828ef4470bef8b426c4bb3370e7d9e1147f53a18839e47dad7caf10a233e61ee15337b4373e'}, {'domain': '.id1.cloud.huawei.com', 'expiry': 1908869785, 'httpOnly': False, 'name': 'hwid_cas_sid', 'path': '/', 'secure': True, 'value': '2049382e3828ef4470bef8b426c4bb3370e7d9e1147f53a18839e47dad7caf10a233e61ee15337b4373e'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_idts_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1593336984125'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_id_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': 'cf787be41ac24d65887dcd20c826ac97'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_idvc_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1593338788, 'httpOnly': False, 'name': 'HW_idn_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': 'ec569450f0ac4cd78fc72965d91ec7e8'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1608888984, 'httpOnly': False, 'name': 'HW_refts_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1593336984124'}, {'domain': '.id1.cloud.huawei.com', 'httpOnly': True, 'name': 'CAS_THEME_NAME', 'path': '/', 'secure': True, 'value': 'red'}, {'domain': 'id1.cloud.huawei.com', 'httpOnly': False, 'name': 'cookieBannerOnOff', 'path': '/', 'secure': False, 'value': 'true'}, {'domain': '.id1.cloud.huawei.com', 'httpOnly': True, 'name': 'VERSION_NO', 'path': '/', 'secure': True, 'value': 'UP_CAS_4.0.4.100'}, {'domain': 'id1.cloud.huawei.com', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/CAS', 'secure': True, 'value': '144E8B2ED3F5D9C8576742C1DDF4CF3D0DCF6949E13D6943'}]")
        self.urlold = self.driver.current_url
        item = self.driver.find_element(
            By.XPATH, "//input[@ht='input_pwdlogin_account']")
        item.send_keys(user)

        item = self.driver.find_element(By.XPATH, "//input[@ht='input_pwdlogin_pwd']")
        item.send_keys(password)

        item = self.driver.find_element(
            By.XPATH, "//div[@ht='click_pwdlogin_submitLogin']")
        item.click()
        time.sleep(1)


        
        while True:
            time.sleep(1)
            self.urlnew = self.driver.current_url
            if self.urlnew != self.urlold:
                break
            print("waiting for login self.urlnew=",self.urlnew)

        return

#  F:\sourcecode\unity\aso_web
#  https://www.qimai.cn/trend/keywordExtend/keyword/%E6%B1%89%E5%AD%97
    def GetKeyWord(self, word):
        url = "https://www.qimai.cn/trend/keywordExtend/keyword/"+word  
        print(url)
        self.driver.get(url)
        webcmd = WebDriverCmd(self.driver)

        key = "//a[@class='search-word']"
        list = webcmd.FindList(key,True)
        aso = ""
        idx =0
        for a in list:
            text = a.text
            # print(text)
            if len(aso)<100:
                if idx==0:
                    aso=text
                else:
                    aso+=","+text

            idx+=1
        
        print(aso)
        return aso

    def GetLocalHtmlKeyWord(self, isHD):
        # url = "https://www.qimai.cn/trend/keywordExtend/keyword/"+word 
        url = "file:///F:/sourcecode/unity/aso_web/app.html"
        if isHD:
            url = "file:///F:/sourcecode/unity/aso_web/app_hd.html"
        print(url)
        self.driver.get(url)
        webcmd = WebDriverCmd(self.driver)

        key = "//a[@class='search-word']"
        list = webcmd.FindList(key,True)
        aso = ""
        idx =0
        for a in list:
            text = a.text
            # print(text)
            if len(aso+","+text)<100:
                if idx==0:
                    aso=text
                else:
                    aso+=","+text

            idx+=1
        
        print(aso)
        return aso

    def GetAso(self, isHD):  
        applans = [Source.LANGUAGE_CN,Source.LANGUAGE_EN]
        for lan in applans:    
            name = mainAppInfo.GetAppName(Source.IOS, isHD,lan) 
            # self.GetKeyWord(name)
            aso = self.GetKeyWord(name)
            mainAppInfo.SetAso(isHD,Source.APPSTORE,lan,aso)

    def Run(self, isHD):     
        self.Init()
        self.GoHome(isHD)
        # self.Login("chyfemail163@163.com", "Qianlizhiwai1")

        self.GetAso(False)
        self.GetAso(True)
        
        print("AsoQimai sucess")


mainAsoQimai = AsoQimai()