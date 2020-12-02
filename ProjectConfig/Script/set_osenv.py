#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path

sys.path.append('./common')
import common
 
# 主函数的实现
if __name__ == "__main__":
    # 设置为utf8编码
    # reload(sys)
    # sys.setdefaultencoding("utf-8")

    # 入口参数：http://blog.csdn.net/intel80586/article/details/8545572
    strCmd = ""
    cmdPath = ""
    count = len(sys.argv) 

    for i in range(1, count):
        print ("参数", i, sys.argv[i])
        if i == 1:
            cmdPath = sys.argv[i]

    common.SetCmdPath(cmdPath)
    gameName = common.getGameName()
    gameType = common.getGameType()

    if common.isWindowsSystem(): 
        path=r"F:\sourcecode\unity\product"
        cmd =r"setx WORK1 %s /m"%path
        
        os.system(cmd) 
    
   

# set regpath=HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment
# set javahome=C:\Program Files\Unity\Hub\Editor\2019.3.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\OpenJDK\jre
# :aliyun  C:\Program Files\Unity\Hub\Editor\2019.3.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\OpenJDK\jre 
# :win10  C:\Program Files\Android\Android Studio\jre\jre
# rem LPY
# setx "JAVA_HOME" "%javahome%" -M
# for /f "tokens=1,* delims=:" %%a in ('reg QUERY "%regpath%" /v "path"') do (
#     set "L=%%a"
#     set "P=%%b"
# )
# set "Y=%L:~-1%:%P%"
# setx path "%%JAVA_HOME%%\bin;%Y%" -m
