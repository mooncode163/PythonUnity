  

import requests  
from urllib3 import encode_multipart_formdata
# import FileUtil
from . import FileUtil
class FileTransfer():  

    def GetPathNameWithExt(self,path):  
        idx = path.rfind("/")
        if idx<0:
            idx = path.rfind("\\")

        if idx<0:
            return path
        ret = path[(idx+1):]
        return ret

    def Download(self,url,savepath): 
        r = requests.get(url) 
        with open(savepath, "wb") as data:
            data.write(r.content)

    def DownloadData(self,url): 
        r = requests.get(url)
        return r.content 

# arg 附加参数
    def Upload(self,url, file_path,arg="arg"):
        """
        :param filename：文件的名称
        :param file_path：文件的绝对路径
        """ 
        # filename = FileUtil.GetPathNameWithExt(file_path)
        filename = self.GetPathNameWithExt(file_path)

        with open(file_path, "rb")as f:
        # with open(file_path, mode="r", encoding="utf8") as f : 
            file = {
                    "file": (filename, f.read()),# 引号的file是接口的字段，后面的是文件的名称、文件的内容
                    "arg": arg, # 如果接口中有其他字段也可以加上
                        } 
            
            encode_data = encode_multipart_formdata(file)
            
            file_data = encode_data[0] 
            # b'--c0c46a5929c2ce4c935c9cff85bf11d4\r\nContent-Disposition: form-data; name="file"; filename="1.txt"\r\nContent-Type: text/plain\r\n\r\n...........--c0c46a5929c2ce4c935c9cff85bf11d4--\r\n
            
            headers_from_data = {
                        "Content-Type": encode_data[1]
                        # "Authorization": token
                                } 
            # token是登陆后给的值，如果你的接口中头部不需要上传字段，就不用写，只要前面的就可以
            # 'Content-Type': 'multipart/form-data; boundary=c0c46a5929c2ce4c935c9cff85bf11d4'，这里上传文件用的是form-data,不能用json
            
            # response = requests.post(url=url, headers=headers_from_data, data=file_data).json()
            response = requests.post(url=url, headers=headers_from_data, data=file_data)
            return response.content.decode("utf-8")


mainFileTransfer = FileTransfer() 
 
    