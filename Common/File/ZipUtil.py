#!/usr/bin/python
# coding=utf-8
import zipfile
import shutil
import os
import sys
import os.path
import time,  datetime    
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  
from Common.Platform import Platform
class ZipUtil():  
    @staticmethod 
    def zipDir(dir_path,file_zip):   

        zipf = zipfile.ZipFile(file_zip, "w",zipfile.ZIP_DEFLATED)
        # 压缩目录
        pre_len = len(os.path.dirname(dir_path))
        for parent, dirnames, filenames in os.walk(dir_path):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                # print(pathfile) 
                arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
                if Platform.isWindowsSystem():
                    # python3
                    arcname = arcname.replace("//", "") 

                # print(arcname)
                zipf.write(pathfile, arcname)
    
        zipf.close()  

    @staticmethod 
    def get_zip_file(input_path, result):
        
        files = os.listdir(input_path)
        for file in files:
            if os.path.isdir(input_path + '/' + file):
                get_zip_file(input_path + '/' + file, result)
            else:
                result.append(input_path + '/' + file)
    
    @staticmethod 
    def zipDir2(dir_path, file_zip):
        
        f = zipfile.ZipFile(file_zip, 'w', zipfile.ZIP_DEFLATED)
        filelists = []
        get_zip_file(dir_path, filelists)
        for file in filelists:
            f.write(file)
        # 调用了close方法才会保证完成压缩
        f.close() 
    
    @staticmethod 
    def un_zip(file_zip,out_dir):
        """unzip zip file"""
        zip_file = zipfile.ZipFile(file_zip)
        if os.path.isdir(out_dir):
            pass
        else:
            os.mkdir(out_dir)
        for names in zip_file.namelist():
            zip_file.extract(names,out_dir)
        zip_file.close()


