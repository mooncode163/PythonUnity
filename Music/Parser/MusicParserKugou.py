# 导入selenium的浏览器驱动接口


import sys
import os
import json
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径



from Common.WebDriver.WebDriverCmd import WebDriverCmd
from selenium import webdriver
from Common.Common import Common
import pyperclip
from Common.WebDriver.WebDriverCmd import CmdInfo
from Common.WebDriver.WebDriverCmd import CmdType
from MusicParserBase import MusicParserBase
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from Music.Data.DBMusic import mainDBMusic
from Music.Data.DBMusic import DBMusic
from Music.Data.MusicInfo import MusicInfo

from Common.File.FileDownload import mainFileDownload

import time
import sqlite3 

# 要想调用键盘按键操作需要引入keys包

# 导入chrome选项


# pip3 install pywin32

# sys.path.append('../common')

# 酷狗音乐web端API接口数据
# https://github.com/ecitlm/Kugou-api
# https://blog.csdn.net/qq_38622264/article/details/80271136?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase
# https://blog.csdn.net/sinat_27938829/article/details/85951865?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.nonecase
# https://blog.csdn.net/likaibk/article/details/53008820
class MusicParserKugou(MusicParserBase):

    defaultLanguage = "美式英语"

    def Login(self, user, password):
        # 3452644866
        print("waiting for login")
        while True:
            time.sleep(1)
            self.urlnew = self.driver.current_url
            if self.urlnew != self.urlold:
                break

        return
        # driver.add_cookie("[{'domain': '.id1.cloud.huawei.com', 'expiry': 1908869785, 'httpOnly': False, 'name': 'sid', 'path': '/', 'secure': True, 'value': '2049382e3828ef4470bef8b426c4bb3370e7d9e1147f53a18839e47dad7caf10a233e61ee15337b4373e'}, {'domain': '.id1.cloud.huawei.com', 'expiry': 1908869785, 'httpOnly': False, 'name': 'hwid_cas_sid', 'path': '/', 'secure': True, 'value': '2049382e3828ef4470bef8b426c4bb3370e7d9e1147f53a18839e47dad7caf10a233e61ee15337b4373e'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_idts_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1593336984125'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_id_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': 'cf787be41ac24d65887dcd20c826ac97'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_idvc_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1593338788, 'httpOnly': False, 'name': 'HW_idn_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': 'ec569450f0ac4cd78fc72965d91ec7e8'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1608888984, 'httpOnly': False, 'name': 'HW_refts_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1593336984124'}, {'domain': '.id1.cloud.huawei.com', 'httpOnly': True, 'name': 'CAS_THEME_NAME', 'path': '/', 'secure': True, 'value': 'red'}, {'domain': 'id1.cloud.huawei.com', 'httpOnly': False, 'name': 'cookieBannerOnOff', 'path': '/', 'secure': False, 'value': 'true'}, {'domain': '.id1.cloud.huawei.com', 'httpOnly': True, 'name': 'VERSION_NO', 'path': '/', 'secure': True, 'value': 'UP_CAS_4.0.4.100'}, {'domain': 'id1.cloud.huawei.com', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/CAS', 'secure': True, 'value': '144E8B2ED3F5D9C8576742C1DDF4CF3D0DCF6949E13D6943'}]")

        item = self.driver.find_element(
            By.XPATH, "//input[@id='u']")
        item.send_keys(user)

        item = self.driver.find_element(By.XPATH, "//input[@id='p']")
        item.send_keys(password)

        item = self.driver.find_element(
            By.XPATH, "//input[@id='login_button']")
        item.click()
        time.sleep(5)

        # cookie = self.driver.get_cookies()
        # print(cookie)
        # [{'domain': '.id1.cloud.huawei.com', 'expiry': 1908869785, 'httpOnly': False, 'name': 'sid', 'path': '/', 'secure': True, 'value': '2049382e3828ef4470bef8b426c4bb3370e7d9e1147f53a18839e47dad7caf10a233e61ee15337b4373e'}, {'domain': '.id1.cloud.huawei.com', 'expiry': 1908869785, 'httpOnly': False, 'name': 'hwid_cas_sid', 'path': '/', 'secure': True, 'value': '2049382e3828ef4470bef8b426c4bb3370e7d9e1147f53a18839e47dad7caf10a233e61ee15337b4373e'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_idts_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1593336984125'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_id_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': 'cf787be41ac24d65887dcd20c826ac97'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1624872984, 'httpOnly': False, 'name': 'HW_idvc_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1593338788, 'httpOnly': False, 'name': 'HW_idn_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': 'ec569450f0ac4cd78fc72965d91ec7e8'}, {'domain': 'id1.cloud.huawei.com', 'expiry': 1608888984, 'httpOnly': False, 'name': 'HW_refts_id1_cloud_huawei_com_id1_cloud_huawei_com', 'path': '/', 'secure': False, 'value': '1593336984124'}, {'domain': '.id1.cloud.huawei.com', 'httpOnly': True, 'name': 'CAS_THEME_NAME', 'path': '/', 'secure': True, 'value': 'red'}, {'domain': 'id1.cloud.huawei.com', 'httpOnly': False, 'name': 'cookieBannerOnOff', 'path': '/', 'secure': False, 'value': 'true'}, {'domain': '.id1.cloud.huawei.com', 'httpOnly': True, 'name': 'VERSION_NO', 'path': '/', 'secure': True, 'value': 'UP_CAS_4.0.4.100'}, {'domain': 'id1.cloud.huawei.com', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/CAS', 'secure': True, 'value': '144E8B2ED3F5D9C8576742C1DDF4CF3D0DCF6949E13D6943'}]

    def Search(self, word):
        print(word)
        url = "https://www.kugou.com/yy/html/search.html#searchType=song&searchKeyWord="+word
        self.driver.get(url)
        time.sleep(1) 
        webcmd = WebDriverCmd(self.driver)

        key = "//div[@class='song_list']"
        div = webcmd.Find(key,True)
        key = ".//ul/li"
        list = webcmd.FindListChild(div,key) 
        print("Search len=",len(list))
        for li in list:
            key = ".//a[@class='song_name']" 
            if webcmd.IsElementChildExist(li,key):
                a = webcmd.FindChild(li,key)
                
                title =a.get_attribute('title')
                href =a.get_attribute('href')
                print(title)
                print(href) 
                # a.click()
                action= ActionChains(self.driver)
                action.click(a).perform()
                self.ParseMusicInfoWebCmd()

            
            

        

    def ParseBoardMusicList(self):
        url = "https://www.kugou.com/yy/rank/home/1-6666.html?from=rank"
        self.driver.get(url)
        time.sleep(1) 
        webcmd = WebDriverCmd(self.driver)

        key = "//div[@class='pc_temp_songlist']"
        div = webcmd.Find(key,True)        
        key = ".//ul/li"
        list = webcmd.FindListChild(div,key) 
        print("ParseMusicBoardList len=",len(list))
        for li in list:
            key = ".//a[@data-active='playDwn']"
            a = webcmd.FindChild(li,key) 
            title =a.get_attribute('title')
            href =a.get_attribute('href')
            print(title)
            print(href) 
 
    def ParseMusicBoardList(self):
        url = "https://www.kugou.com/yy/html/rank.html?from=homepage"
        self.driver.get(url)
        time.sleep(1) 
        webcmd = WebDriverCmd(self.driver)

        key = "//div[@class='pc_temp_side']"
        div = webcmd.Find(key,True)        
        key = ".//ul/li/a"
        list = webcmd.FindListChild(div,key) 
        print("ParseMusicBoardList len=",len(list))
        for a in list:
            title =a.get_attribute('title')
            href =a.get_attribute('href')
            print(title)
            print(href) 

# https://webfs.yun.kugou.com/202007241652/120b77e516c45ae7d4a2bd352fdcdc30/part/0/969372/G192/M0B/0D/03/oJQEAF5lgzeAE2HVAEkf7hp8OCI301.mp3
    def ParseMusicInfoWebCmd(self):
   
        webcmd = WebDriverCmd(self.driver)
        
        # 跳转到新的页面 
        time.sleep(1)
        
        old_window = self.driver.current_window_handle
        key = "//audio[@id='myAudio']"
        if webcmd.IsElementExist(key)==False:
            while True:
                time.sleep(1)
                
                for win in self.driver.window_handles:
                    if win != old_window:
                        self.driver.switch_to.window(win)
                        old_window = self.driver.current_window_handle

                    print("self.driver.current_url 2=", self.driver.current_url) 

                if webcmd.IsElementExist(key):  
                    break

        info = MusicInfo()
        key = "//audio[@id='myAudio']"
        item = webcmd.Find(key,True) 
        audio =item.get_attribute('src')
        info.url = audio
        print(audio)
        mainFileDownload.Download(info.url,"OutPut/1.mp3")

        # play
        key = "//a[@id='toggle']"
        webcmd.AddCmd(CmdType.CLICK_Action,key,1)
        # webcmd.Run(True)
        
        # title
        key = "//span[@class='audioName']"
        span = webcmd.Find(key)
        title =span.get_attribute('title')
        print(title)
        info.title = title

        # artist
        key = "//p[@class='singerName fl']"
        item = webcmd.Find(key,False) 
        key = ".//a"
        a = webcmd.FindChild(item,key)
        title =a.get_attribute('title')
        href =a.get_attribute('href')
        print(title)
        print(href)
        info.artist = title

        # album
        key = "//p[@class='albumName fl']"
        item = webcmd.Find(key,False) 
        key = ".//a"
        a = webcmd.FindChild(item,key)
        title =a.get_attribute('title')
        href =a.get_attribute('href')
        print(title)
        print(href)
        info.album = title

        # 专辑封面
        key = "//div[@class='albumImg']"
        div = webcmd.Find(key) 
        key = ".//img"
        img = webcmd.FindChild(div,key)
        pic =img.get_attribute('src')
        print(pic)
        info.pic = pic
        
        # 歌词
        key = "//div[@class='songWordContent songWordContentM jspScrollable']"
        if webcmd.IsElementExist(key):
            div = webcmd.Find(key)
            webcmd.SetItemVisible(div,1)
            key = ".//p[@class='ie8FontColor']"
            list = webcmd.FindListChild(div,key)
            print("len=",len(list))
            for p in list:
                title = p.text
                if len(title)>0:
                    print(title)

        
        mainDBMusic.AddItem(info)
        db = DBMusic()


    def ParseMusicInfo(self, url):
        print(url)
        self.driver.get(url)
        time.sleep(1)

        self.ParseMusicInfoWebCmd()

# 主函数的实现
if __name__ == "__main__":
    # 设置为utf8编码
    # reload(sys)
    # sys.setdefaultencoding("utf-8")

    # 入口参数：http://blog.csdn.net/intel80586/article/details/8545572
    cmdPath = Common.cur_file_dir()
    count = len(sys.argv)

    isHD = False
    for i in range(1, count):
        print("参数", i, sys.argv[i])
        if i == 1:
            cmdPath = sys.argv[i]

        if i == 3:
            if sys.argv[i] == "hd":
                isHD = True

    # cmdPath = cmdPath.replace("ad\\", "")

    # dir = FileUtil.GetLastDirofDir(cmdPath)
    # # dir = FileUtil.GetLastDirofDir(dir)
    # common.SetCmdPath(dir)

    p = MusicParserKugou()
    p.SetCmdPath(cmdPath)
    p.Init()

    # argv1 = sys.argv[2]
    # ad.osApp = sys.argv[3]
    # if argv1 == "createapp":
    #     ad.ParseMusicInfo(isHD)
    #     time.sleep(3)
    #     # ad.CreateApp(True)
    # p.ParseMusicBoardList()
    p.ParseMusicInfo("https://www.kugou.com/song/#hash=9378D50A6E94724FE1D31389A17ABDC6&album_id=973606")
    # p.Search("征服")
    # p.Search("周杰伦")
    
    # ad.Quit(300)

    print("AppStoreHuawei sucess")
