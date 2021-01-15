# 导入selenium的浏览器驱动接口 

import sys
import os
import json
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径

  
import sqlite3
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver

# 当前工作目录 Common/PythonUnity/ProjectConfig/Script
sys.path.append('../../') 
sys.path.append('./') 
from Project.Resource import mainResource
from Common import Source
from Common.File.FileUtil import FileUtil
from Common.File.FileBrowser import FileBrowser
from Common.File.JsonUtil import JsonUtil 

JsonUtil
from AppInfo.AppInfo import mainAppInfo

# 要想调用键盘按键操作需要引入keys包

# 导入chrome选项


# pip3 install pywin32

# sys.path.append('../common')


class AppStoreBase():
    driver: None 
    urlCreatePlaceId: None
    osApp: None
    urlold:None
    urlnew:None
    # rootDirProjectOutPut="F:\\sourcecode\\unity\\product\\kidsgame\\ProjectOutPut"
 
   
    def GetSmsCode(self):
        code = ""
        while True:
            time.sleep(2)
            code = mainAppInfo.GetSmsCode()
            if len(code) != 0:
                break
            print("waiting for GetSmsCode")
        return code
        
    def GoHome(self):
        # 加载百度页面
        # driver.get("https://developer.huawei.com/consumer/cn/")
        self.driver.get("https://adnet.qq.com/index")
        # time.sleep(5)

        # self.saveString2File(self.driver.page_source,"1.html")
        #   # 点击登录按钮
        # self.driver.find_element_by_id('switcher_plogin').click()
        # time.sleep(1)
 
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

    def Quit(self,delay):
        time.sleep(delay) 
        self.driver.quit()
        time.sleep(1)
 
    

    # 让元素在可见范围 可以点击操作
    def SetItemVisible(self,item,delay=1):
        ActionChains(self.driver).move_to_element(item).perform()
        time.sleep(delay)

    
#   该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false        
    def IsElementExist(self,element):
        flag=True
        browser=self.driver
        try:
            # browser.find_element_by_css_selector(element)
            browser.find_element(By.XPATH, element)
            return flag 
        except:
            flag=False
            return flag

    def GetAppName(self, ishd,lan):
        name = mainAppInfo.GetAppName(Source.ANDROID, ishd,lan) 
        return name

    def GetAppPromotion(self, ishd,lan):
        name = mainAppInfo.GetAppPromotion(ishd,lan) 
        return name
        

    def GetAppDetail(self, ishd,lan):
        name = mainAppInfo.GetAppDetail(ishd,lan)  
        return name

    def OpenFileBrowser(self,path,autoclick):
        FileBrowser.OpenFile(path,autoclick)
         
    def LoginQQ(self,user,password):
        # 3452644866 
        print("waiting for login")
        # self.AddCookie()
        time.sleep(2)

        # return
        # driver.add_cookie("[{'domain': '.id1.cloud.huawei.com', 'expiry': 1908869785, 'httpOnly': False, 'name': 'sid', 'path': '/', 'secure': True, 'value': '2049382e3828ef4470bef8b426c4bb3370e7d9e1147f53a18839e47dad7caf10a233e61ee15337b4373e'}, {'domain': '.id1.cloud.huawei.com', 'expiry': 1908869785, 'httpOnly': False, 'name': 'hwid_cas_sid', 'path': '/', 'secure': True, 'value': '2049382e3828ef4470bef8b426c4bb3370e7d9e1147f53a18839e47dad7caf10a233e61ee15337b4373e'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_idts_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1593336984125'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_id_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': 'cf787be41ac24d65887dcd20c826ac97'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_idvc_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1593338788, 'httpOnly': False, 'name': 'HW_idn_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': 'ec569450f0ac4cd78fc72965d91ec7e8'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1608888984, 'httpOnly': False, 'name': 'HW_refts_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1593336984124'}, {'domain': '.id1.cloud.huawei.com', 'httpOnly': True, 'name': 'CAS_THEME_NAME', 'path': '/', 'secure': True, 'value': 'red'}, {'domain': 'id1.cloud.huawei.com', 'httpOnly': False, 'name': 'cookieBannerOnOff', 'path': '/', 'secure': False, 'value': 'true'}, {'domain': '.id1.cloud.huawei.com', 'httpOnly': True, 'name': 'VERSION_NO', 'path': '/', 'secure': True, 'value': 'UP_CAS_4.0.4.100'}, {'domain': 'id1.cloud.huawei.com', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/CAS', 'secure': True, 'value': '144E8B2ED3F5D9C8576742C1DDF4CF3D0DCF6949E13D6943'}]")
        self.driver.switch_to.frame("ptlogin_iframe")
        time.sleep(2)

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
 

 #获取cookies保存到文件
    def SaveCookie(self,filePath):
        cookies=self.driver.get_cookies()  
        JsonUtil.SaveJson(filePath,cookies)
        # with open('e:/cookies/cookies_taptap.json','w') as f:
        #     f.write(json_cookies)
    #读取文件中的cookie
    def AddCookie(self,filepath):
        flag = os.path.exists(filepath)
        if flag ==False:
            return
        self.driver.delete_all_cookies()
        strfile = FileUtil.GetFileString(filepath) 
        list_cookies=json.loads(strfile)
        # cookies=self.getPureDomainCookies(list_cookies)
        for i in list_cookies:
            self.driver.add_cookie(i)
                
    def getPureDomainCookies(self,cookies):
        domain2cookie={}  #做一个域到cookie的映射
        for cookie in cookies:
            domain=cookie['domain']
            if domain in domain2cookie:
                domain2cookie[domain]=[]
            else:
                domain2cookie[domain].append(cookie)
                
        maxCnt=0
        ansDomain=''
        for domain in domain2cookie.keys():
            cnt=len(domain2cookie[domain])
            if cnt > maxCnt:
                maxCnt=cnt
                ansDomain=domain
        ansCookies=domain2cookie[ansDomain]
        return ansCookies

 