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
import pyautogui 

from Common.Platform import Platform

if 'Windows' in platform.system():
    import win32con
    import win32gui

class FileBrowser():  
    @staticmethod
    def OpenFile(path,isAutoClick):
        if Platform.isWindowsSystem():
            FileBrowser.OpenFileWindow(path,isAutoClick)
        if Platform.isMacSystem():
            FileBrowser.OpenFileMac(path,isAutoClick)


# mac 需要将输入法切换为英文 才能用快捷键
    @staticmethod
    def OpenFileMac(path,isAutoClick):
        test = 0
        #模拟快捷键Command+Shift+G 
        pyautogui.hotkey("Command","Shift","G")
        time.sleep(1) 
        pyautogui.typewrite(os.path.normpath(path))
        time.sleep(1)

        # if isAutoClick:
        pyautogui.press("enter")

        # cmd =  "open "+path
        # os.system(cmd)

        # os.system('open '+path)

    @staticmethod
    def OpenFileWindow(path,isAutoClick):
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
        if isAutoClick==True:
            win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button

        time.sleep(3)

 

 
 

  