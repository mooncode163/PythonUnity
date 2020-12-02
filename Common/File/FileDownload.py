  

import requests  


class FileDownload():  
    def Download(self,url,savepath): 
        r = requests.get(url) 
        with open(savepath, "wb") as data:
            data.write(r.content)

    def DownloadData(self,url): 
        r = requests.get(url)
        return r.content 

mainFileDownload = FileDownload() 
 
    