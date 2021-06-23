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
        dirCSharp = mainResource.GetRootUnityScriptApp()
        dirTs = mainResource.GetRootUnityScriptApp()+"_Ts"
        FileUtil.CreateDir(dirTs)

  



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