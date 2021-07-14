# 导入selenium的浏览器驱动接口
from selenium import webdriver

# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys

# 导入chrome选项
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import time; 

from WebDriver.WebDriverCmd import CmdType
from WebDriver.WebDriverCmd import WebDriverCmd 
from WebDriver.WebDriverCmd import CmdInfo 


from AppInfo import AppInfo
from DBApp import DBApp
from DBApp import mainDBApp


class ServerAppVersionTapTap():  
    driver:None
    def GetVersion(self,html, start,min,end):
        idx = html.find(start) 
        if idx<0:
            return ""
        idx = idx + len(start)
        strOther = html[idx:] 
        idx = strOther.find(min)
        idx = idx + len(min)
        strOther = strOther[idx:] 
        # print(strOther) 
        idx_end = strOther.find(end)
        # print(" idx_end =",idx_end) 
        strOther = strOther[0:idx_end]
        return strOther
 
    def GetHtml(self,appid): 
        url = "https://www.taptap.com/app/" + appid
        # 创建chrome浏览器驱动，无头模式（超爽）
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        # linux 上chrome上需要加上下面两句 ,不然会报错
        # 例如 unknown error: DevToolsActivePort file doesn‘t exist
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        # 加载百度页面
        self.driver.get(url)
        time.sleep(3)
        # html = self.driver.execute_script("return document.documentElement.outerHTML")
        html = self.driver.page_source
        return html

# https://www.taptap.com/app/46445
  

# <li>
#                       <span class="info-item-title">当前版本:</span>
#                       <span class="info-item-content">1.7.4</span>
#                     </li>
 
    def ParseVersionFromWeb(self,appid):
        html = self.GetHtml(appid) 
        # print(("taptap html=",html))
        webcmd = WebDriverCmd(self.driver) 
        version = "1.0.0"
        # return version
        # Current Version: 
        # 当前版本
        key = "//span[contains(text(),'当前版本')]"
        
        # key = "//span[text()='当前版本:']" 
        if not webcmd.IsElementExist(key):
            key = "//span[contains(text(),'Current Version')]"

        if webcmd.IsElementExist(key):
            item = webcmd.Find(key)
        # print(("taptap item=",item.text))


            # paragraph-m14-w14 gray-08 info-form__item__value
            key = "span[contains(@class,'info-form__item__value')]"
            brother = webcmd.FindBrother(item,key) 
            version = brother.text
        print("taptap version=",version)
        # return version
        # 关闭浏览器
        self.driver.quit()
        return version
 


    def GetVersion(self,cur_version,package,appid,isDebug=False): 
        # print(request.url)
        # appinfo = AppInfo()
        # appinfo.appid= "100270155"
        # appinfo.package= "com.moonma.caicaile"
        # appinfo.version= "2.1.0"

        db = DBApp()
        db.OpenDB("DBAppTaptap.db") 
        
        version = db.GetVersionByPackage(package)
        print(" dbversion = ",version)
        isByWeb = False
        if version<cur_version:
            isByWeb = True

        if isDebug:
            isByWeb =True

        if isByWeb:
            version = self.ParseVersionFromWeb(appid)
            appinfo = AppInfo()
            appinfo.appid= appid
            appinfo.package= package
            appinfo.version= version

            if db.IsItemExist(appinfo.package)==True: 
                db.UpdateItem(appinfo)
            else:
                # AddItem
                db.AddItem(appinfo)
            

        return version
 


mainServerAppVersionTapTap = ServerAppVersionTapTap() 
# # 主函数的实现
if __name__ == "__main__":

    mainServerAppVersionTapTap.ParseVersion("46445")
