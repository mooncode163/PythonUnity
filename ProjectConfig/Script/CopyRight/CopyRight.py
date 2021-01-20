import os
import shutil
import zipfile
import sys 

sys.path.append('../../') 
sys.path.append('./') 
from Project.Resource import mainResource
from Config.Config import mainConfig
from Config.AdConfig import mainAdConfig  
from Common import Source
from Common.Common import Common
from Project.Resource import mainResource 
from Common import Source
from Common.File.FileUtil import FileUtil 
from AppInfo.AppInfo import mainAppInfo
 
import json
  
# 代码行后面有// 如 public  int LINE_WIDTH_PIXSEL_MAX = 900;//  2048x1536   注释会出现下面错误：
# ValueError: All strings must be XML compatible: Unicode or ASCII, no NULL bytes or control characters

class CopyRight():
    title = "" 
    def MakeCopyRightDoc(self,isHd):
        title = mainAppInfo.GetAppName(Source.ANDROID,isHd,Source.LANGUAGE_CN)+"V1.0.0"
        codedir = "/Users/moon/sourcecode/LearnWord"
        codedir = mainResource.GetRootUnityAssets()+"/Script/Apps/"+mainResource.getGameType()
        # codedir = mainResource.GetRootUnityAssets()+"/Script/Apps/"+mainResource.getGameType()+"/Base"
        outputdir = mainResource.GetProjectOutPutApp()
        FileUtil.CreateDir(outputdir)

        docoutput = outputdir+"/"+mainResource.getGameType() +".docx"
        if isHd:
            docoutput = outputdir+"/"+mainResource.getGameType() +"_HD.docx"


        os.system("pyerz -e cs -i "+codedir+" -o "+docoutput +" -t "+title)
 
# pip3 install pyerz
# https://github.com/soultoolman/pyerz
# 主函数的实现
if __name__ == "__main__": 
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

    p = CopyRight()
    p.MakeCopyRightDoc(False)
    p.MakeCopyRightDoc(True)


    
  
     

