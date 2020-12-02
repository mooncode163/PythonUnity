import sys
import os
import json
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径


from Common.DB.Sql import Sql 
import re

class DBMusic(): 
    sql:None
    TABLE_NAME:"" 
   

    def OpenDB(self,dbfile):
        self.sql = Sql()
        self.sql.Open(dbfile)
        self.TABLE_NAME = "TableMusic"

        self.item_col = []
        self.item_coltype = []

        self.KEY_title = "title"
        self.KEY_year = "year"
        self.KEY_url = "url"
        self.KEY_id = "id"
        self.KEY_source = "source"
        self.KEY_album = "album"
        self.KEY_artist = "artist"
        self.KEY_genre = "genre"
        self.KEY_pic = "pic"
        
     

        self.item_col.append(self.KEY_title)
        self.item_col.append(self.KEY_year)
        self.item_col.append(self.KEY_url)
        self.item_col.append(self.KEY_id)
        self.item_col.append(self.KEY_source)
        self.item_col.append(self.KEY_album)
        self.item_col.append(self.KEY_artist)
        self.item_col.append(self.KEY_genre)
        self.item_col.append(self.KEY_pic)

        for i in range(len(self.item_col)):
            self.item_coltype.append("TEXT")

         # 注意 CREATE TABLE 这种语句不分大小写 PRIMARY KEY
        # sql_create = '''
        # CREATE TABLE IF NOT EXISTS `TablePoem`  (
        #     `title`    TEXT  , 
        #     `year`    TEXT  , 
        #     `author`    TEXT  ,
        #     `content`    TEXT  ,
        #     `content_pinyin`    TEXT  ,
        #     `translation`    TEXT  ,
        #     `authorDetail`    TEXT  ,
        #     `appreciation`    TEXT
        # )
        # '''

        # self.sql.Execute(sql_create)
        self.sql.CreateTable(self.TABLE_NAME,self.item_col,self.item_coltype)


    def IsBlankString(self,string):
        if string==None:
            return True

        if len(string)==0:
            return True

        return False

    def SetVaule(self,values,content):
        if self.IsBlankString(content):
            values.append("unknown")
        else:
            str = content
            # values.append(re.escape(content))
            # str = str.replace(",",".")
            # str = str.replace("，",".")
            values.append(str)

    def AddItem(self,info):
        if self.IsItemExist(info.title)==True:
            return

        values=[] 
        self.SetVaule(values,info.title)
        self.SetVaule(values,info.year)
        self.SetVaule(values,info.url)
        self.SetVaule(values,info.id)
        self.SetVaule(values,info.source)
        self.SetVaule(values,info.album)
        self.SetVaule(values,info.artist)
        self.SetVaule(values,info.genre)
        self.SetVaule(values,info.pic)
   
        # INSERT INTO TablePoem  VALUES('a','c','b','d','e','f')
# INSERT INTO TablePoem ('title', 'author', 'content','content_pinyin','translation','appreciation') VALUES('a','unknown','b','unknown','unknown','unknown')
       
        self.sql.Insert(self.TABLE_NAME,values)


    
    def IsItemExist(self,title):
        ret = False
        strsql = "SELECT * FROM " + self.TABLE_NAME + " WHERE title = '" + title + "'"
        cursor = self.sql.Execute(strsql)
        rows=cursor.fetchall()
        if len(rows)>0:
            ret = True
        
        print("IsItemExist  ret=",ret)
        return ret


    def GetIndexOfCol(self,strcol):
        for i,value in enumerate(self.item_col):
            if value == strcol:
                return i
        
        return 0
  
    def GetAllItem(self):
        strsql = "select * from " + self.TABLE_NAME
        cursor = self.sql.Execute(strsql) 
        rows=cursor.fetchall()
        for r in rows:
            listRow = list(r)
            title = listRow[0]
            value = listRow[self.GetIndexOfCol(self.KEY_title)] 
            print(title)
            print(value)
            break


mainDBMusic = DBMusic()
mainDBMusic.OpenDB("OutPut/DbMusic.db")
 
 