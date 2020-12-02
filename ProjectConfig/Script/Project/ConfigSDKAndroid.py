#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path

# sys.path.append('./common')
# import common

o_path = os.getcwd()  # 返回当前工作目录
# 当前工作目录 Common/PythonUnity/ProjectConfig/Script
sys.path.append('../../') 
sys.path.append('./') 

# sys.path.append('./ziputils')
from Common.File.ZipUtil import ZipUtil
from Project.Resource import mainResource 
 
class ConfigSDKAndroid(): 

    def GetRootDirLibs(self):
        return mainResource.GetRootDirAndroidStudio() + "/libs"

    def GetRootDirAdSdk(self):
        return self.GetRootDirLibs() + "/ad_lib"

    def GetDirAdSdk(self,src):
        return self.GetRootDirAdSdk() + "/"+src
    
    def GetZipFileAdSdk(self,src):
        return self.GetDirAdSdk(src) +".zip"

    def GetRootDirAdSdkJavaCode(self):
        return mainResource.GetRootDirAndroidStudio() + "/src/main/java/com/moonma/common/adkit/platform"
    def GetDirAdSdkJavaCode(self,src):
        return self.GetRootDirAdSdkJavaCode() + "/"+src
    def GetZipFileAdSdkJavaCode(self,src,noad):
        ret =""
        if noad:
            ret = self.GetDirAdSdkJavaCode(src) +"_noad.zip"
        else:
            ret = self.GetDirAdSdkJavaCode(src) +".zip"
        return ret


    # 
    def DeleteMACOSX(self,root_dir):
        macosx_dir = root_dir+"/__MACOSX"
        flag = os.path.exists(macosx_dir)
        if flag:
            shutil.rmtree(macosx_dir)

    def SetAdSdk(self,src,enable):
        self.SetAdSdkLib(src,enable)
        self.SetAdSdkJavaCode(src,not enable)


    def GetDirShareSdkLib(self):
        return mainResource.GetRootDirAndroidStudio() + "/libs/share"

    def SetShareSdk(self,enable): 
        # lib
        dir_lib = self.GetDirShareSdkLib()
        file_zip = mainResource.GetRootDirAndroidStudio() + "/libs/share.zip"
        rootdir_lib = mainResource.GetRootDirAndroidStudio() + "/libs"

        flag = os.path.exists(dir_lib)
        if flag:
            shutil.rmtree(dir_lib) 

        if enable:
            flag = os.path.exists(file_zip)
            if flag:
                ZipUtil.un_zip(file_zip,rootdir_lib)

        self.DeleteMACOSX(rootdir_lib)

        # F:\sourcecode\unity\product\kidsgame\project_android\kidsgame\src\main\java\com\moonma\common\share
        # code
        dir_code = mainResource.GetRootDirAndroidStudio() + "/src/main/java/com/moonma/common/share"
        file_zip_enable = mainResource.GetRootDirAndroidStudio() + "/src/main/java/com/moonma/common/share.zip"
        file_zip_disable = mainResource.GetRootDirAndroidStudio() + "/src/main/java/com/moonma/common/share_disable.zip"
        rootdir_code = mainResource.GetRootDirAndroidStudio() + "/src/main/java/com/moonma/common"

        flag = os.path.exists(dir_code)
        if flag:
            shutil.rmtree(dir_code) 

        file_zip = file_zip_disable
        if enable:
            file_zip = file_zip_enable 

        flag = os.path.exists(file_zip)
        if flag:
            ZipUtil.un_zip(file_zip,rootdir_code)

        self.DeleteMACOSX(rootdir_code)

    

    # 备份游戏代码到CodeZip  压缩zip
    def SetAdSdkLib(self,src,enable):
        rootdir_ad = self.GetRootDirAdSdk()
        file_zip = self.GetZipFileAdSdk(src)   
        

        print (rootdir_ad)
        print(file_zip)

        dir_adsdk = self.GetDirAdSdk(src)
        flag = os.path.exists(dir_adsdk)
    
        if flag:
            shutil.rmtree(dir_adsdk) 

        if enable:
            flag = os.path.exists(file_zip)
            if flag:
                ZipUtil.un_zip(file_zip,rootdir_ad) 

        self.DeleteMACOSX(rootdir_ad)


    def SetAdSdkJavaCode(self,src,noad):
        rootdir_ad = self.GetRootDirAdSdkJavaCode()
        file_zip = self.GetZipFileAdSdkJavaCode(src,noad)   
        dir_adsdk = self.GetDirAdSdkJavaCode(src)
        print (dir_adsdk)
        print(file_zip)

        flag = os.path.exists(dir_adsdk)
        if flag:
            shutil.rmtree(dir_adsdk)  
        
        dir_adsdk_noad = dir_adsdk+"_noad"
        flag = os.path.exists(dir_adsdk_noad)
        if flag:
            shutil.rmtree(dir_adsdk_noad)
            

        ZipUtil.un_zip(file_zip,rootdir_ad)

        self.DeleteMACOSX(rootdir_ad)

mainConfigSDKAndroid = ConfigSDKAndroid()
