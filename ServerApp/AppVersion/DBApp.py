import sys
import os
# import json
# o_path = os.getcwd()  # 返回当前工作目录
# sys.path.append(o_path)  # 添加自己指定的搜索路径
sys.path.append("../../") 

from Common.DB.Sql import Sql 
import re

class DBApp(): 
    sql:None
    TABLE_NAME:"" 
   

    def OpenDB(self,dbfile):
        self.sql = Sql()
        self.sql.Open(dbfile)
        self.TABLE_NAME = "TableApp"

        self.item_col = []
        self.item_coltype = []

        self.KEY_appid = "appid"
        self.KEY_version = "version"
        self.KEY_package = "package" 
        
     

        self.item_col.append(self.KEY_appid)
        self.item_col.append(self.KEY_version)
        self.item_col.append(self.KEY_package) 

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
        if self.IsItemExist(info.package)==True:
            return

        values=[] 
        self.SetVaule(values,info.appid)
        self.SetVaule(values,info.version)
        self.SetVaule(values,info.package) 
   
        # INSERT INTO TablePoem  VALUES('a','c','b','d','e','f')
# INSERT INTO TablePoem ('title', 'author', 'content','content_pinyin','translation','appreciation') VALUES('a','unknown','b','unknown','unknown','unknown')
       
        self.sql.Insert(self.TABLE_NAME,values)


    def UpdateItem(self,info):
        if self.IsItemExist(info.package)==False:
            return

        cols = []
        cols.append(self.KEY_version)

        values=[] 
        # self.SetVaule(values,info.appid)
        # self.SetVaule(values,info.version)
        self.SetVaule(values,info.version)  
        
        self.sql.Update(self.TABLE_NAME,cols,values,self.KEY_package,info.package)
        

    def IsItemExist(self,package):
        ret = False
        strsql = "SELECT * FROM " + self.TABLE_NAME + " WHERE package = '" + package + "'"
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
            appid = listRow[self.GetIndexOfCol(self.KEY_appid)] 
            version = listRow[self.GetIndexOfCol(self.KEY_version)]
            package = listRow[self.GetIndexOfCol(self.KEY_package)]
            print(appid)
            print(version)
            print(package)
            break

    def GetVersionByPackage(self,package):
        strsql = "select * from " + self.TABLE_NAME+ " where package = '"+package+ "'" 
        print(strsql)
        cursor = self.sql.Execute(strsql) 
        rows=cursor.fetchall()
        version = ""
        for r in rows:
            listRow = list(r)  
            version = listRow[self.GetIndexOfCol(self.KEY_version)]
            break
        return version

mainDBApp = DBApp()
mainDBApp.OpenDB("DBApp.db")
 
 