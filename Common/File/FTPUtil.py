#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path
import json
 
from ftplib import FTP
import time,tarfile,os
# import paramiko

# ubuntu 安装 vsftpd
# sudo apt-get install vsftpd
# FileZilla连接 选择sftp协议 vsftpd 的端口选22
 
# 添加vsftpd 登录用户
#新建文件/etc/vsftpd.user_list，用于存放允许访问ftp的用户：
# sudo touch /etc/vsftpd.user_list 
# sudo vim /etc/vsftpd.user_list 
# 在/etc/vsftpd.user_list中添加允许登录ftp 的用户
# root
 

# https://blog.csdn.net/qq_39122146/article/details/103907247




class FTPUtil():   
    #连接ftp
    def ftpconnect(self,host,port, username, password):
        ftp = FTP()
        # 打开调试级别2，显示详细信息
        # ftp.set_debuglevel(2)
        ftp.connect(host, port)
        ftp.login(username, password)
        return ftp

    #从ftp下载文件
    def downloadfile(self,ftp, remotepath, localpath):
        # 设置的缓冲区大小
        bufsize = 1024
        fp = open(localpath, 'wb')
        ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
        ftp.set_debuglevel(0)# 参数为0，关闭调试模式
        fp.close()

    #从本地上传文件到ftp
    def uploadfile(self,ftp, remotepath, localpath):
        bufsize = 1024
        fp = open(localpath, 'rb')
        ftp.storbinary('STOR ' + remotepath, fp, bufsize)
        ftp.set_debuglevel(0)
        fp.close()

mainFTPUtil = FTPUtil() 

if __name__ == "__main__":
    #host,port, username, password
    p =  FTPUtil()
    # ftp = p.ftpconnect("47.242.56.146", 21,"root", "Qianlizhiwai1")
    # #下载文件，第一个是ftp服务器路径下的文件，第二个是要下载到本地的路径文件
    # p.downloadfile(ftp, "/12.mp3", r"C:\Users\Administrator\Desktop\ftp\download\test.mp3")
    # # 上传文件，第一个是要上传到ftp服务器路径下的文件，第二个是本地要上传的的路径文件
    # p.uploadfile(ftp, '/upload/1.txt', "C:/Users/Administrator/Desktop/1.txt")
    # # ftp.close() #关闭ftp
    # # #调用本地播放器播放下载的视频
    # # os.system('start D:\soft\kugou\KGMusic\KuGou.exe C:\Users\Administrator\Desktop\ftp\test.mp3')

    # print(ftp.getwelcome())# 打印出欢迎信息
    # # 获取当前路径
    # pwd_path = ftp.pwd()
    # print("FTP当前路径:", pwd_path)
    # 显示目录下所有目录信息
    # ftp.dir()
    # 设置FTP当前操作的路径
    # ftp.cwd('/upload/')
    # # 返回一个文件名列表
    # filename_list = ftp.nlst()
    # print(filename_list)

    # ftp.mkd('目录名')# 新建远程目录
    # ftp.rmd('目录名')  # 删除远程目录
    # ftp.delete('文件名')  # 删除远程文件
    # ftp.rename('fromname', 'toname')  # 将fromname修改名称为toname

    # 逐行读取ftp文本文件
    file = '/upload/1.txt'
    # ftp.retrlines('RETR %s' % file)
    #与 retrlines()类似，只是这个指令处理二进制文件。回调函数 cb 用于处理每一块（块大小默认为 8KB）下载的数据
    # ftp.retrbinary('RETR %s' % file)


    
    
    # transport = paramiko.Transport(("47.242.56.146", 21))    # 获取Transport实例
    # transport.connect(username="root", password="Qianlizhiwai1")    # 建立连接
    
    # # 创建sftp对象，SFTPClient是定义怎么传输文件、怎么交互文件
    # sftp = paramiko.SFTPClient.from_transport(transport)
    
    # # 将本地 api.py 上传至服务器 /www/test.py。文件上传并重命名为test.py
    # sftp.put("E:/test/api.py", "/www/test.py")
    
    # # 将服务器 /www/test.py 下载到本地 aaa.py。文件下载并重命名为aaa.py
    # sftp.get("/www/test.py", "E:/test/aaa.py")
    
    # # 关闭连接
    # transport.close()

 
 