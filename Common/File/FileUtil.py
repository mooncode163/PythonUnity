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
  

from xml.dom.minidom import parse
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  
from Common.Platform import Platform
 
class FileUtil():  
   
    @staticmethod   
    def CopyDir(src,dst,isRemove=True): 
        flag = os.path.exists(dst)
        if flag:
            if isRemove:
                shutil.rmtree(dst)
        shutil.copytree(src,dst)

    @staticmethod  
    def CopyFile(src,  dst):
        if os.path.isfile(src):
            shutil.copyfile(src,dst)

     # 复制单个文件
    @staticmethod  
    def CopyOneFile(sourceFile,  targetFile):
        if os.path.isfile(sourceFile):
            # shutil.copyfile(src,dst)
            open(targetFile, "wb").write(open(sourceFile, "rb").read())
            
    #把某一目录下的所有文件复制到指定目录中
    @staticmethod 
    def CopyFiles(sourceDir,  targetDir):
        if sourceDir.find(".svn") > 0:
            return
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,  file)
            targetFile = os.path.join(targetDir,  file)
            if os.path.isfile(sourceFile):
                if not os.path.exists(targetDir):
                    os.makedirs(targetDir)
                if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                    open(targetFile, "wb").write(open(sourceFile, "rb").read())
    #    if os.path.isdir(sourceFile):
    #        First_Directory = False
    #        copyFiles(sourceFile, targetFile)

    #复制一级目录下的所有文件到指定目录：
    @staticmethod 
    def CoverFiles(sourceDir,  targetDir):
        for file in os.listdir(sourceDir):
            # 过滤文件
            if file == "Thumbs.db":
                continue

            sourceFile = os.path.join(sourceDir,  file)
            # sourceFile= os.path.normpath(sourceFile)
            targetFile = os.path.join(targetDir,  file)
            # targetFile= os.path.normpath(targetFile)
                #cover the files
            if os.path.isfile(sourceFile):
                
                # open(targetFile, "wb").write(open(sourceFile, "rb").read())
                
                # flag = os.path.exists(targetFile)
                # if flag:
                #     os.remove(targetFile)
                dir = FileUtil.GetLastDirofDir(targetFile)
                if os.path.exists(dir)==False:
                    os.mkdir(dir)

                shutil.copyfile(sourceFile, targetFile)

            #目录嵌套
            if os.path.isdir(sourceFile):
                print(sourceFile)
                print(targetFile)
                FileUtil.CoverFiles(sourceFile,targetFile)



# 获取子目录列表
    @staticmethod 
    def GetSubDirList(sourceDir,listdir):
        for file in os.listdir(sourceDir):
            # 过滤文件
            if file == "Thumbs.db":
                continue

            sourceFile = os.path.join(sourceDir,  file)
            #目录嵌套
            if os.path.isdir(sourceFile):
                print(sourceFile)
                listdir.append(sourceFile)


# 获取子目录文件列表
    @staticmethod 
    def GetSubFileList(sourceDir,ext,listfile):
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,  file)
                #cover the files
            if os.path.isfile(sourceFile):
                # print sourceFile
                # 分割文件名与后缀
                temp_list = os.path.splitext(file)
                # name without extension
                name = temp_list[0]
                # 后缀名，包含.   例如: ".apk "
                ext_file = temp_list[1] 
                ext_file = ext_file[1:]
                if ext==ext_file:
                    print(sourceFile)
                    listfile.append(sourceFile)

            #目录嵌套
            if os.path.isdir(sourceFile):
                # print sourceFile
                FileUtil.GetSubFileList(sourceFile,ext,listfile)
 

    #删除一级目录下的所有文件：
    @staticmethod 
    def RemoveFileInFirstDir(targetDir):
        for file in os.listdir(targetDir):
            targetFile = os.path.join(targetDir,  file)
            if os.path.isfile(targetFile):
                os.remove(targetFile)
    
    # 复制单个文件
    @staticmethod 
    def CopyOneFile(sourceFile,  targetFile):
            if os.path.isfile(sourceFile):
                open(targetFile, "wb").write(open(sourceFile, "rb").read())

    @staticmethod 
    def SaveString2File(str, file):
        f = open(file, 'wb')  # 若是'wb'就表示写二进制文件
        b = str.encode('utf-8',"ignore")
        f.write(b)
        f.close()

    @staticmethod 
    def SaveByte2File(b, file):
        f = open(file, 'wb')  # 若是'wb'就表示写二进制文件 
        f.write(b)
        f.close()

    @staticmethod 
    def GetFileString(filePath): 
        f = open(filePath, 'rb')
        strFile = f.read().decode('utf-8',"ignore")
        f.close()
        return strFile

 #last dir
    @staticmethod 
    def GetLastDir(): 
        return GetLastDirofDir(cur_file_dir())

    @staticmethod 
    def GetLastDirofDir(path): 
        str_split = '/'
        if Platform.isWindowsSystem():
            str_split = '\\'
        idx = path.rfind(str_split)

        ret = path[0:idx]
        return ret

    def GetDirOfPath(path): 
        str_split = '/'
        if Platform.isWindowsSystem():
            str_split = '\\'
        idx = path.rfind(str_split)

        ret = path[0:idx]
        return ret

    # 不包含.
    @staticmethod 
    def GetFileExt(path):  
        idx = path.rfind(".")
        if idx<0:
            return ""
        idx=idx+1 
        ret = path[idx:]
        # print(path="+path+" idx="+str(idx)+" ret="+ret+" slen="+str(slen)
        return ret
        
    @staticmethod 
    def GetFileName(path):  
        idx = path.rfind(".")
        if idx<0:
            return path
        ret = path[0:idx]
        return ret

    @staticmethod 
    def GetPathNameWithExt(path):  
        idx = path.rfind("/")
        if idx<0:
            idx = path.rfind("\\")

        if idx<0:
            return path
        ret = path[(idx+1):]
        return ret

    @staticmethod 
    def GetPathNameWithoutExt(path):   
        return FileUtil.GetFileName(FileUtil.GetPathNameWithExt(path))

    @staticmethod 
    def GetPathName():
        return GetDirNameofPath(getLastDir())

    @staticmethod 
    def GetDirNameofPath(path): 
        str_split = '/'
        if Platform.isWindowsSystem():
            str_split = '\\'
        idx = path.rfind(str_split)
        s_len=len(path)
        game = path[idx+1:s_len]
        return game

    @staticmethod 
    def CreateDir(dir): 
        if os.path.exists(dir)==False:
            os.mkdir(dir)


     # 复制单个文件
    @staticmethod  
    def CreateFile(sourceFile): 
            open(sourceFile, "w").write("")
            

    @staticmethod 
    #  循环创建
    def CreateDir2(dir): 
        dirlast = FileUtil.GetDirOfPath(dir)
        listdir = []
        while(True):
            if os.path.exists(dirlast)==False:
                # print("dirlast=",dirlast)
                listdir.insert(0,dirlast)
                dirlast = FileUtil.GetDirOfPath(dirlast)
            else:
                break
        
        ext = FileUtil.GetFileExt(dir)
        # print("CreateDir2 ext=",ext)
        if len(ext)==0:
            listdir.append(dir)

        for dirtmp in listdir:
            if os.path.exists(dirtmp)==False:
                os.mkdir(dirtmp)

    @staticmethod 
    def RemoveDir(dir): 
        if os.path.exists(dir)==True:
            shutil.rmtree(dir)

    @staticmethod 
    def RemoveFile(filePath): 
        if os.path.exists(filePath)==True:
            os.remove(filePath)

  