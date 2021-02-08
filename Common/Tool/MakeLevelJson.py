import os  
import time  
import json 
import sys 
import platform 
import math
# from PIL import Image

class MakeLevelJson():  
    listFile:None 
    fileJosn = "level.json" 
    dstSize = 1024

    def isWindowsSystem(self):
        return 'Windows' in platform.system()

    def SaveString2File(self,str, file):
        f = open(file, 'wb')  # 若是'wb'就表示写二进制文件
        b = str.encode('utf-8',"ignore")
        f.write(b)
        f.close()

    def GetFileString(self,filePath): 
        f = open(filePath, 'rb')
        strFile = f.read().decode('utf-8',"ignore")
        f.close()
        return strFile

    def LoadJson(self):
        self.listWord = []
        if os.path.exists(self.fileJosn)==False:
            return

        strjson = self.GetFileString(self.fileJosn)
        dataRoot = json.loads(strjson)
        dataItems = dataRoot["items"]
        for item in dataItems: 
            info = WordInfo()
            info.title=item["title"]
            info.detail=item["detail"]
            info.index=item["index"]
            info.page=item["page"]
            self.listWord.append(info)

    def Save(self,filepath):
        dataRoot = json.loads("{}")
        dataItems = []
        for name in self.listFile:
            item= json.loads("{}")
            item["id"]=name
            dataItems.append(item)
        dataRoot["items"]=dataItems
        
        json_str = json.dumps(dataRoot,ensure_ascii=False,indent=4,sort_keys = True)
        self.SaveString2File(json_str,filepath)
        return False

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
        idx_dot = path.rfind(".")
        if idx_dot<0:
            return ""
        else:
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

    def RenameFiles(self,dir):
        for file in os.listdir(dir):
            # 过滤文件
            if file == "Thumbs.db":
                continue

            path = os.path.join(dir,  file)  
            if os.path.isfile(path): 
                ext = self.GetFileExt(path)
                if ext=="png" or ext =="jpg" or ext =="jpeg":
                    # 咩咩素材-植物线稿 (1)
                    path_new = path.replace("咩咩素材-植物线稿 (","")
                    path_new = path_new.replace(")","")
                    os.rename(path, path_new)   

            #目录嵌套
            if os.path.isdir(path): 
                self.RenameFiles(path)


    def ScanFiles(self,dir):
        for file in os.listdir(dir):
            # 过滤文件
            if file == "Thumbs.db":
                continue

            path = os.path.join(dir,  file)  
            if os.path.isfile(path): 
                ext = self.GetFileExt(path)
                if ext=="png" or ext =="jpg" or ext =="jpeg":

                    
                    name = self.GetFileNamePath(file)
                    # print(file)
                    
                    # image 
                    # img = self.GetImage(path)
                    # w = img.width
                    # h = img.height
                    # tosize = self.dstSize
                    # if w>h:
                    #     w_new =tosize
                    #     h_new =(int)(h*w_new/w)
                    # else:
                    #     h_new =tosize
                    #     w_new = (int)(w*h_new/h)

                    isfilter = False

                    # type = ext
                    # if type =="jpg":
                    #     type = "jpeg"

                    # if w>tosize or h>tosize:
                    #     print("ResizeImage file =",file)
                    #     try: 
                    #         self.ResizeImage(path,path,w_new,h_new,type)
                    #     except Exception as e: 
                    #         isfilter = True
                    #         print("ResizeImage eror=",e," file =",file)
                            
                    if isfilter==False:
                        self.listFile.append(name)

            #目录嵌套
            if os.path.isdir(path): 
                self.ScanFiles(path)
 
    def GetImage(self,path):
        img = Image.open(path)
        return img 

    # '''
    # filein: 输入图片
    # fileout: 输出图片
    # width: 输出图片宽度
    # height:输出图片高度
    # type:输出图片类型（png, gif, jpeg...） type = 'png'
    # '''
    def ResizeImage(self,filein, fileout, width, height, type):
        img = Image.open(filein)
        out = img.resize((width, height),Image.ANTIALIAS) #resize image with high-quality
        out.save(fileout, type) 

    def Run(self): 
        self.listFile = []
        self.fileJosn = "item_"+self.GetFileNamePath(self.GetCurPath())+".json"
        print("self.fileJosn=",self.fileJosn)
        # self.RenameFiles(self.GetCurPath())
        self.ScanFiles(self.GetCurPath())
        self.Save(self.fileJosn)
        
  

# 主函数的实现
if __name__ == "__main__":  
    p = MakeLevelJson()
    p.Run()
    print("MakeLevelJson finish")