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

class AppVersionTapTap():  
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
 
    def ParseVersion(self,appid):
        html = self.GetHtml(appid) 
        # print(("taptap html=",html))
        webcmd = WebDriverCmd(self.driver) 

        # Current Version: 
        # 当前版本
        key = "//span[contains(text(),'当前版本')]"
        
        # key = "//span[text()='当前版本:']" 
        if not webcmd.IsElementExist(key):
            key = "//span[contains(text(),'Current Version')]"

        item = webcmd.Find(key)
        # print(("taptap item=",item.text))

        key = "span[@class = 'info-item-content']"
        brother = webcmd.FindBrother(item,key) 
        version = brother.text
        print("taptap version=",version)
        # 关闭浏览器
        self.driver.quit()
        return version
 



mainAppVersionTapTap = AppVersionTapTap() 
# # 主函数的实现
if __name__ == "__main__":

    mainAppVersionTapTap.ParseVersion("46445")
