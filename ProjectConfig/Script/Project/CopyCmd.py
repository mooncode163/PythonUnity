#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path
import time,  datetime

#include common.py
sys.path.append('../../') 
sys.path.append('./')  
from Project.Resource import mainResource
from Common.Platform import Platform

class CopyCmd(): 
    def copyCmdFiles(self,sourceDir,  targetDir):

        #  先清除 cmd file
        for file in os.listdir(targetDir):
            targetFile = os.path.join(targetDir,  file)
            #file
            if os.path.isfile(targetFile):
                os.remove(targetFile)

        # copy
        for file in os.listdir(sourceDir): 
            sourceFile = os.path.join(sourceDir,  file)
            targetFile = os.path.join(targetDir,  file) 
            if os.path.isfile(sourceFile): 
                # copy2 同时复制文件权限
                shutil.copy2(sourceFile,targetFile) 

            

    def copyCmdDir(self,name):
        dir1 = common.GetProjectConfigDefault()+"/"+name
        dir2 = common.GetProjectConfigApp() + "/"+name
        flag = os.path.exists(dir2)
        if flag:
            shutil.rmtree(dir2)
        shutil.copytree(dir1,dir2)
        # common.coverFiles(dir1,dir2)

    def copyAllBuildDir(self):
        dir1 = common.GetProjectConfigDefault()+"/all_build"
        dir2 = common.GetProjectConfigAppType() 
        flag = os.path.exists(dir2)
        
        FileUtil.CoverFiles(dir1,dir2)

#主函数的实现
if  __name__ =="__main__":
    
    #入口参数：http://blog.csdn.net/intel80586/article/details/8545572
    print("脚本名：", sys.argv[0])
    cmdPath = common.cur_file_dir()
    count = len(sys.argv)
    for i in range(1,count):
        print ("参数", i, sys.argv[i])
        if i==1:
            cmdPath = sys.argv[i]
    
    common.SetCmdPath(cmdPath)
    gameName = common.getGameName()
    gameType = common.getGameType()
    
    print(gameType) 
    print(gameName) 
    dir1 = common.GetProjectConfigDefault()
    dir2 = common.GetProjectConfigApp()
  
    #copyCmdFiles(dir1,dir2)

    copyCmdDir("cmd_win")
    copyCmdDir("cmd_mac")
    copyAllBuildDir()

    print("copy_cmd sucess")