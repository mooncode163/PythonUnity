# 导入selenium的浏览器驱动接口
import sys
import os
import json
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
from AppStore.AppStoreBase import AppStoreBase
sys.path.append('../../') 
sys.path.append('./') 

from Common.WebDriver.WebDriverCmd import CmdType
from Common.WebDriver.WebDriverCmd import WebDriverCmd 
from Common.WebDriver.WebDriverCmd import CmdInfo 

import pyperclip

from Project.Resource import mainResource
from Common import Source 
from Common.File.FileUtil import FileUtil 
from Common.File.FileBrowser import FileBrowser
from AppInfo.AppInfo import mainAppInfo
from AppStore.Huawei.HuaweiAppGalleryApi import mainHuaweiAppGalleryApi
from AppStore.AppStoreAcount import mainAppStoreAcount

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import sqlite3 



# 要想调用键盘按键操作需要引入keys包

# 导入chrome选项


# pip3 install pywin32

# sys.path.append('../common')


class AppStoreHuawei(AppStoreBase):

    defaultLanguage = "美式英语"
    fileCookie = "e:/cookies/cookies_huawei.json" 

    listCountry = ["zh-CN","en-US", "en-GB"]  
    listCountryLanguage = ["cn","en", "en"] 

    # listCountry = ["en-AU","en-GB"]  
    # listCountryLanguage = ["en","en"] 
    listDisplay = ["APP_PHONE"]  
    listDisplayName = ["1080p"] 

    def GoHome(self, isHD):
        # self.AddCookie(self.fileCookie)
        appid = mainAppInfo.GetAppId(isHD, Source.HUAWEI)
        url = "https://developer.huawei.com/consumer/cn/service/josp/agc/index.html#/myApp"
        print(url)
        self.driver.get(url)
        self.urlold = self.driver.current_url
        time.sleep(3)


    def Login(self, user, password):
        # 3452644866
        mainAppInfo.SetSmsCode("")
        # 等待扫码登录
        # while True:
        #     time.sleep(1)
        #     self.urlnew = self.driver.current_url
        #     if self.urlnew != self.urlold:
        #         break
        #     print("waiting for login self.urlnew=",self.urlnew)

        # return

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


        code = self.GetSmsCode()
        print("Login GetSmsCode=",code)

        # 输入短信验证码
        item = self.driver.find_element(
            By.XPATH, "//input[@ht='input_authentication_authcode']")
        item.send_keys(code)
        

        while True:
            time.sleep(1)
            self.urlnew = self.driver.current_url
            if self.urlnew != self.urlold:
                break
            print("waiting for login self.urlnew=",self.urlnew)

        return

        # cookie = self.driver.get_cookies()
        # print(cookie)
        # [{'domain': '.id1.cloud.huawei.com', 'expiry': 1908869785, 'httpOnly': False, 'name': 'sid', 'path': '/', 'secure': True, 'value': '2049382e3828ef4470bef8b426c4bb3370e7d9e1147f53a18839e47dad7caf10a233e61ee15337b4373e'}, {'domain': '.id1.cloud.huawei.com', 'expiry': 1908869785, 'httpOnly': False, 'name': 'hwid_cas_sid', 'path': '/', 'secure': True, 'value': '2049382e3828ef4470bef8b426c4bb3370e7d9e1147f53a18839e47dad7caf10a233e61ee15337b4373e'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_idts_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1593336984125'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_id_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': 'cf787be41ac24d65887dcd20c826ac97'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_idvc_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1593338788, 'httpOnly': False, 'name': 'HW_idn_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': 'ec569450f0ac4cd78fc72965d91ec7e8'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1608888984, 'httpOnly': False, 'name': 'HW_refts_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1593336984124'}, {'domain': '.id1.cloud.huawei.com', 'httpOnly': True, 'name': 'CAS_THEME_NAME', 'path': '/', 'secure': True, 'value': 'red'}, {'domain': 'id1.cloud.huawei.com', 'httpOnly': False, 'name': 'cookieBannerOnOff', 'path': '/', 'secure': False, 'value': 'true'}, {'domain': '.id1.cloud.huawei.com', 'httpOnly': True, 'name': 'VERSION_NO', 'path': '/', 'secure': True, 'value': 'UP_CAS_4.0.4.100'}, {'domain': 'id1.cloud.huawei.com', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/CAS', 'secure': True, 'value': '144E8B2ED3F5D9C8576742C1DDF4CF3D0DCF6949E13D6943'}]


# 3452644866 qq31415926


    def CreateApp(self, isHD):
        appid = mainAppInfo.GetAppId(isHD, Source.HUAWEI)
        print("CreateApp appid=",appid," isHD=",isHD)
        if appid != "0":
            self.UpdateAppInfo(isHD)
            self.UploadScreenShot(isHD)
            self.UpdateApkApi(isHD)
            return
            
        # self.Init()
        # self.GoHome(isHD)
        # self.Login("chyfemail163@163.com", "Qianlizhiwai1")
        # self.SaveCookie(self.fileCookie)

        webcmd = WebDriverCmd(self.driver)
        old_window = self.driver.current_window_handle
        url = "https://developer.huawei.com/consumer/cn/service/josp/agc/index.html#/myApp"
        self.driver.get(url)
        time.sleep(1)

        # 等待网页加载成功
        key = "//iframe[@id='mainIframeView']"
        while True:
            time.sleep(1)
            print("web is loading...")
            if self.IsElementExist(key) == True:
                print("web loading finish")
                break

        # 跳转到新的页面
        print("self.driver.current_url=", self.driver.current_url)
        # self.driver.switch_to.window(self.driver.window_handles[0])
        for win in self.driver.window_handles:
            if win != old_window:
                self.driver.switch_to.window(win)
        time.sleep(1)
        print("self.driver.current_url 2=", self.driver.current_url)

        # self.driver.switch_to.frame("mainIframeView")
        # time.sleep(1)
        self.Switch2MainFrameView()

        webcmd.AddCmdWait(CmdType.CLICK, "//a[@id='MyAppListNewApp']")
        webcmd.Run(True)

        title = self.GetAppName(isHD, Source.LANGUAGE_CN)
        webcmd.AddCmd(
            CmdType.INPUT, "//input[@ng-model='Model.productAndApp.appName']", title, 1)
        webcmd.Run(True)

        key = "//span[contains(text(),'请选择应用分类')]"
        webcmd.AddCmd(CmdType.CLICK, key)
        # <div class="ucd-droplist-option ng-binding ng-scope" ng-bind="parentType.value">应用</div>
        key = "//div[@class='ucd-droplist-option ng-binding ng-scope' and contains(text(),'应用')]"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)

        key = "//span[contains(text(),'请选择语言')]"
        webcmd.AddCmd(CmdType.CLICK, key)
        key = "//div[@class='ucd-droplist-option ng-binding ng-scope' and contains(text(),'" + \
            self.defaultLanguage+"')]"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)

        old_window = self.driver.current_window_handle
        # waiting 确定
        print("waiting 确定 手动点击 ")
        while True:
            time.sleep(1)
            if self.IsElementExist("//a[@id='PubProDetermine']") == False:
                break

        print("self.driver.current_url=", self.driver.current_url)
        # self.driver.switch_to.window(self.driver.window_handles[0])
        for win in self.driver.window_handles:
            if win != old_window:
                self.driver.switch_to.window(win)
        time.sleep(1)

        # self.driver.switch_to.frame("mainIframeView")
        self.Switch2MainFrameView()
 
        item = webcmd.Find("//span[@id='AppInfoAppIdContent']",True) 
        appid = item.text
        print(appid)
        mainAppInfo.SetAppId(isHD, Source.ANDROID, Source.HUAWEI, appid)

        # self.FillAppInfo(isHD)



    def AddLanguage(self, webcmd, title):
        item = webcmd.AddCmdWait(
            CmdType.CLICK, "//a[@id='AppInfoManageLanguageButton']")
        # self.SetItemVisible(item)
        webcmd.Run(True)

        webcmd.AddCmd(
            CmdType.INPUT, "//input[@ng-model='searchTxt']", title, 2)
        webcmd.Run(True)

        key = "//span[@title='"+title+"']"
        print(key)
        if self.IsElementExist(key):
            # webcmd.AddCmd2(CmdType.CLICK, key)
            webcmd.AddCmd2(
                CmdType.CLICK, "//label[@class='checkbox lang-item ng-scope']")
        else:
            print(key, "is not exit")

        # webcmd.AddCmd2(CmdType.CLICK, "//label[@class='checkbox lang-item ng-scope']")
        webcmd.Run(True)

        item = webcmd.AddCmd2(
            CmdType.CLICK, "//a[@class='btn btn-primary btn-small ng-binding']")
        # self.SetItemVisible(item)
        webcmd.Run(True)
        time.sleep(2)

    def FillLanguage(self, webcmd, isHD, lanName, lanKey):

        # 选择语言
        # webcmd.AddCmd(CmdType.CLICK, "//input[@type='search' and @aria-owns='ui-select-choices-3']", "", 1)
        item = webcmd.AddCmd(
            CmdType.CLICK, "//span[@class='ui-select-match-text pull-left']", "", 2)
        self.SetItemVisible(item)
        webcmd.Run(True)

        # 简体中文-默认
        if lanName == self.defaultLanguage:
            lanName = lanName+"-默认"

        key = "//div[@class='ucd-droplist-option ng-binding' and text()='" + \
            lanName+"']"
        # key = "//div[@class='ucd-droplist-option ng-binding' and text()='"+lanName+"-默认"+"']"
        # if self.IsElementExist(key)==False:
        #     key = "//div[@class='ucd-droplist-option ng-binding' and text()='"+lanName+"']"

        # 模糊匹配
        # key = "//div[@class='ucd-droplist-option ng-binding' and contains(text(),'"+lanName+"')]"

        item = webcmd.AddCmd(CmdType.CLICK, key, "", 1)
        if item == None:
            print(key)
        else:
            self.SetItemVisible(item)

        webcmd.Run(True)

        title = self.GetAppName(isHD, lanKey)
        print(title)
        pyperclip.copy(title)
        key = "//input[@id='AppInfoAppNameInputBox']"
        webcmd.AddCmd2(CmdType.INPUT_CLEAR, key)
        # webcmd.AddCmd(CmdType.ENTER, "//input[@id='AppInfoAppNameInputBox']",title,1)
        pyperclip.paste()

        webcmd.AddCmd2(CmdType.CTR_V, key)
        webcmd.Run(True)

        title = self.GetAppDetail(isHD, lanKey)
        pyperclip.copy(title)
        key = "//textarea[@id='AppInfoAppIntroduceInputBox']"
        # webcmd.AddCmd(CmdType.CLICK, key,title,1)
        pyperclip.paste()
        webcmd.AddCmd2(CmdType.INPUT_CLEAR, key)
        webcmd.AddCmd2(CmdType.CTR_V, key)
        # webcmd.AddCmd(CmdType.INPUT, "//textarea[@id='AppInfoAppIntroduceInputBox']",title,2)
        webcmd.Run(True)
        time.sleep(2)

        title = self.GetAppPromotion(isHD, lanKey)
        print(title)
        pyperclip.copy(title)
        key = "//input[@id='AppInfoAppBriefInputBox']"
        item = self.driver.find_element(By.XPATH, key)

        ActionChains(self.driver).move_to_element(item).perform()
        time.sleep(1)
        # webcmd.AddCmd(CmdType.ENTER, "//input[@id='AppInfoAppBriefInputBox']",title,1)
        pyperclip.paste()
        # webcmd.AddCmd2(CmdType.INPUT_CLEAR, key)
        webcmd.AddCmd2(CmdType.CLICK, key)
        webcmd.AddCmd2(CmdType.INPUT_CLEAR, key)
        # 必须enter选中
        webcmd.AddCmd2(CmdType.ENTER, key)
        webcmd.AddCmd2(CmdType.CTR_V, key)
        webcmd.Run(True)
        time.sleep(2)

        # icon
        key = "//img[@id='AppInfoAppIconAddButton']"
        item = self.driver.find_element(By.XPATH, key)
        ActionChains(self.driver).move_to_element(item).perform()
        time.sleep(2)
        # webcmd.AddCmd2(CmdType.ENTER, key)
        # webcmd.AddCmd(CmdType.CLICK, key, "", 2)
        item.click()

        icon = mainResource.GetOutPutIconPathWin32(mainResource.GetProjectOutPut(
        ), Source.TAPTAP, isHD)+"\\huawei\\icon_android_216.png"
        print(icon)
        # webcmd.Run(True)
        time.sleep(2)
        self.OpenFileBrowser(icon, True)
        time.sleep(2)


#    <span class="text ng-binding">横向截图</span>
        idx_start = 6
        strkey = "竖向截图"
        if isHD:
            idx_start = 1
            strkey = "横向截图"

        key = "//span[@class='text ng-binding' and text()='"+strkey+"']"
        item = webcmd.AddCmd(CmdType.CLICK, key)
        self.SetItemVisible(item)
        webcmd.Run(True)

        for i in range(0, 5):
            key = "//img[@id='AppIntroScreenshot"+str(i+idx_start)+"']"
            item = self.driver.find_element(By.XPATH, key)

            if i >= 2:
                # 将 滚动条 底部对齐
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(false);", item)
                time.sleep(2)
            # 鼠标悬停
            ActionChains(self.driver).move_to_element(item).perform()
            time.sleep(2)
            # webcmd.AddCmd(CmdType.CLICK, key, "", 2)
            item.click()
            time.sleep(2)
            # webcmd.AddCmd2(CmdType.ENTER, key)
            pic = mainResource.GetOutPutScreenshotPathWin32(mainResource.GetProjectOutPut(
            ), Source.TAPTAP, isHD) + "\\"+lanKey+"\\1080p\\"+str(i+1)+".jpg"
            print(pic)
            # webcmd.Run(True)
            self.OpenFileBrowser(pic, True)
            time.sleep(2)

    def Switch2MainFrameView(self):
        webcmd = WebDriverCmd(self.driver)
        # 等待网页加载成功
        key = "//iframe[@id='mainIframeView']"
        while True:
            time.sleep(1)
            print("web is Switch2MainFrameView...")
            if self.IsElementExist(key) == True:
                print("web Switch2MainFrameView finish")
                break

        self.driver.switch_to.frame("mainIframeView")
        time.sleep(2)

    def FillAppInfo(self, isHD):
        webcmd = WebDriverCmd(self.driver)
        old_window = self.driver.current_window_handle
        appid = mainAppInfo.GetAppId(isHD, Source.HUAWEI)
        url = "https://developer.huawei.com/consumer/cn/service/josp/agc/index.html#/myApp/"+appid
        print(url)
        self.driver.get(url)
        time.sleep(3)

       # 跳转到新的页面
        print("self.driver.current_url=", self.driver.current_url)
        # self.driver.switch_to.window(self.driver.window_handles[0])
        for win in self.driver.window_handles:
            if win != old_window:
                self.driver.switch_to.window(win)
        time.sleep(1)
        print("self.driver.current_url 2=", self.driver.current_url)

        # 等待网页加载成功
        # key = "//iframe[@id='mainIframeView']"
        # while True:
        #     time.sleep(1)
        #     print("web is loading...")
        #     if self.IsElementExist(key) == True:
        #         print("web loading finish")
        #         break

        # self.driver.switch_to.frame("mainIframeView")
        # time.sleep(2)
        self.Switch2MainFrameView()

        # 填写语言资料
        lanKeys = ("简体中文", "英式英语", "美式英语")
        applans = (Source.LANGUAGE_CN, Source.LANGUAGE_EN, Source.LANGUAGE_EN)

        # 添加语言
        for lan in range(0, len(lanKeys)):
            self.AddLanguage(webcmd, lanKeys[lan])

        # 填写语言
        for lan in range(0, len(lanKeys)):
            self.FillLanguage(webcmd, isHD, lanKeys[lan], applans[lan])

        # 滚动到浏览器顶部
        js_top = "var q=document.documentElement.scrollTop=0"
        # 滚动到浏览器底部
        js_bottom = "var q=document.documentElement.scrollTop=document.documentElement.scrollHeight"
        self.driver.execute_script(js_bottom)
        time.sleep(2)

        # 应用分类
        isSort = True
        # 请选择二级分类
        key = "//span[contains(text(),'请选择二级分类')]"
        isSort = self.IsElementExist(key)
        if isSort == False:
            print("not find key="+key)
            isSort = False
            # return

        if isSort:
            item = webcmd.AddCmd(CmdType.CLICK, key)
            self.SetItemVisible(item)
            webcmd.Run(True)

            # <div class="ucd-droplist-option ng-binding">教育</div>
            key = "//div[@class='ucd-droplist-option ng-binding' and contains(text(),'教育')]"
            item = webcmd.AddCmd(CmdType.CLICK, key)
            self.SetItemVisible(item)
            webcmd.Run(True)

            key = "//span[contains(text(),'请选择三级分类')]"
            webcmd.AddCmd(CmdType.CLICK, key)
            webcmd.Run(True)

            # <div class="ucd-droplist-option ng-binding">学习</div>
            key = "//div[@class='ucd-droplist-option ng-binding' and contains(text(),'学习')]"
            item = webcmd.AddCmd(CmdType.CLICK, key)
            self.SetItemVisible(item)
            webcmd.Run(True)

        key = "//input[@id='AppInfoCustomerEmailInputBox']"
        item = webcmd.AddCmd(CmdType.INPUT, key, "chyfemail163@163.com")
        self.SetItemVisible(item)
        webcmd.Run(True)

        # 保存
        key = "//a[@id='AppInfoSaveButtonCn']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)

        time.sleep(3)

        # 确定
        key = "//a[@id='CommonConfirmButtonOk']"
        if self.IsElementExist(key):
            webcmd.AddCmd(CmdType.CLICK, key)
            webcmd.Run(True)
            self.PreSubmitApp(isHD)
        else:
            self.PreSubmitApp(isHD)

    # 准备提交app

    def PreSubmitApp(self, isHD):

        appid = mainAppInfo.GetAppId(isHD, Source.HUAWEI)
        url = "https://developer.huawei.com/consumer/cn/service/josp/agc/index.html#/myApp/"+appid
        print(url)
        self.driver.get(url)
        time.sleep(3)
        old_window = self.driver.current_window_handle

        webcmd = WebDriverCmd(self.driver)
        # 准备提交
        key = "//span[@class='yellow-circle']"
        webcmd.AddCmdWait(CmdType.CLICK, key)
        webcmd.Run(True)

       # 跳转到新的页面
        print("self.driver.current_url=", self.driver.current_url)
        # self.driver.switch_to.window(self.driver.window_handles[0])
        for win in self.driver.window_handles:
            if win != old_window:
                self.driver.switch_to.window(win)
        time.sleep(1)
        print("self.driver.current_url 2=", self.driver.current_url)

        # 等待网页加载成功
        # key = "//iframe[@id='mainIframeView']"
        # while True:
        #     time.sleep(1)
        #     print("web is loading...")
        #     if self.IsElementExist(key) == True:
        #         print("web loading finish")
        #         break

        # self.driver.switch_to.frame("mainIframeView")
        # time.sleep(3)
        self.Switch2MainFrameView()

        # # 管理国家
        # key = "//a[@id='VerInfoManageCountryButton']"
        # webcmd.AddCmd(CmdType.CLICK, key)
        # webcmd.Run(True)

        # # 全球
        # key = "//span[@id='CountryCheckMarkGlobal']"
        # webcmd.AddCmd(CmdType.CLICK, key)
        # webcmd.Run(True)

        # self.UpdateApk(isHD)

        # 分级
        # key = "//a[@class='agc-button-primary agc-button-normal version-info-rate ml-0 ng-binding' and contains(text(),'分级')]"
        key = "//a[contains(text(),'分级')]"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)
        time.sleep(3)

        # 分级勾选
        key = "//div[@class='rate-dialog-content']"
        # div =  self.driver.find_element(By.XPATH, key)
        key = "//label[@class='radio rate-dialog-huaweiRating']"
        webcmd.AddCmd(CmdType.CLICK, key)

        # 分级确认
        key = "//a[@id='submit']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)

        # copyright
        key = "//img[@id='AppInfoUploadCertificateURLs1']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)
        apk = mainResource.GetOutPutCopyRightPathWin32(
            mainResource.GetProjectOutPut(), isHD)+"\\huawei.png"
        print(apk)
        flag = os.path.exists(apk)
        if flag:
            self.OpenFileBrowser(apk, True)
            time.sleep(2)

        # 隐私政策网址
        key = "//input[@id='VerInfoPrivacyPolicyInputBox']"
        webcmd.AddCmd(CmdType.INPUT, key, mainAppInfo.GetAppPrivacyUrl(isHD))
        webcmd.Run(True)

        # <span class="text ng-binding">审核通过立即上架</span>
        key = "//span[@class='text ng-binding' and contains(text(),'审核通过立即上架')]"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)

        # 保存
        key = "//a[@id='VerInfoSaveButton']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)
        time.sleep(2)

        # 确定 保存
        # <a class="btn btn-primary btn-small ng-binding" data-dismiss="dialog" ng-click="callback()">确定</a>
        key = "//a[@class='btn btn-primary btn-small ng-binding' and contains(text(),'确定')]"
        if self.IsElementExist(key):
            webcmd.AddCmd(CmdType.CLICK, key)
            webcmd.Run(True)
            self.UpdateApk(isHD)
            self.SubmitApp(isHD)

    def SearchApp(self, ishd):
        name = self.GetAppName(isHD, Source.LANGUAGE_CN)
        item = self.driver.find_element(
            By.XPATH, "//input[@ng-model='Model.product.query.appName']")
        item.send_keys(name)
        time.sleep(1)

        # search
        self.driver.find_element_by_id('search_medium_id').click()
        time.sleep(2)

    def SubmitApp(self, isHD):
        webcmd = WebDriverCmd(self.driver)
        # 隐私政策网址
        key = "//input[@id='VerInfoPrivacyPolicyInputBox']"
        if self.IsElementExist(key):
            webcmd.AddCmd(CmdType.INPUT, key, mainAppInfo.GetAppPrivacyUrl(isHD))
            webcmd.Run(True)

        # 不申请
        key = "//span[@id='VerInfoNotApplyButton']"
        if self.IsElementExist(key):
            webcmd.AddCmd(CmdType.CLICK_Action, key)
            webcmd.Run(True)

        # item = self.driver.find_element(By.XPATH, "//span[@id='VerInfoNotApplyButton']")
        # item.click()
        # time.sleep(1)

        # 提交审核
        key = "//a[@id='VerInfoSubmitButton']"
        if self.IsElementExist(key):
            webcmd.AddCmd(CmdType.CLICK_Action, key)
            webcmd.Run(True)
        time.sleep(3)

        # 确定
        key = "//a[@id='AppSubmitConfirmButtonOk']"
        if self.IsElementExist(key):
            webcmd.AddCmd(CmdType.CLICK_Action, key)
            webcmd.Run(True)

        time.sleep(3)

    def UpdateApk(self, isHD):
        webcmd = WebDriverCmd(self.driver)

        # 滚动到浏览器顶部
        js_top = "var q=document.documentElement.scrollTop=0"
        # 滚动到浏览器底部
        js_bottom = "var q=document.documentElement.scrollTop=document.documentElement.scrollHeight"
        self.driver.execute_script(js_top)
        time.sleep(2)

        # key = "//iframe[@id='mainIframeView']"
        # if self.IsElementExist(key)==True:
        #     self.driver.switch_to.frame("mainIframeView")
        # time.sleep(1)

        # 软件包管理
        # time.sleep(1)
        # info = CmdInfo()
        # info.type = CmdType.CLICK_SCRIPT
        # info.cmd = "//a[@id='VerInfoDownloadLink']"
        # info.value = ""
        # info.delay = 1
        # info.isWaiting = True
        # item = webcmd.AddCmdInfo(info)
        # self.SetItemVisible(item)
        key = "//a[@id='VerInfoDownloadLink']" 
        item = webcmd.Find(key,True)
        self.SetItemVisible(item)

        webcmd.AddCmdWait(CmdType.CLICK_Action, key)
        webcmd.Run(True)

        webcmd.AddCmd(CmdType.CLICK_SCRIPT,
                      "//a[@id='ManageAppUploadPackageButton']")
        webcmd.Run(True)

        # <a class="agc-button-primary agc-button-normal ng-binding" ng-click="uploadPkg()" ng-show="!notAllowedUploadPkg" target="_blank">上传</a>
        # 第一次上传
        key = "//a[@ng-show='!notAllowedUploadPkg' and contains(text(),'上传')]"
        if self.IsElementExist(key):
            webcmd.AddCmd(CmdType.CLICK_SCRIPT, key)
            webcmd.Run(True)

        webcmd.AddCmd(CmdType.CLICK_Action,
                      "//div[@id='uploaderSelectContainer']")
        webcmd.Run(True)

        time.sleep(2)
        apk = mainResource.GetOutPutApkPathWin32(
            mainResource.GetProjectOutPut(), Source.HUAWEI, isHD)
        print(apk)
        self.OpenFileBrowser(apk, True)
        time.sleep(1)

        # <div class="uploader-progress-bar" ng-style="{width: uploadProgress}"></div>

        # # <div class="progress"><div class="progress-bar" style="width: 82%;" aria-valuenow="82"></div></div>
        # 等待上传完成
        isUploading = False
        while True:
            time.sleep(1)
            key = "//div[@class='uploader-progress-bar']"
            if self.IsElementExist(key):
                item = self.driver.find_element(By.XPATH, key)
                if item is not None:
                    style = item.get_attribute('style')
                    isUploading = True
                    print(style)
                    # if style.find("100") >=0:
                    #     time.sleep(1)
                    #     print("upload apk finish")
                    #     break
            else:
                if isUploading == True:
                    isUploading = False
                    time.sleep(1)
                    print("upload apk finish")
                    break

        time.sleep(1)

        # 不申请
        # webcmd.AddCmd(CmdType.CLICK, "//span[@id='VerInfoNotApplyButton']")
        # webcmd.Run(True)

        # 提交审核
        # webcmd.AddCmd(CmdType.CLICK, "//a[@id='VerInfoSubmitButton']")
        # webcmd.Run(True)
        # time.sleep(3)

        # 确定
        # webcmd.AddCmd(CmdType.CLICK, "//a[@id='AppSubmitConfirmButtonOk']")
        # webcmd.Run(True)
        # time.sleep(3)

    def UpdateApp(self, isHD):
        # self.UpdateAppOld(isHD)
        # return
        old_window = self.driver.current_window_handle
        webcmd = WebDriverCmd(self.driver)
        # 打开新标签
        # self.driver.find_element_by_xpath('//body').send_keys(Keys.CONTROL,"t")
        # js = "window.open('')"
        # self.driver.execute_script(js)
        # time.sleep(2)

        appid = mainAppInfo.GetAppId(isHD, Source.HUAWEI)
        # https://developer.huawei.com/consumer/cn/service/josp/agc/index.html#/myApp/101054959
        url = "https://developer.huawei.com/consumer/cn/service/josp/agc/index.html#/myApp/"+appid
        self.driver.get(url)
        time.sleep(1)
        # 等待网页加载成功
        # key = "//iframe[@id='mainIframeView']"
        # while True:
        #     time.sleep(1)
        #     print("web is loading...")
        #     if self.IsElementExist(key) == True:
        #         print("web loading finish")
        #         break
 

        # self.driver.switch_to.frame("mainIframeView")
        # time.sleep(3)
        self.Switch2MainFrameView()

         
        key = "//span[@title='版本信息']"
        if self.IsElementExist(key) == False:
            print("find 版本信息 fail key=",key)
            self.UpdateApp(isHD)
            

        key = "//span[@class='green-circle']" 
        # red-circle
        if self.IsElementExist(key) == False:
            print("key fail key=",key)
            # 待修改
            key = "//span[@class='red-circle']"
            if self.IsElementExist(key) == False: 
                key = "//span[@class='yellow-circle']"
                # 第一次上传apk
                # self.PreSubmitApp(isHD)
                # return
                if self.IsElementExist(key) == False:
                    print("key fail key2=",key)
                    print("self.driver.current_url fail=", self.driver.current_url)
                    # print(self.driver.page_source) 
                    mainResource.saveString2File(self.driver.page_source,"1.html")

        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True) 
        time.sleep(5)

        # 跳转到新的页面
        print("self.driver.current_url=", self.driver.current_url)
        # self.driver.switch_to.window(self.driver.window_handles[0])
        for win in self.driver.window_handles:
            if win != old_window:
                self.driver.switch_to.window(win)
        time.sleep(3)
        print("self.driver.current_url 2=", self.driver.current_url)

        # self.driver.switch_to.frame("mainIframeView")
        self.Switch2MainFrameView()

        old_window = self.driver.current_window_handle
        # 升级按钮
        key = "//a[@id='VersionUpgradeButton']"
        if self.IsElementExist(key):
            webcmd.AddCmd(CmdType.CLICK_Action, key)
            webcmd.Run(True) 
            time.sleep(2)

        # 跳转到新的页面
        print("self.driver.current_url=", self.driver.current_url)
        # self.driver.switch_to.window(self.driver.window_handles[0])
        for win in self.driver.window_handles:
            if win != old_window:
                self.driver.switch_to.window(win)
        time.sleep(3)
        print("self.driver.current_url 2=", self.driver.current_url)

        # self.driver.switch_to.frame("mainIframeView")
        # time.sleep(3)
        self.Switch2MainFrameView()

        self.UpdateApk(isHD)
        time.sleep(1)
        self.SubmitApp(isHD)
 
    def SearchApp(self, ishd):
        name = self.GetAppName(isHD, Source.LANGUAGE_CN)
        self.driver.get("https://adnet.qq.com/medium/list")
        time.sleep(2)
        item = self.driver.find_element(
            By.XPATH, "//input[@class='form-control']")
        time.sleep(1)

        item.send_keys(name)
        # item.send_keys("儿童写汉字")

        time.sleep(1)

        # search
        self.driver.find_element_by_id('search_medium_id').click()
        time.sleep(2)

        # 筛选
        item = self.driver.find_element(
            By.XPATH, "//button[@class='btn filter-operate']")
        # item = self.driver.find_element(By.XPATH, "//div[@class='filter-parent-control']")

        # error
        # item.click()
        self.driver.execute_script("arguments[0].click();", item)
        time.sleep(2)

# <input type="checkbox" class="check" name="" value="IOS">
        if self.osApp == Source.ANDROID:
            item = self.driver.find_element(
                By.XPATH, "//input[@value='Android']")
            # item.click()
            self.driver.execute_script("arguments[0].click();", item)
            time.sleep(1)

        if self.osApp == Source.IOS:
            item = self.driver.find_element(By.XPATH, "//input[@value='IOS']")
            # item.click()
            self.driver.execute_script("arguments[0].click();", item)
            time.sleep(1)

        # 确定
        item = self.driver.find_element(
            By.XPATH, "//button[@class='btn btn-primary']")
        # item.click()
        self.driver.execute_script("arguments[0].click();", item)
        time.sleep(2)

        # 点击第一个
        item = self.driver.find_element(By.XPATH, "//div[@class='media']")
        item.click()
        time.sleep(1)


    def UpdateApkApi(self,isHD): 
        package = mainAppInfo.GetAppPackage(Source.ANDROID,isHD)
        apk = mainResource.GetOutPutApkPath(Source.HUAWEI, isHD)
        appid = mainAppInfo.GetAppId(isHD, Source.HUAWEI)
        mainHuaweiAppGalleryApi.UploadApk(appid,apk) 

    def DeleteAllLanguage(self, isHD):
        appid = mainAppInfo.GetAppId(isHD, Source.HUAWEI)  
        for country in self.listCountry:
            mainHuaweiAppGalleryApi.DeleteLanuage(appid,country)




    def UpdateAppInfo(self, isHD):
        appid = mainAppInfo.GetAppId(isHD, Source.HUAWEI)  
        defaultLang = "en-US"
        policyUrl= mainAppInfo.GetAppPrivacyUrl(isHD)
        mainHuaweiAppGalleryApi.UpdateAppBaseInfo(appid,defaultLang,policyUrl)

        idx = 0
        for country in self.listCountry:
            lan = self.listCountryLanguage[idx]
            title= mainAppInfo.GetAppName(Source.ANDROID, isHD,lan)
            detail = mainAppInfo.GetAppDetail(isHD,lan)
            shortDetail = mainAppInfo.GetAppPromotion(isHD,lan)
            whatsNew = mainAppInfo.GetAppUpdate(isHD,lan)
            mainHuaweiAppGalleryApi.UpdateAppInfo(appid,country,title,detail,shortDetail,whatsNew)

            # subtitle= mainAppInfo.GetAppSubtitle(isHD,lan)
            # 
            # policyText =""
 
            # keywords = mainAppInfo.GetAso(isHD,Source.APPSTORE,lan)
            # marketingUrl = mainAppInfo.GetAppSoftwareUrl(isHD)
            # promotionalText =  mainAppInfo.GetAppPromotion(isHD, lan) 
            # supportUrl =  mainAppInfo.GetAppSupportUrl(isHD)
            
          
            idx+=1


    def UploadScreenShot(self, isHD):
        appid = mainAppInfo.GetAppId(isHD, Source.HUAWEI) 
        # mainHuaweiAppGalleryApi.DeleteLanuage(appid,"zh-CN")
        # return
         
        pic = mainResource.GetOutPutCopyRightPathWin32(mainResource.GetProjectOutPut(), isHD)+"\\huawei.png"
        mainHuaweiAppGalleryApi.UploadImageCopyRight(appid,pic)
        # return

        idx = 0
        for country in self.listCountry:
            lan = self.listCountryLanguage[idx]
            icon = mainResource.GetOutPutIconPathWin32(mainResource.GetProjectOutPut(), Source.TAPTAP, isHD)+"\\huawei\\icon_android_216.png"
            mainHuaweiAppGalleryApi.UploadImageIcon(appid,icon,country)
            mainHuaweiAppGalleryApi.StartScreenShot()
            for i in range(0, 5):
                pic = mainResource.GetOutPutScreenshotPathWin32(mainResource.GetProjectOutPut(), Source.TAPTAP, isHD) + "\\"+lan+"\\1080p\\"+str(i+1)+".jpg"
                mainHuaweiAppGalleryApi.UploadOneScreenShot(appid,pic,isHD)
            mainHuaweiAppGalleryApi.CommitScreenShot(appid,isHD,country)

            idx+=1
 

    def SubmitAppApi(self, isHD):
        appid = mainAppInfo.GetAppId(isHD, Source.HUAWEI)
        mainHuaweiAppGalleryApi.SubmitApp(appid)



    def Run(self,type, isHD):     

        name = mainAppInfo.GetAppStoreAcount(isHD,Source.HUAWEI)
        mainHuaweiAppGalleryApi.ClientId = mainAppStoreAcount.GetClientId(Source.HUAWEI,name)
        mainHuaweiAppGalleryApi.ClientSecret = mainAppStoreAcount.GetClientSecret(Source.HUAWEI,name) 
        print(" mainHuaweiAppGalleryApi.ClientId =",mainHuaweiAppGalleryApi.ClientId,"name=",name)

        if type == "createapp":

            appid = mainAppInfo.GetAppId(isHD, Source.HUAWEI)

            if appid == "0":
                self.Init()
                self.GoHome(isHD)
                # self.Login("chyfemail163@163.com", "Qianlizhiwai1")
                name = mainAppInfo.GetAppStoreAcount(isHD,Source.HUAWEI)
                self.Login(name, mainAppStoreAcount.GetPassword(Source.HUAWEI,name))
                # 
                # self.SaveCookie(self.fileCookie)
             
            if isHD:
                self.CreateApp(isHD)
            else:
                self.CreateApp(False)
                time.sleep(3)
                self.CreateApp(True)
 

        # if type == "update":
            
        #     # if isHD:
        #     #     self.UpdateApp(True)
        #     # else:
        #     #     self.UpdateApp(False)
        #     #     time.sleep(3)
        #         # ad.UpdateApp(True)

        if type == "UploadScreenShot":
            if isHD:
                self.UploadScreenShot(True)
            else:
                self.UploadScreenShot(False)
                time.sleep(3)
                # ad.UpdateApp(True)

        if type == "UpdateAppInfo":
            self.UpdateAppInfo(False)
            self.UpdateAppInfo(True)

        if type == "DeleteAllLanguage":
            self.DeleteAllLanguage(isHD) 



        if type == "UpdateApk":
            if isHD:
                self.UpdateApkApi(True)
            else:
                self.UpdateApkApi(False)
                time.sleep(3)
                # ad.UpdateApp(True)

        # ad.Quit(300)
        if type == "UpdateVersion":
            if isHD:
                self.UpdateApkApi(True)
            else:
                self.UpdateApkApi(False)
                time.sleep(3)
            
            self.SubmitAppApi(isHD)

        

        print("AppStoreHuawei sucess")


mainAppStoreHuawei = AppStoreHuawei()