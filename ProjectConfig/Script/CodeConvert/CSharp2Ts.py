# 导入selenium的浏览器驱动接口
import sys
import os
import json
import requests
import platform  

o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径 
sys.path.append('../../') 
sys.path.append('./') 
 
from Common.Common import Common
from Project.Resource import mainResource
from Common import Source 
from Common.File.FileUtil import FileUtil 
from AppInfo.AppInfo import mainAppInfo
    
# unity c# 代码转成成cocos laya ts
class CSharp2Ts:
    def CodeCSharp2Ts(self): 
        self.CSharp2Ts("laya")
        self.CSharp2Ts("cocos")

    def CSharp2Ts(self,name): 
        dirCSharp = mainResource.GetRootUnityScriptApp()
        dirTs = mainResource.GetCodeConvert()+"_"+name
        FileUtil.CreateDir2(dirTs)
        listCSharp = []
        FileUtil.GetSubFileList(dirCSharp,"cs",listCSharp)
        for filecs in listCSharp:
            filets = filecs.replace(dirCSharp,dirTs)
            filets = filets.replace(".cs",".ts")
            uiview_ts = mainResource.GetDirProductCommonTS()+"/UIView_"+name+".ts"
            FileUtil.CreateDir2(filets)
            # FileUtil.CreateFile(filets)
            strfile = FileUtil.GetFileString(uiview_ts)
            strfile = strfile.replace("UIViewSampe",FileUtil.GetPathNameWithoutExt(filets))
            FileUtil.SaveString2File(strfile,filets)
  



# 主函数的实现
if __name__ == "__main__":
    # 设置为utf8编码
    # reload(sys)
    # sys.setdefaultencoding("utf-8")
    is_auto_plus_version = False
    # 入口参数：http://blog.csdn.net/intel80586/article/details/8545572
    cmdPath = Common.cur_file_dir()
    count = len(sys.argv)
    arg3 = ""
    arg4 = ""
    for i in range(1, count):
        print("参数", i, sys.argv[i])
        if i == 1:
            cmdPath = sys.argv[i]
        if i == 3:
            arg3 = sys.argv[i]
        if i == 4:
            arg4 = sys.argv[i]

    mainResource.SetCmdPath(cmdPath)

    p = CSharp2Ts()
    p.CodeCSharp2Ts()
 

    print("CSharp2Ts sucess")


mainCSharp2Ts = CSharp2Ts()