  

import requests  
import sys
import zipfile
import shutil
import os
import os.path 
import platform 



class Platform():  
    @staticmethod  
    def isMacSystem():
        # print(platform.system())
        return 'Darwin' in platform.system()

    @staticmethod  
    def isWindowsSystem():
        return 'Windows' in platform.system()

    @staticmethod  
    def isLinuxSystem():
        return 'Linux' in platform.system() 

    def IsVMWare(): 
        my_file =  "/Volumes/VMware Shared Folders"
        if os.path.exists(my_file):
            # 指定的目录存在
            return True
        return False
 
    