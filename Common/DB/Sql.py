import sqlite3

class Sql(): 
    conn:None
    def Open(self,dbfile):
        self.conn = sqlite3.connect(dbfile)
        return self.conn

    def Close(self):
        self.conn.close()

    def Execute(self,strsql):
        print("Execute=",strsql)
        cursor = self.conn.execute(strsql)
        self.conn.commit()
        return cursor

    def IsExitTable(self,name):
        ret = False
        strsql = "select * from sqlite_master where type='table' and name = '" + name + "'";
        cursor = self.Execute(strsql) 
        rows=cursor.fetchall()
        if len(rows)>0:
            ret = True
        # for row in rows:  
            # print('%s %s\n' % (row[0],row[1]))  
        cursor.close()
        return ret 
    
    # 插入 string[] values
    def Insert(self,tableName,values):
        strsql = "INSERT INTO " + tableName + " VALUES('" + values[0] 

        for i in range(1,len(values)):  
            strsql +=   "','" + values[i]

        strsql += "')"
        self.Execute(strsql)

    def Update(self,tableName,cols,values, selectKey,  selectValue):
        strsql = "UPDATE " + tableName + " SET " + cols[0] + " = '" + values[0]+"'"

        for i in range(1,len(values)):  
            strsql +=   "," + cols[i] + " = '" + values[i]+"'"

        strsql += " WHERE "+ selectKey + " = '" + selectValue + "'"
        print("Update strsql="+strsql)
        # UPDATE TableApp SET appid = '100270155',version = '2.2.2',package = 'com.moonma.caicaile' WHERE package = 'com.moonma.caicaile'
        self.Execute(strsql)
 

    # string[] colValues colTypes
    def CreateTable (self,tableName,col,colType):
        strsql = "CREATE TABLE IF NOT EXISTS " + tableName + " (" + col[0] + " " + colType[0]

        for i in range(1,len(col)): 
            strsql += ", " + col[i] + " " + colType[i]
        
        strsql += ")"
    
        self.Execute(strsql)
 


# def create(conn):
#     # 注意 CREATE TABLE 这种语句不分大小写
#     sql_create = '''
#     CREATE TABLE `users` (
#         `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#         `username`    TEXT NOT NULL UNIQUE,
#         `password`    TEXT NOT NULL,
#         `email`    TEXT
#     )
#     '''
#     # 用 execute 执行一条 sql 语句
#     conn.execute(sql_create)
#     print('创建成功')


# def insert(conn, username, password, email):
#     sql_insert = '''
#     INSERT INTO
#         users(username,password,email)
#     VALUES
#         (?, ?, ?);
#     '''
#     # 下面的写法用 string.format 拼 sql, 是一个严重的安全漏洞
#     # 会被 SQL 注入
#     # sql = '''
#     # INSERT INTO
#     #     users(username,password,email)
#     # VALUES
#     #     ("{}", "{}", "{}")
#     # '''.format('123', '345', 'a.com')
#     # conn.execute(sql)
#     # 参数拼接要用 ?，execute 中的参数传递必须是一个 tuple 类型
#     conn.execute(sql_insert, (username, password, email))
#     print('插入数据成功')


# def select(conn):
#     # 一个注入的用户名
#     usr = 'gua" or "1"="1'
#     pwd = 'gua'
#     sql = '''
#     SELECT
#         id, username, email
#     FROM
#         users
#     WHERE
#         username=? and pwe=?
    


#     #WHERE
#     #    username="{}" and password="{}"
#     #'''.format(usr, pwd)
#     # 这是读取数据的套路
#     cursor = conn.execute(sql)
#     print('所有数据', list(cursor))
#     # for row in cursor:
#     #     print(row)


# def delete(conn, user_id):
#     sql_delete = '''
#     DELETE FROM
#         users
#     WHERE
#         id=?
#     '''
#     # 注意, execute 的第二个参数是一个 tuple
#     # tuple 只有一个元素的时候必须是这样的写法
#     conn.execute(sql_delete, (user_id,))


# def update(conn, user_id, email):
#     """
#     UPDATE
#         `users`
#     SET
#         `email`='gua', `username`='瓜'
#     WHERE
#         `id`=6
#     """
#     sql_update = '''
#     UPDATE
#         `users`
#     SET
#         `email`=?
#     WHERE
#         `id`=?
#     '''
#     conn.execute(sql_update, (email, user_id))


# def main():
#     # 指定数据库名字并打开
#     db_path = 'web8.sqlite'
#     conn = sqlite3.connect(db_path)
#     print("打开了数据库")
#     # 打开数据库后 就可以用 create 函数创建表
#     # create(conn)
#     # 然后可以用 insert 函数插入数据
#     # insert(conn, 'sql4', '1234', 'a@b.c')
#     # 可以用 delete 函数删除数据
#     # delete(conn, 1)
#     # 可以用 update 函数更新数据
#     # update(conn, 1, 'gua@cocode.cc')
#     # select 函数查询数据
#     # select(conn)
#     #
#     # 必须用 commit 函数提交你的修改
#     # 否则你的修改不会被写入数据库
#     conn.commit()
#     # 用完数据库要关闭
#     conn.close()

 