import os  
import time  
import json 
import sys 
import platform 
import math
from PIL import Image

class ImageConvert():  
    listFile:None 
    fileJosn = "level.json" 
    dstSize = 1024

    def isWindowsSystem(self):
        return 'Windows' in platform.system()
 

   
    def GetCurPath(self):
        #获取脚本路径
        path = sys.path[0]
        #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path) 
    # 不包含. 
    def GetFileExt(self,path):  
        idx = path.rfind(".")+1
        slen=len(path)
        size = slen-idx
        ret = path[idx:]
        # print(path="+path+" idx="+str(idx)+" ret="+ret+" slen="+str(slen)
        return ret


    def GetFileName(self,path):  
        idx = path.rfind(".")
        if idx<0:
            return path

        ret = path[0:idx]
        return ret

    def GetFileNamePath(self,path): 
        str_split = '/'
        if self.isWindowsSystem():
            str_split = '\\'
        idx = path.rfind(str_split)
        s_len=len(path)
        game = path[idx+1:s_len]
        game = self.GetFileName(game)
        return game

    def ScanFiles(self,dir):
        for file in os.listdir(dir):
            # 过滤文件
            if file == "Thumbs.db":
                continue

            path = os.path.join(dir,  file)  
            if os.path.isfile(path): 
                ext = self.GetFileExt(path)
                if ext =="jpg" or ext =="jpeg":
                    name = self.GetFileNamePath(file)
                    # print(file)
                    pathnew = self.GetFileName(path)+".png"
                    # image  
                    isfilter = False
                    try: 
                        self.ImageJpgToPng(path,pathnew)
                    except Exception as e: 
                        isfilter = True
                        print("ImageJpgToPng eror=",e," file =",file)

                    if isfilter==False:
                        os.remove(path)
                

            #目录嵌套
            if os.path.isdir(path): 
                self.ScanFiles(path)
 
    def GetImage(self,path):
        img = Image.open(path)
        return img 

 
    def ImageJpgToPng(self,filein, fileout):
        img = Image.open(filein)
        img = img.convert("RGBA")
        datas = img.getdata()
        newData = list()
        for item in datas:
            if item[0] > 225 and item[1] > 225 and item[2] > 225:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData) 

        img.save(fileout, "PNG") 
        

    def JpgToPng(self): 
        self.listFile = [] 
        self.ScanFiles(self.GetCurPath()) 
        


        

  

# 主函数的实现
if __name__ == "__main__":  
    p = ImageConvert()
    p.JpgToPng()
    print("ImageConvert finish")