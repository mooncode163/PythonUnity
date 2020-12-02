#!/usr/bin/python
# coding=utf-8
import zipfile
import shutil
import os
import os.path
import time,  datetime
import sys

#include AppInfo.py
sys.path.append('../../') 
sys.path.append('./')  
from Config.Config import mainConfig
from Common import Source
from Config.AdConfig import mainAdConfig  
from Project.Resource import mainResource
from Common.File.FileUtil import FileUtil 
from Common.File.ZipUtil import ZipUtil 
from Project.IPABuild import mainIPABuild
from Project.IPABuild import IPABuild
from Common.Platform import Platform


class AppstoreUploadiOS():   
  
# http://help.apple.com/itc/appsspec/#/itc6e4198248
# Transporter 上传工具
# https://help.apple.com/itc/transporteruserguide
#主函数的实现
    def Run(self,isHD): 
        strFile = "app.itmsp"
        if isHD:
            strFile = "app_pad.itmsp"
        
        if Platform.isWindowsSystem():
            strCmd = " "
        else:
            if mainIPABuild.IsXcode10():
                strCmd = "/Applications/Xcode.app/Contents/Applications/Application\ Loader.app/Contents/itms/bin/iTMSTransporter -m upload -u "+Source.APPSTORE_USER+" -p "+Source.APPSTORE_PASSWORD+"  -v eXtreme -f "+mainResource.GetProjectConfigApp()+ "/appstore/ios/"+strFile
            else:
                #xcode 11: 手动更新Transporter组件(java)方法： https://www.lagou.com/lgeduarticle/94642.html
                strCmd = "/Applications/Transporter.app/Contents/itms/bin/iTMSTransporter -m upload -u "+Source.APPSTORE_USER+" -p "+Source.APPSTORE_PASSWORD+"  -v eXtreme -f "+mainResource.GetProjectConfigApp()+ "/appstore/ios/"+strFile
        os.system(strCmd) 
            
        print ("appstore_upload_ios sucess")

mainAppstoreUploadiOS = AppstoreUploadiOS()



