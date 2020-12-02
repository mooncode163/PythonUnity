# 导入selenium的浏览器驱动接口
from selenium import webdriver

# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys

# 导入chrome选项
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import time; 

class AppVersionHuawei():  
    def saveString2File(self,str, file):
        f = open(file, 'wb')  # 若是'wb'就表示写二进制文件
        b = str.encode('utf-8',"ignore")
        f.write(b)
        f.close()
 
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


    def ParseVersion(self,appid):
        url = "https://appgallery1.huawei.com/#/app/C"+appid
        # 创建chrome浏览器驱动，无头模式（超爽）
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)

        # 加载百度页面
        driver.get(url)
        time.sleep(3)

        # 获取页面名为wrapper的id标签的文本内容
        # data = driver.find_element_by_id("wrapper").text
        # print(data)

        # 打印页面标题 "百度一下，你就知道"
        # print(driver.title)

        # 生成当前页面快照并保存
        # driver.save_screenshot("baidu.png")
        # item = driver.find_element(By.CLASS_NAME, "detailInfo")
        # print(item.text)

        # 打印网页渲染后的源代码
        print("page_source")
        # print(driver.page_source)

        html = driver.execute_script("return document.documentElement.outerHTML")
        html = driver.page_source
        start = ">版本<"
        start_en = ">Version<"
        mid = "info_val\">"
        end = "</div>"

        version = self.GetVersion(html,start,mid,end)
        if version=="":
            version = self.GetVersion(html,start_en,mid,end)

        if version=="":
            version = "0.0.0"

        print(version) 
        # print(html)
        # saveString2File(html,"1.html")
        # 关闭浏览器
        driver.quit()
        return version


mainAppVersionHuawei = AppVersionHuawei() 
# # 主函数的实现
# if __name__ == "__main__":

#     ParseVersion("100270155")
