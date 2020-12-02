
from DB.Sql import Sql 
import re

class DBPoem(): 
    sql:None
    TABLE_NAME:"" 
   

    def OpenDB(self,dbfile):
        self.sql = Sql()
        self.sql.Open(dbfile)
        self.TABLE_NAME = "TablePoem"

        self.item_col = []
        self.item_coltype = []

        self.KEY_title = "title"
        self.KEY_year = "year"
        self.KEY_author = "author"
        self.KEY_content = "content"
        self.KEY_content_pinyin = "content_pinyin"
        self.KEY_translation = "translation"
        self.KEY_authorDetail = "authorDetail"
        self.KEY_appreciation = "appreciation"

        self.arrayPunctuation = ["。", "？", "！", "，", "、", "；", "：" ]



        self.item_col.append(self.KEY_title)
        self.item_col.append(self.KEY_year)
        self.item_col.append(self.KEY_author)
        self.item_col.append(self.KEY_content)
        self.item_col.append(self.KEY_content_pinyin)
        self.item_col.append(self.KEY_translation)
        self.item_col.append(self.KEY_authorDetail)
        self.item_col.append(self.KEY_appreciation)

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
        self.SetVaule(values,info.author)
        self.SetVaule(values,self.FortmatContent(info.content))
        self.SetVaule(values,self.FortmatContent(info.content_pinyin))
        self.SetVaule(values,info.translation)
        self.SetVaule(values,info.authorDetail)
        self.SetVaule(values,info.appreciation) 
        print("AddItem content_pinyin=",values[4])
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


    def FortmatContent(self,content):
        strtmp = content
        # 去除 (难着 一作：犹著)
        for i in range(10):
            idx0 = strtmp.find("(")
            idx1 = strtmp.find(")")
            if idx0<idx1:
                strfind = strtmp[idx0:idx1+1]
                strtmp = strtmp.replace(strfind,"")
        
        for i in range(10):
            idx0 = strtmp.find("（")
            idx1 = strtmp.find("）")
            if idx0<idx1:
                strfind = strtmp[idx0:idx1+1]
                strtmp = strtmp.replace(strfind,"")

        for i in range(10):
            idx0 = strtmp.find("[")
            idx1 = strtmp.find("]")
            if idx0<idx1:
                strfind = strtmp[idx0:idx1+1]
                strtmp = strtmp.replace(strfind,"")
                      
        for i in range(10):
            idx0 = strtmp.find("【")
            idx1 = strtmp.find("】")
            if idx0<idx1:
                strfind = strtmp[idx0:idx1+1]
                strtmp = strtmp.replace(strfind,"")

        return strtmp

    

    def SplitContent(self,content):
        strtmp = content
        strsplit = "-"
        for s in self.arrayPunctuation:
            strtmp = strtmp.replace(s,strsplit)
        
        liststr = strtmp.split(strsplit)
        # for s in liststr:
        #     print(s)
        return liststr

            
    def GetPoemContent(self,title):
        strsql = "select * from " + self.TABLE_NAME + " where title = '" + title + "'";
        cursor = self.sql.Execute(strsql) 
        rows=cursor.fetchall()
        for r in rows:
            listRow = list(r) 
            content = listRow[self.GetIndexOfCol(self.KEY_content)]
            return self.SplitContent(content) 

        return None


    def GetAllItem(self):
        strsql = "select * from " + self.TABLE_NAME
        cursor = self.sql.Execute(strsql) 
        rows=cursor.fetchall()
        for r in rows:
            listRow = list(r)
            title = listRow[0]
            content = listRow[self.GetIndexOfCol(self.KEY_content)]
            self.SplitContent(content)
            print(title)
            print(content)
            break

  
 
 