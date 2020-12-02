# 导入selenium的浏览器驱动接口


import sys
import os
import json
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
 
import AppInfo  
import time 
from Common import Source 
from AppStore.AppStoreBase import AppStoreBase  
from Project.Resource import mainResource
from AppInfo.AppInfo import mainAppInfo
from AppStore.AppStoreGoogleInternal import mainAppStoreGoogleInternal  
# 导入chrome选项


# pip3 install pywin32

# sys.path.append('../common')


class AppStoreGoogle(AppStoreBase):  
    HTTP_HEAD ="http://127.0.0.1:5000/"
# 3452644866 qq31415926
    def CreateApp(self, isHD):
        # ad.GoHome(isHD)
        time.sleep(1)
        print(" gp CreateApp")
        package = mainAppInfo.GetAppPackage(Source.ANDROID,isHD)
        name= mainAppInfo.GetAppName(Source.IOS, isHD,Source.LANGUAGE_EN) 
        gameName = mainResource.getGameName()
        gameType = mainResource.getGameType() 
        #self.driver.get(self.HTTP_HEAD+"GooglePlayDeveloperAPI/CreateApp?package="+package+"&name="+name+"&apptype="+gameType+"&appkey="+gameName+"&path="+mainResource.cmdPath)
        mainAppStoreGoogleInternal.Run("createapp",isHD)
         
#  https://developers.google.cn/android-publisher/api-ref/rest/v3/AppImageType?hl=zh-cn
    def UploadScreenShot(self,isHD):  
        package = mainAppInfo.GetAppPackage(Source.ANDROID,isHD) 
        gameName = mainResource.getGameName()
        gameType = mainResource.getGameType()
        mainAppStoreGoogleInternal.Run("UploadScreenShot",isHD)
        #self.driver.get(self.HTTP_HEAD+"GooglePlayDeveloperAPI/UploadScreenShot?package="+package+"&apptype="+gameType+"&appkey="+gameName+"&path="+mainResource.cmdPath)

    def UpdateAppInfo(self,isHD):  
        package = mainAppInfo.GetAppPackage(Source.ANDROID,isHD) 
        gameName = mainResource.getGameName()
        gameType = mainResource.getGameType()
        mainAppStoreGoogleInternal.Run("UpdateAppInfo",isHD)
        #self.driver.get(self.HTTP_HEAD+"GooglePlayDeveloperAPI/UpdateAppInfo?package="+package+"&apptype="+gameType+"&appkey="+gameName+"&path="+mainResource.cmdPath)

    def UpdateApk(self,isHD): 
        package = mainAppInfo.GetAppPackage(Source.ANDROID,isHD) 
        gameName = mainResource.getGameName()
        gameType = mainResource.getGameType()
        mainAppStoreGoogleInternal.Run("UpdateApk",isHD)
        #self.driver.get(self.HTTP_HEAD+"GooglePlayDeveloperAPI/UpdateApk?package="+package+"&apptype="+gameType+"&appkey="+gameName+"&path="+mainResource.cmdPath)

    def Run(self,type, isHD):     
        if type == "createapp":
            self.Init()
            # self.GoHome(isHD) 
            self.CreateApp(isHD)
            time.sleep(3)
            # ad.CreateApp(True)

        if type == "UpdateAppInfo":
            if isHD:
                self.UpdateAppInfo(True)
            else:
                self.UpdateAppInfo(False)
                time.sleep(3)
                # ad.UpdateApp(True)

            # ad.CreateApp(True)

        if type == "UploadScreenShot":
            if isHD:
                self.UploadScreenShot(True)
            else:
                self.UploadScreenShot(False)
                time.sleep(3)
                # ad.UpdateApp(True)            # ad.CreateApp(True)

        if type == "UpdateAppInfo":
            if isHD:
                self.UpdateAppInfo(True)
            else:
                self.UpdateAppInfo(False)
                time.sleep(3)
                # ad.UpdateApp(True)

        if type == "UpdateApk":
            if isHD:
                self.UpdateApk(True)
            else:
                self.UpdateApk(False)
                time.sleep(3)
                # ad.UpdateApp(True)

        # ad.Quit(300)


mainAppStoreGoogle = AppStoreGoogle()
    
 
