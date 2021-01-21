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
# 


# @moon fix bugs
# https://github.com/soultoolman/pyerz
# 手动copy 到 /Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/pyerz
# 代码行后面有// 如 public  int LINE_WIDTH_PIXSEL_MAX = 900;//  2048x1536   注释会出现下面错误：
# ValueError: All strings must be XML compatible: Unicode or ASCII, no NULL bytes or control characters



class CopyRight():
    title = "" 
    def MakeCodeDoc(self,isHd):
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

        self.WordToPdf(docoutput)
    
    def MakeGuideDoc(self,isHd): 
        title = mainAppInfo.GetAppName(Source.ANDROID,isHd,Source.LANGUAGE_CN)+"V1.0.0"
        outputdir = mainResource.GetProjectOutPutApp()
        FileUtil.CreateDir(outputdir)

        docoutput = outputdir+"/"+mainResource.getGameType() +"_guide.docx"
        dirscreenshot = mainResource.GetProjectOutPutApp()+"/screenshot/shu/cn/1080p"
        filedetail = mainResource.GetProjectConfigApp()+"/appinfo/app_description.xml"
        if isHd:
            dirscreenshot = mainResource.GetProjectOutPutApp()+"/screenshot/heng/cn/1080p"
            filedetail = mainResource.GetProjectConfigApp()+"/appinfo/app_description_hd.xml"
            docoutput = outputdir+"/"+mainResource.getGameType() +"_guide_hd.docx"

        
        filedst = dirscreenshot+"/detail.xml"
        FileUtil.CopyFile(filedetail,filedst) 
        cmd = "pyerz -e xml -i "+dirscreenshot+" -o "+docoutput +" -t "+title
        # print("cmd=",cmd)
        for i in range(5):
            pic = dirscreenshot+"/"+str(i+1)+".jpg"
            if os.path.exists(pic):
                cmd +=  " -pic "+pic

        os.system(cmd)


        os.remove(filedst)

        self.WordToPdf(docoutput)


# mac word 转pdf 工具 libreoffice
# https://sspai.com/post/44140
# https://www.libreoffice.org/
    def WordToPdf(self,worddoc):
        filepdf = worddoc.replace(".docx",".pdf") 
        cmd = "soffice --convert-to pdf "+worddoc
        # os.system(cmd)

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
    p.MakeCodeDoc(False)
    p.MakeCodeDoc(True)

    p.MakeGuideDoc(False)
    p.MakeGuideDoc(True)



    
  
     

