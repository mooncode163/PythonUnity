#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path
import time
import datetime
import json

#include common.py
#  
o_path = os.getcwd()  # 返回当前工作目录
print(o_path)
# sys.path.append(o_path)  # 添加自己指定的搜索路径
# 当前工作目录 Common/PythonUnity/ProjectConfig/Script
sys.path.append('../../') 
# sys.path.append('./')  

dir = os.path.abspath(__file__)
print(dir)
dir = os.path.dirname(dir)
print(dir) 
# sys.path.append("..") #把上级目录加入到变量中
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  


from Common.Common import Common
from Project.Resource import mainResource 

# from Config import config
from Common import Source
# from Config import adconfig  
from Common.File.FileUtil import FileUtil    

from AppInfo.AppInfo import mainAppInfo

from AppStore.AppStoreHuawei import mainAppStoreHuawei
from AppStore.AppStoreTaptap import mainAppStoreTaptap
from AppStore.AppStoreGoogle import mainAppStoreGoogle
from AppStore.AppStoreApple import mainAppStoreApple
from AppStore.AsoQimai import mainAsoQimai
from AppStore.AsoDeep import mainAsoDeep

class AppStoreManager():   
    #构造函数
    def __init__(self): 
        name =""
    
    def GetAppStore(self,channel):
        print("GetAppStore channel=",channel)
        if channel == Source.HUAWEI:
            return mainAppStoreHuawei
        if channel == Source.TAPTAP:
            return mainAppStoreTaptap
        if channel == Source.GP:
            return mainAppStoreGoogle
        if channel == Source.APPSTORE:
            print("GetAppStore mainAppStoreApple=")
            return mainAppStoreApple
  
         
                         

# 主函数的实现
if __name__ == "__main__": 
    # 入口参数：http://blog.csdn.net/intel80586/article/details/8545572
    cmdPath = Common.cur_file_dir()
    count = len(sys.argv)
    arg2 = ""
    arg3 = ""
    arg4 = ""
    for i in range(1,count):
        print("参数", i, sys.argv[i])
        if i==1:
            cmdPath = sys.argv[i] 
        if i==2:
            arg2 = sys.argv[i]
        if i==3:
            arg3 = sys.argv[i]
        if i==4:
            arg4 = sys.argv[i]


    isHd = False
    if arg4 =="hd":
        isHd = True

    mainResource.SetCmdPath(cmdPath)
    
    p = AppStoreManager() 

    if arg2 == "createapp":
        print("createapp arg4=",arg4," isHd=",isHd)
        # python AppStoreManager.py %~dp0 createapp huawei hd
        # p.CreateApp(arg2,arg3,arg4)
        p.GetAppStore(arg3).Run(arg2,isHd)

    if arg2 == "new_version":
        # python AppStoreManager.py %~dp0 createapp huawei hd
        # p.CreateApp(arg2,arg3,arg4)
        p.GetAppStore(arg3).Run(arg2,isHd)

    if arg2 == "UploadScreenShot":
        p.GetAppStore(arg3).Run(arg2,isHd)

    if arg2 == "CreateBundleID":
        print("AppStoreManager CreateBundleID")
        p.GetAppStore(arg3).Run(arg2,isHd)
 
    if arg2 == "DownloadProfile": 
        p.GetAppStore(arg3).Run(arg2,isHd)

    if arg2 == "DeleteAllScreenShot":
        p.GetAppStore(arg3).Run(arg2,isHd)
        

    if arg2 == "UpdateAppInfo":
        p.GetAppStore(arg3).Run(arg2,isHd)

    if arg2 == "UpdateIAPInfo":
        p.GetAppStore(arg3).Run(arg2,isHd)

    if arg2 == "DeleteAllLanguage":
        p.GetAppStore(arg3).Run(arg2,isHd) 

    if arg2 == "update":
        # python AppStoreManager.py %~dp0 createapp huawei hd
        # p.UpdateApp(arg2,arg3,arg4)
        p.GetAppStore(arg3).Run(arg2,isHd)

    if arg2 == "SubmitApp": 
        p.GetAppStore(arg3).Run(arg2,isHd)

    if arg2 == "UpdateVersion": 
        p.GetAppStore(arg3).Run(arg2,isHd) 
        
    if arg2 == "getappid":
        # python AppStoreManager.py %~dp0 createapp huawei hd
        # p.GetAppid(arg2,arg3)
        p.GetAppStore(arg3).Run(arg2,isHd)

    if arg2 == "AsoQimai": 
        isHd = False
        if arg3 =="hd":
            isHd = True
        mainAsoQimai.Run(isHd)

    if arg2 == "AsoDeep": 
        isHd = False
        if arg3 =="hd":
            isHd = True
        mainAsoDeep.Run(isHd)


    print("AppStoreManager sucess arg=",arg2)
