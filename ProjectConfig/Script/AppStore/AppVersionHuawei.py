# 导入selenium的浏览器驱动接口
from selenium import webdriver

# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys

# 导入chrome选项
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import time; 

from Common.WebDriver.WebDriverCmd import CmdType
from Common.WebDriver.WebDriverCmd import WebDriverCmd 
from Common.WebDriver.WebDriverCmd import CmdInfo 

class AppVersionHuawei():  
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

# https://appgallery1.huawei.com/#/app/C101026329
    def GetHtml(self,appid):
        url = "https://appgallery1.huawei.com/#/app/C"+appid
        # 创建chrome浏览器驱动，无头模式（超爽）
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        # 加载百度页面
        self.driver.get(url)
        time.sleep(3)
        # html = self.driver.execute_script("return document.documentElement.outerHTML")
        html = self.driver.page_source
        return html

    def ParseVersion(self,appid):
        html = self.GetHtml(appid) 
        start = ">版本<"
        start_en = ">Version<"
        mid = "info_val\">"
        end = "</div>"

        version = self.GetVersion(html,start,mid,end)
        if version=="":
            version = self.GetVersion(html,start_en,mid,end)

        if version=="":
            version = "1.0.0"

        print(version) 
        # print(html)
        # saveString2File(html,"1.html")
        # 关闭浏览器
        self.driver.quit()
        return version

    def GetApkUrl(self,appid):
        html = self.GetHtml(appid)
        webcmd = WebDriverCmd(self.driver)
        strappid = "C"+appid
        key = "//div[@appid='"+strappid+"']"
        item = webcmd.Find(key)
        url = item.get_attribute("apkdownloadurl")
        print("apk=",url)
        return url



mainAppVersionHuawei = AppVersionHuawei() 
# # 主函数的实现
# if __name__ == "__main__":

#     ParseVersion("100270155")
