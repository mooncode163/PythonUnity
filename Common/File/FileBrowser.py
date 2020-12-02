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
import platform 

from Common.Platform import Platform

if 'Windows' in platform.system():
    import win32con
    import win32gui

class FileBrowser():  
    @staticmethod
    def OpenFile(path,autoclick):
        # win32gui
        dialog = win32gui.FindWindow('#32770', u'打开')  # 对话框
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
        ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
        # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
        Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)
        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button
        win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, os.path.normpath(path))
        # win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, "F:\\sourcecode\\unity\\product\\kidsgame\\ProjectOutPut\\xiehanzi\\hanziyuan\\screenshot\\shu\\cn\\480p\\1.jpg")
        # win32gui.SendMessage(Edit,win32con.WM_SETTEXT,None,'F:\sourcecode\unity\product\kidsgame\ProjectOutPut\xiehanzi\hanziyuan\screenshot\shu\cn\480p\1.jpg')  # 往输入框输入绝对地址
        if autoclick==True:
            win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button

        time.sleep(3)

 

 
 

  