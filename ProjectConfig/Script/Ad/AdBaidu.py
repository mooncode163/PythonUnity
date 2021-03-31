  
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
from Config.Config import mainConfig
from Config.AdConfig import mainAdConfig  
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
from AppStore.AppVersionHuawei import mainAppVersionHuawei
from AppStore.AppVersionApple import mainAppVersionApple
from AppStore.AppConnectApi import mainAppConnectApi
from Common.Platform import Platform
from Ad.AdBase import AdBase
from selenium.webdriver.support.select import Select 

from AppStore.AppStoreAcount import mainAppStoreAcount
from AppStore.UploadAssetApple import mainUploadAssetApple 
from AppStore.AppStoreApple import mainAppStoreApple

# 要想调用键盘按键操作需要引入keys包

# 导入chrome选项


# pip3 install pywin32

# sys.path.append('../common')


class AdBaidu(AdBase):
    driver: None
    dirRoot: None
    urlCreatePlaceId: None 
    osApp: None
    BANNER = "横幅"
    INSERT = "插屏"
    VIDEO = "激励视频"

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
        # self.driver.get("https://union.baidu.com/")
        print("GoHome")
        self.driver.get("https://union.baidu.com/bqt#/")
        print("GoHome 1")
        time.sleep(2)

 

    def Login(self, user, password):
        print("Login")

        self.urlold = self.driver.current_url
        print("Login urlold=", self.urlold)

        webcmd = WebDriverCmd(self.driver)
        webcmd.AddCmdWait(CmdType.CLICK_Action,"//div[@class='btn-login']")
        webcmd.Run(True) 


        webcmd.AddCmd(CmdType.INPUT,"//input[@id='uc-common-account']",user)
        webcmd.AddCmd(CmdType.INPUT,"//input[@id='ucsl-password-edit']",password)

        # 登录
        # <div class="login-action">
        # webcmd.AddCmd(CmdType.CLICK_Action,"//input[@id='submit-formt']")
        # webcmd.AddCmd(CmdType.CLICK_Action,"//div[@class='login-action']")

        webcmd.Run(True) 

        # self.LoginQQ(user, password)
        # self.SaveCookie()
        # 等待登录成功
        while True:
            time.sleep(1)
            self.urlnew = self.driver.current_url
            print("Login urlnew=", self.urlnew)
            if self.urlnew != self.urlold:
                print("Login Finish =", self.urlnew)
                break
 
 
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


    def SetText(self, key,title): 
        webcmd = WebDriverCmd(self.driver)
        if Platform.isWindowsSystem():
            pyperclip.copy(title) 
            pyperclip.paste()
            webcmd.AddCmd2(CmdType.CLICK_Action, key)
            webcmd.AddCmd2(CmdType.CTR_V, key) 
        else:
            webcmd.AddCmd(CmdType.INPUT, key,title)

        webcmd.Run(True)

 
# .apk
    def DeleteAllDownloadFile(self,sourceDir,file_ext):
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,  file)
                #cover the files
            if os.path.isfile(sourceFile):
                # print sourceFile
                # 分割文件名与后缀
                temp_list = os.path.splitext(file)
                # name without extension
                src_apk_name = temp_list[0]
                # 后缀名，包含.   例如: ".apk "
                ext = temp_list[1]
                # apk_ext='.apk';
                if file_ext==ext:
                    print(sourceFile)
                    os.remove(sourceFile)
# .apk
    def GetDownloadFile(self,sourceDir,file_ext):
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,  file)
                #cover the files
            if os.path.isfile(sourceFile):
                # print sourceFile
                # 分割文件名与后缀
                temp_list = os.path.splitext(file)
                # name without extension
                src_apk_name = temp_list[0]
                # 后缀名，包含.   例如: ".apk "
                ext = temp_list[1] 
                if file_ext==ext:
                    print(sourceFile)
                    return sourceFile

        return ""

    def GetPathXcodePrifile(self,isHd): 
        package = mainAppInfo.GetAppPackage(Source.IOS,isHd)
        path = mainResource.GetResourceDataApp()+"/"+package+".mobileprovision"
        if os.path.exists(path)==False:
            package = package.replace(".","")
            path = mainResource.GetResourceDataApp()+"/"+package+".mobileprovision"
        return os.path.normpath(path)

 

    def DownloadAppleDeveloper(self,isHd):
        url = "https://developer.apple.com/account/resources/profiles/add"
        self.driver.get(url)
        time.sleep(3)
        webcmd = WebDriverCmd(self.driver)

        key = "//button[@id='action-ok']"
        item = webcmd.Find(key)
        if item is not None:
            item = webcmd.AddCmd(CmdType.CLICK_Action, key)
            webcmd.Run(True)
            self.driver.get(url)

        # <label for="IOS_APP_STORE">
        key = "//label[@for='IOS_APP_STORE']"
        item = webcmd.AddCmdWait(CmdType.CLICK_Action, key) 
        webcmd.Run(True)

        # <button type="summit" id="action-continue" class="tb-btn--primary">Continue</button> 
        key = "//button[@id='action-continue']"
        item = webcmd.AddCmd(CmdType.CLICK_Action, key) 
        webcmd.Run(True)
        package = mainAppInfo.GetAppPackage(Source.IOS,isHd)
        print(package)
        # select app
        # <div class=" css-1hwfws3">
        key = "//div[@class=' css-1hwfws3']"
        item = webcmd.AddCmdWait(CmdType.CLICK_Action, key) 
        webcmd.Run(True)

        key = "//input[@id='react-select-2-input']"
        item = webcmd.AddCmdWait(CmdType.INPUT, key,package) 
        webcmd.Run(True)

        # 手工输入包名
        # <div><label for="name">Provisioning Profile Name</label><input type="text" maxlength="50" id="name" class="form-text text-input" required=""></div>

        key = "//input[@id='name']"
        item = webcmd.Find( key,True) 

        webcmd.AddCmd(CmdType.INPUT, key,package) 
        webcmd.Run(True)

        # <button type="submit" id="action-continue" class="tb-btn--primary">Generate</button>
        key = "//button[@id='action-continue']"
        item = webcmd.AddCmd(CmdType.CLICK_Action, key) 
        webcmd.Run(True)
        
        # <a class="tb-btn--primary" download="" href="/services-account/QH65B2/account/ios/profile/downloadProfileContent?teamId=Y9ZUK2WTEE&amp;provisioningProfileId=TUNL6PRSZA">Download</a>
        key = "//a[@class='tb-btn--primary']"
        item = webcmd.AddCmdWait(CmdType.CLICK_Action, key) 
        webcmd.Run(True)

    def LoginAppleDeveloper(self,user,password):
        webcmd = WebDriverCmd(self.driver)
        self.driver.get("https://developer.apple.com/account")
        time.sleep(1)

        self.urlold = self.driver.current_url
        print("Login urlold=",self.urlold) 

        # 等待网页加载成功
        key = "//iframe[@id='aid-auth-widget-iFrame']"
        while True:
            # self.driver.switch_to.frame('aid-auth-widget-iFrame')
            time.sleep(1)
            print("web is loading...")
            if webcmd.IsElementExist(key)==True:
                print("web loading finish")
                break

        self.driver.switch_to.frame('aid-auth-widget-iFrame')
        time.sleep(1)

        key = "//input[@id='account_name_text_field']"
        item = webcmd.AddCmdWait(CmdType.INPUT, key,user) 
        webcmd.Run(True)
        key = "//button[@id='sign-in']"
        item = webcmd.AddCmdWait(CmdType.CLICK_Action, key) 
        webcmd.Run(True)
 
        time.sleep(1)

        key = "//input[@id='password_text_field']"
        item = webcmd.AddCmdWait(CmdType.INPUT, key,password) 
        webcmd.Run(True)
        key = "//button[@id='sign-in']"
        item = webcmd.AddCmdWait(CmdType.CLICK_Action, key) 
        webcmd.Run(True)
  

        # 等待登录成功
        while True:
            time.sleep(1)  
            self.urlnew = self.driver.current_url
            print("Login urlnew=",self.urlnew)
            if self.urlnew!=self.urlold:
                print("Login Finish =",self.urlnew)
                break
     

    def UpLoadSigniOS(self,isHd):
        webcmd = WebDriverCmd(self.driver)
        # downloadDir = "C:\\Users\\moon\\Downloads"   
        # self.DeleteAllDownloadFile(downloadDir,".mobileprovision")

        # self.LoginAppleDeveloper("chyfemail163@163.com","Moonqianlizhiwai1")
        # self.DownloadAppleDeveloper(isHd)

        # .mobileprovision
        # appsign =self.GetDownloadFile(downloadDir,".mobileprovision") 
        appsign =self.GetPathXcodePrifile(isHd)


        # 上传签名包
        # key = "//input[@accept='.apk' and @name='file']"
        key = "//label[@class='veui-button veui-uploader-input-label']"
        item = webcmd.AddCmdWait(CmdType.CLICK_Action, key)
        # webcmd.SetItemVisible(item)
        webcmd.Run(True)

        self.OpenFileBrowser(appsign)

    def UpLoadSignAndroid(self,isHD):
        webcmd = WebDriverCmd(self.driver)
          # E:\Users\moon\Downloads
        
        if Platform.isWindowsSystem():
            downloadDir = "C:\\Users\\moon\\Downloads"

        if Platform.isMacSystem():
            downloadDir = "/Users/moon/Downloads"

        self.DeleteAllDownloadFile(downloadDir,".apk")

        # 下载空包 E:\Users\moon\Downloads\mssp-verify-b8920a35.apk
        key = "//button[@class='veui-button bottom20']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)

        time.sleep(3)
        apk_unsign = self.GetDownloadFile(downloadDir,".apk") 
        apk_sign = mainResource.GetProjectOutPut()+"/mssp_baidu/signed.apk"
        if isHD:
            apk_sign = mainResource.GetProjectOutPut()+"/mssp_baidu/signed_hd.apk"

        FileUtil.CreateDir(FileUtil.GetLastDirofDir(apk_sign))
        jks = mainResource.GetDirProductCommon()+"/Ad/moonma.jks"

        if Platform.isWindowsSystem(): 
     
            # sign apk:
            # jarsigner -verbose -keystore ~/sourcecode/mssp_baidu/moonma.jks -signedjar ~/sourcecode/mssp_baidu/signed.apk ~/sourcecode/mssp_baidu/empty.apk moonma -storepass qianlizhiwai
            cmd = "jarsigner -verbose -keystore "+jks+" -signedjar "+apk_sign+" "+apk_unsign+" moonma -storepass qianlizhiwai"
            
        if Platform.isMacSystem(): 
            # sign apk:
            # jarsigner -verbose -keystore ~/sourcecode/mssp_baidu/moonma.jks -signedjar ~/sourcecode/mssp_baidu/signed.apk ~/sourcecode/mssp_baidu/empty.apk moonma -storepass qianlizhiwai
            cmd = "jarsigner -verbose -keystore "+jks+" -signedjar "+apk_sign+" "+apk_unsign+" moonma -storepass qianlizhiwai"
            
        print(cmd)
        os.system(cmd)
        time.sleep(1)

        # sign end

        # 滚动到浏览器顶部
        js_top = "var q=document.documentElement.scrollTop=0"
        # 滚动到浏览器底部
        js_bottom = "var q=document.documentElement.scrollTop=document.documentElement.scrollHeight"
        self.driver.execute_script(js_bottom)
        time.sleep(2)

        # 上传签名包
        # key = "//input[@accept='.apk' and @name='file']"
        key = "//label[@class='veui-button veui-uploader-input-label']"
        item = webcmd.AddCmd(CmdType.CLICK_Action, key)
        # webcmd.SetItemVisible(item)
        webcmd.Run(True)

        self.OpenFileBrowser(apk_sign) 

        if Platform.isMacSystem():
            # 等待 
            webcmd.WaitKeyBoard('q')
            time.sleep(1)


# 3452644866 qq31415926
    def CreateApp(self, isHD):
        self.driver.get("http://union.baidu.com/bqt/appco.html#/promotion/application/create")
        time.sleep(1)

        webcmd = WebDriverCmd(self.driver)
        appChannel = Source.TAPTAP
        appid = mainAppInfo.GetAppId(isHD, Source.TAPTAP)
        appurl = "https://www.taptap.com/app/"+appid 
        if appid=="0":
            appid = mainAppInfo.GetAppId(isHD, Source.HUAWEI)
            appChannel = Source.HUAWEI
            # appurl = mainAppVersionHuawei.GetApkUrl(mainAppInfo.GetAppId(isHD, Source.HUAWEI)) 
            appurl = "https://appgallery1.huawei.com/#/app/C"+appid

 
        key = "//input[@type='text' and @name='name']"
        title = self.GetAppName(isHD)
        if self.osApp== Source.IOS:
            appid = mainAppInfo.GetAppId(isHD, Source.APPSTORE)
            title = mainAppVersionApple.GetAppName(appid)

        self.SetText(key,title)

# 行业
        key = "//div[@class='veui-select veui-select-empty']"
        div = webcmd.Find(key)
        key = ".//button[@aria-haspopup='listbox']"
        item = webcmd.FindChild(div,key)
        item.click()

        time.sleep(1)
        key = "//span[@class='veui-option-label' and text()='教育']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)

        time.sleep(1)
        key = "//span[@class='veui-option-label' and text()='儿童']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)
        


        

        key = "//input[@type='text' and @name='keyword']"
        title = self.GetAppName(isHD)
        self.SetText(key,title)

        key = "//textarea[@class='veui-textarea-input']"
        title = mainAppInfo.GetAppDetail(isHD,Source.LANGUAGE_CN)
        max = 150
        if len(title)>=max:
            title = title[0:max-1]
        self.SetText(key,title)

        # <button type="button" class="veui-button">  Android </button>
        if self.osApp== Source.ANDROID:
            key = "//button[@class='veui-button' and contains(text(),'Android')]"
            webcmd.AddCmd(CmdType.CLICK, key)
            webcmd.Run(True)

        


        key = "//input[@type='text' and @name='packageName']"
        title = mainAppInfo.GetAppPackage(self.osApp,isHD)
        self.SetText(key,title)
 
        #应用市场 http://app.mi.com/details?id=com.kibey.prophecy
        if self.osApp== Source.ANDROID:
            key = "//button[@class='veui-button veui-dropdown-button']"
            webcmd.AddCmd(CmdType.CLICK, key)
            webcmd.Run(True)

            time.sleep(1)
            keyword = ""
            if appChannel == Source.TAPTAP:
                keyword = "TapTap"
            if appChannel == Source.HUAWEI:
                # 华为应用市场
                keyword = "华为"

            key = "//span[@class='veui-option-label' and text()='"+keyword+"']"
            webcmd.AddCmd(CmdType.CLICK, key)
            webcmd.Run(True)  

        if self.osApp== Source.IOS:
            appurl = mainAppInfo.GetAppUrl(Source.IOS,isHD,Source.APPSTORE)

        key = "//input[@type='text' and @name='appUrl']"
        # http(s)://appdl-drcn.dbankcdn.com/xxx或者http(s)://appdlc-drcn.hispace.hicloud.com/xxx
        # http://appdlc-drcn.hispace.hicloud.com/dl/appdl/application/apk/7c/7c1e552794ec43d488e9149e6c4644a7/com.ss.android.ugc.aweme.lite.2007201350.apk
        print("appurl=",appurl)
        self.SetText(key,appurl)

        old_window = self.driver.current_window_handle
        # 下一步
        # <button ui="primary" type="submit" class="veui-button">下一步</button>
        key = "//button[@ui='primary' and @type='submit']"
        webcmd.AddCmd(CmdType.CLICK, key)
        webcmd.Run(True)

                # 跳转到新的页面
        print("self.driver.current_url=", self.driver.current_url)
        # self.driver.switch_to.window(self.driver.window_handles[0])
        for win in self.driver.window_handles:
            if win != old_window:
                self.driver.switch_to.window(win)
        time.sleep(3)
        print("self.driver.current_url 2=", self.driver.current_url)
 
 
        if self.osApp== Source.ANDROID:
            self.UpLoadSignAndroid(isHD)
        if self.osApp== Source.IOS:
            self.UpLoadSigniOS(isHD)

        # 完成
        key = "//button[@ui='primary' and @type='submit']"
        webcmd.AddCmd(CmdType.CLICK_Action, key)
        webcmd.Run(True)
        
        # self.CreatePlaceId(isHD)
         

    def GetAppName(self, ishd): 
        name = mainAppInfo.GetAppName(self.osApp, ishd,Source.LANGUAGE_CN) 
        return name
  
# ID:abb4293d
    def GetAdPlaceId(self, str): 
        head = "ID:"
        idx = str.find(head)+len(head)
        appid = str[idx:]
        print("appid=",appid)
        return appid

    def SearchApp(self, ishd): 
        if self.appId!="0":
            return 
        name = self.GetAppName(ishd)
        print("GetAppName=",name)

        webcmd = WebDriverCmd(self.driver)
        self.driver.get("http://union.baidu.com/bqt/appco.html#/promotion/application")
        time.sleep(3) 

        key = "//button[@class='veui-button filters' and contains(text(),'筛选')]" 
        webcmd.AddCmd(CmdType.CLICK_Action, key,name)
        webcmd.Run(True) 

        print("SearchApp self.osApp=",self.osApp)
        if self.osApp==Source.ANDROID:
            key = "//span[@class='filter-option' and contains(text(),'Android')]" 
        if self.osApp==Source.IOS:
            key = "//span[@class='filter-option' and contains(text(),'iOS')]" 
        
        print("SearchApp key=",key)
        webcmd.AddCmd(CmdType.CLICK_Action, key)
        webcmd.Run(True) 
 
        key = "//button[@ui='primary' and contains(text(),'确定')]"
        webcmd.AddCmd(CmdType.CLICK_Action, key)
        webcmd.Run(True) 
 
        key = "//input[@role='searchbox']"
        webcmd.AddCmd(CmdType.INPUT, key,name)
 
        key = "//button[@aria-label='搜索']"
        webcmd.AddCmd(CmdType.CLICK_Action, key)
        webcmd.Run(True) 

        time.sleep(2)

        key = "//div[@class='table-multi-line']"
        div = webcmd.Find(key)
        key = ".//div[@class='one-line']"
        # div1 = webcmd.FindChild(div,key)
        title = name
        self.appName = title
        print("title=",title)
        # key = ".//div[@class='sec-line']"
        # div2 = webcmd.FindChild(div,key)
        # ID:abb4293d 
        # self.appId = self.GetAdPlaceId(div2.text)


        # <div class="table-multi-line"><div class="one-line">开心猜猜乐</div><div class="sec-line">ID:a49df22d</div></div>
        key = "//div[@class='one-line' and text()='"+self.appName+"']/../div[@class='sec-line']"
        item = webcmd.Find(key)
        text = item.text
        head = "ID:"
        idx = text.find(head)+len(head)
        self.appId = text[idx:]
        # self.appId = self.appKey
        # key = "//button[@ui='link' and contains(text(),'修改')]"

        # 先找父节点tr
        key = "//div[@class='one-line' and text()='"+self.appName+"']"
        div_name = webcmd.Find(key)
        tr = webcmd.GetParent(div_name,4)
        # tr = webcmd.GetParent(tr)
        # tr = webcmd.GetParent(tr)
        # tr = webcmd.GetParent(tr)
        # key = "//div[@class='one-line' and text()='"+self.appName+"']/../../../../button[@ui='link' and contains(text(),'修改')]"
        # key = "//div[@class='one-line' and text()='"+self.appName+"']/../../../../"
        # tr = webcmd.Find(key)
        key = ".//button[@ui='link' and contains(text(),'修改')]"
        button = webcmd.FindChild(tr,key)
        webcmd.DoCmd(button,CmdType.CLICK_Action)
        # listbtn = webcmd.FindList(key)
        # if ishd:
        #     item = listbtn[0]
        # else:
        #     item = listbtn[1]

        # webcmd.DoCmd(item,CmdType.CLICK_Action)
        # webcmd.AddCmd(CmdType.CLICK_Action, key)
        # webcmd.Run(True) 
        time.sleep(2)

        print("self.driver.current_url=", self.driver.current_url)
        url = self.driver.current_url
        head = "id="
        idx = url.find(head)+len(head)
        self.appKey = url[idx:]
        print("appKey=",self.appKey)
        # http://union.baidu.com/bqt/appco.html#/promotion/application/edit?id=275514138
    
  
    def GetAdInfo(self, ishd):
        print("GetAdInfo ishd=",ishd)
        self.SearchApp(ishd) 
        
        name = self.GetAppName(ishd)
        webcmd = WebDriverCmd(self.driver)
        # self.driver.get("http://union.baidu.com/bqt/appco.html#/union/slot")
        # http://union.baidu.com/bqt/appco.html#/union/slot?system=2&appId=275514138
        system = 1
        if self.osApp==Source.ANDROID:
            system = 2

        if self.osApp==Source.IOS:
            system = 1

        url = "http://union.baidu.com/bqt/appco.html#/union/slot?system="+str(system)+"&appId="+self.appKey
        print("GetAdInfo url=",url)  
        self.driver.get(url)
        time.sleep(3)  
        key = "//div[@id='watermarker-id']"
        div_main = webcmd.Find(key) 

        key = ".//table[@ui='slim alt' and @class='veui-table']"
        table = webcmd.FindChild(div_main,key)   
        # <table ui="slim alt" class="veui-table">

        # <input type="text" autocomplete="off" role="searchbox" aria-haspopup="listbox" class="veui-input-input">
        # key = "//input[@type='text' and @role='searchbox']"
        # webcmd.AddCmd(CmdType.INPUT, key,name)
        # webcmd.Run(True)
        # https://blog.csdn.net/weixin_41858542/article/details/85068645
        # WebElement parent = child.findElement(By.xpath("./.."));// 找到父元素
        # List<WebElement> children = parent.findElements(By.xpath("./*"));// 找到所有子元素
        # <div class="veui-table-cell"><div title="激励视频 创建于 2020-07-29" class="slot-cell">激励视频 创建于 2020-07-29</div><div class="tableID filter-cell">ID:7177592</div></div>
        key = "//div[@class='tableID filter-cell' and contains(text(),'ID:')]"
        list = webcmd.FindList(key)
        for item in list: 
            adid = self.GetAdPlaceId(item.text)
            # 兄弟节点
            brother = item.find_element_by_xpath(".//../div[@class='slot-cell']")
            title = brother.text
            print(title)
            if title.find(self.BANNER)>=0:
                self.adIdBanner = adid
            if title.find(self.INSERT)>=0:
                self.adIdInsert = adid
            if title.find(self.VIDEO)>=0:
                self.adIdVideo = adid
        
        self.SaveAdIdToJson(self.osApp,ishd,Source.BAIDU)



    def CreatePlaceId(self, isHD):
        self.SearchApp(isHD)
        self.CreateAdBanner(isHD)
        self.CreateAdInsert(isHD)
        self.CreateAdVideo(isHD)
        time.sleep(1)
        self.GetAdInfo(isHD)

    def OpenFileBrowser(self,filepath):
        FileBrowser.OpenFile(filepath,True)
    

    def SelectApp(self):
        webcmd = WebDriverCmd(self.driver) 

        key = "//button[@aria-haspopup='listbox' and @aria-disabled='false']"
        webcmd.AddCmd(CmdType.CLICK_Action, key)
        webcmd.Run(True)

        key = "//input[@name='basic.appSid']"
        webcmd.AddCmd(CmdType.INPUT, key,self.appId)
        webcmd.Run(True)

        # <span class="veui-select-label">儿童学形状和颜色(andriod) (ID:e72aabfc)</span>
        # 父节点button
        try:
            # key = "//span[@class='veui-option-label' and contains(text(),"+self.appId+")]/parent::button"
            # item = webcmd.Find(key)
            key = "//span[@class='veui-option-label' and contains(text(),"+self.appId+")]"
            item = webcmd.Find(key,True)
            button = webcmd.GetParent(item)
            print(button.tag_name)
            # CLICK_Action
            # webcmd.SetItemVisible(item)
            webcmd.DoCmd(item,CmdType.CLICK)
            time.sleep(2)
            # webcmd.WaitKeyBoard('q')
            # CLICK_SCRIPT CLICK_Action
            # item = webcmd.AddCmd(CmdType.CLICK_Action, key)
            # if item==None:
            #     print("no key SelectApp key=",key)
            # # webcmd.SetItemVisible(item)
            # webcmd.Run(True) 
        except Exception as e:
            print(e) #打印所有异常到屏幕
            # 手动选择
            webcmd.WaitKeyBoard('q')
            time.sleep(2)

        time.sleep(1)

    def CreateAdBanner(self, isHD): 
        self.driver.get("http://union.baidu.com/bqt/appco.html#/union/slot/create") 
        webcmd = WebDriverCmd(self.driver)
        time.sleep(3)

        name = self.GetAppName(isHD)

        key = "//input[@name='name']"
        webcmd.AddCmd(CmdType.INPUT_CLEAR, key)
        webcmd.AddCmd(CmdType.INPUT, key,self.BANNER+"_"+name)
        webcmd.Run(True) 

         # 选择应用  
        self.SelectApp()

 
        key = "//button[@class='veui-button' and contains(text(),'"+self.BANNER+"')]"
        webcmd.AddCmd(CmdType.CLICK_Action, key)
        webcmd.Run(True) 
 
        key = "//button[@ui='primary' and @type='submit' and contains(text(),'确定')]"
        webcmd.AddCmd(CmdType.CLICK_Action, key)
        webcmd.Run(True) 
        time.sleep(3)


    def CreateAdInsert(self, isHD):
        self.driver.get("http://union.baidu.com/bqt/appco.html#/union/slot/create") 
        webcmd = WebDriverCmd(self.driver)
        time.sleep(3)

        name = self.GetAppName(isHD)

        key = "//button[@class='veui-button' and contains(text(),'"+self.INSERT+"')]"
        webcmd.AddCmd(CmdType.CLICK_Action, key)
        webcmd.Run(True) 
 

        key = "//input[@name='name']"
        webcmd.AddCmd(CmdType.INPUT_CLEAR, key)
        webcmd.AddCmd(CmdType.INPUT, key,self.INSERT+"_"+name)
        webcmd.Run(True)  

        # 选择应用  
        self.SelectApp()

 
        key = "//span[@class='veui-radio-label' and contains(text(),'全屏')]"
        webcmd.AddCmd(CmdType.CLICK_Action, key) 
        key = "//span[@class='veui-checkbox-label' and contains(text(),'蜂窝数据4G网络')]"
        webcmd.AddCmd(CmdType.CLICK_Action, key) 
        key = "//span[@class='veui-checkbox-label' and contains(text(),'2G/3G等其他网络')]"
        webcmd.AddCmd(CmdType.CLICK_Action, key)
        webcmd.Run(True) 
 

        key = "//button[@ui='primary' and @type='submit' and contains(text(),'确定')]"
        webcmd.AddCmd(CmdType.CLICK_Action, key)
        webcmd.Run(True) 
        time.sleep(3)


    def CreateAdVideo(self, isHD):
        self.driver.get("http://union.baidu.com/bqt/appco.html#/union/slot/create") 
        webcmd = WebDriverCmd(self.driver)
        time.sleep(3)

        name = self.GetAppName(isHD)

        key = "//button[@class='veui-button' and contains(text(),'"+self.VIDEO+"')]"
        webcmd.AddCmd(CmdType.CLICK_Action, key)
        webcmd.Run(True) 
 

        key = "//input[@name='name']"
        webcmd.AddCmd(CmdType.INPUT_CLEAR, key)
        webcmd.AddCmd(CmdType.INPUT, key,self.VIDEO+"_"+name)
        webcmd.Run(True) 
  
        # 选择应用  
        self.SelectApp()
 
        key = "//button[@ui='primary' and @type='submit' and contains(text(),'确定')]"
        webcmd.AddCmd(CmdType.CLICK_Action, key)
        webcmd.Run(True) 
        time.sleep(3)

    def RunDownloadSigniOS(self): 
        mainAppStoreApple.DownloadProfile(False)
        mainAppStoreApple.DownloadProfile(True)
        
    def OnCreatePlaceId(self,isHD): 
        if isHD:
            self.CreatePlaceId(True)
        else:
            self.CreatePlaceId(False)
            time.sleep(3)
            self.CreatePlaceId(True) 
# 主函数的实现
    def Run(self,type, os,isHD):     
        self.osApp = os  
        print("adbaidu run isHD=",isHD)

        name = mainAppInfo.GetAppStoreAcount(isHD,Source.APPSTORE)
        print("name=",name)
        mainAppConnectApi.API_KEY_ID = mainAppStoreAcount.GetiOSAPI_KEY_ID(name)
        print("API_KEY_ID=",mainAppConnectApi.API_KEY_ID)
        mainAppConnectApi.API_USER_ID = mainAppStoreAcount.GetiOSAPI_USER_ID(name) 
        mainAppConnectApi.teamID = mainAppStoreAcount.GetiOSteamID(name) 
        mainAppConnectApi.CertificateID = mainAppStoreAcount.GetiOSCertificateID(name) 

        mainUploadAssetApple.KEY_ID = mainAppConnectApi.API_KEY_ID
        mainUploadAssetApple.ISSUER_ID = mainAppConnectApi.API_USER_ID
        mainUploadAssetApple.PRIVATE_KEY = mainAppConnectApi.GetKEY_PRIVATE()
        mainUploadAssetApple.tokenKey = mainAppConnectApi.GetToken()

        self.Init()

        time.sleep(1)

        self.GoHome()
        self.Login("moonmaapp","Qianlizhiwai1")
        if self.osApp == Source.IOS:
            self.RunDownloadSigniOS()

        if type == "createapp":
            if isHD:
                self.CreateApp(True)
            else:
                self.CreateApp(False)
                time.sleep(3)
                self.CreateApp(True)

            # 
            self.OnCreatePlaceId(isHD)



        if type == "createplaceid":
            self.OnCreatePlaceId(isHD)
  

        if type == "adinfo":
            self.GetAdInfo(False)
            time.sleep(3)
            self.appId="0"
            self.appKey="0"
            self.GetAdInfo(True)

        print("AdBaidu sucess")

mainAdBaidu = AdBaidu()
