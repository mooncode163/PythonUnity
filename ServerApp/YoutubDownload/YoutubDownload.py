from flask import Flask 
from flask import request
import sys
app = Flask(__name__)
sys.path.append("../../") 

import requests
import platform  
import jwt 
import time
import datetime
import os
import json 
import base64
   
# http://youtu.be/rJ18V_NNq8g
# http://47.242.56.146:5001/YoutubDownload?keyid=rJ18V_NNq8g
# http://127.0.0.1:5001/YoutubDownload?keyid=rJ18V_NNq8g
@app.route('/YoutubDownload')
def YoutubDownload():
    print(request.url)
    keyid = request.args["keyid"]
    url_youtube = "http://youtu.be/"+keyid
    # pytube http://youtu.be/rJ18V_NNq8g
    # python 里无法直接执行cd目录，要用chdir改变当前的工作目录
    dirroot = "/var/www/html"
    ext = ".mp4"
    DeleteAllDownloadFile(dirroot,ext)
    os.chdir(dirroot)
    os.system("pytube "+url_youtube)
    video_file = GetDownloadFile(dirroot,ext)
    video_file = video_file.replace(dirroot+"/","")
    # http://47.242.56.146/Duo%20Painter%20-%20[UNITY%203D]%20-%20GAME%20PLAY.mp4
    # return "test"
    return video_file 
 
 
# .apk
def DeleteAllDownloadFile(sourceDir,file_ext):
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir,  file)
            #cover the files
        if os.path.isfile(sourceFile):
            # print sourceFile
            # 分割文件名与后缀
            temp_list = os.path.splitext(file)
            # name without extension
            src_apk_name = temp_list[0]
            # 后缀名，包含.   例如: ".apk "
            ext = temp_list[1]
            # apk_ext='.apk';
            if file_ext==ext:
                print(sourceFile)
                os.remove(sourceFile)
# .apk
def GetDownloadFile(sourceDir,file_ext):
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir,  file)
            #cover the files
        if os.path.isfile(sourceFile):
            # print sourceFile
            # 分割文件名与后缀
            temp_list = os.path.splitext(file)
            # name without extension
            src_apk_name = temp_list[0]
            # 后缀名，包含.   例如: ".apk "
            ext = temp_list[1] 
            if file_ext==ext:
                print(sourceFile)
                return sourceFile

    return ""
if __name__ == '__main__': 
    # app.run()

    # 5000
    app.run(host='0.0.0.0', port=5001)