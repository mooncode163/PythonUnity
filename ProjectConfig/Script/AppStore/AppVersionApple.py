import sys
import zipfile
import shutil
import os
import os.path
import json

sys.path.append('../../') 
sys.path.append('./') 
from Common.File.FileDownload import mainFileDownload 

class AppVersionApple(): 

# https://itunes.apple.com/lookup?id=914391781
# https://itunes.apple.com/cn/lookup?id=914391781
    def GetHtml(self,appid):
        url = "https://itunes.apple.com/lookup?id="+appid
        # # 创建chrome浏览器驱动，无头模式（超爽）
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # self.driver = webdriver.Chrome(chrome_options=chrome_options)

        # # 加载百度页面
        # self.driver.get(url)
        # time.sleep(3)
        # # html = self.driver.execute_script("return document.documentElement.outerHTML")
        # html = self.driver.page_source
        html = mainFileDownload.DownloadData(url)
        return html

    def ParseVersion(self,appid):
        html = self.GetHtml(appid) 
        rootJson = json.loads(html) 
        jsonResult = rootJson["results"]; 
        version ="1.0.0"
        if len(jsonResult) == 0:
            return version
        
        jsonItem = jsonResult[0]
        url =  jsonItem["trackViewUrl"]
        # string key_releaseNotes = "releaseNotes";
        # if (Common.JsonDataContainsKey(jsonItem, key_releaseNotes))
        # {
        #     strUpdateNote = (string)jsonItem[key_releaseNotes];
        # }
        version =  jsonItem["version"]; 
        return version

    def GetAppName(self,appid):
        html = self.GetHtml(appid) 
        rootJson = json.loads(html) 
        jsonResult = rootJson["results"]; 
        version =""
        if len(jsonResult) == 0:
            return version
        
        jsonItem = jsonResult[0] 
        version =  jsonItem["trackName"]; 
        return version
        
  

mainAppVersionApple = AppVersionApple()  
