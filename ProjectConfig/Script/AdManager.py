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
# 当前工作目录 Common/PythonCreator/ProjectConfig/Script
sys.path.append('../../') 
sys.path.append('./')  

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

from AppInfo.AppInfo import mainAppInfo

from Ad.AdBaidu import mainAdBaidu
from Ad.AdGdt import mainAdGdt

class AdManager():   
    #构造函数
    def __init__(self): 
        name =""
    
    def GetAd(self,channel):
        print("GetAd channel=",channel)
        if channel == Source.BAIDU:
            return mainAdBaidu
        if channel == Source.GDT:
            return mainAdGdt
 
    def GetXcodePrefile(self): 
        mainAdBaidu.RunDownloadSigniOS()
   
   
         
                         

# 主函数的实现
if __name__ == "__main__": 
    # 入口参数：http://blog.csdn.net/intel80586/article/details/8545572
    cmdPath = Common.cur_file_dir()
    count = len(sys.argv)
    arg2 = ""
    arg3 = ""
    arg4 = ""
    arg5 = ""
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
        if i==5:
            arg5 = sys.argv[i]

    isHd = False
    if arg5 =="hd":
        isHd = True
    print("AdManager __main__ arg4=",arg4)

    mainResource.SetCmdPath(cmdPath)
    # createapp android baidu 
    # createplaceid android gdt
    # adinfo android gdt
    p = AdManager() 

    if arg2 == "createapp": 
        p.GetAd(arg4).Run(arg2,arg3,isHd)
 
    if arg2 == "createplaceid": 
        p.GetAd(arg4).Run(arg2,arg3,isHd)

    if arg2 == "adinfo": 
        p.GetAd(arg4).Run(arg2,arg3,isHd)

    if arg2 == "GetXcodePrefile": 
        p.GetXcodePrefile()
        

    print("AdManager sucess arg=",arg2)
