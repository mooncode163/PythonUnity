#!/usr/bin/python
# coding=utf-8
import sys
import zipfile
import shutil
import os
import os.path
import json

from . import FileUtil

class CSVParser():  
    KEY_WORD_YINHAO = "\""
    KEY_WORD_YINHAO2 = "”"
    KEY_WORD_SPLIT = ","
    KEY_WORD_CANCEL = "#"

    rootJson = None
    fileJson = ""
    # 当前行数组
    listLine = []
    # 整个内容表
    listTable = []


    def ReadData(self,text):  
        self.SplitAllLine(text)
    def SplitAllLine(self,text):  
        list = text.split("\n") 
        index = 0
        for i in range(0, len(list)): 
            strline = list[i]
            if len(strline) > 0:
                # 注释
                if strline[0:1]==self.KEY_WORD_CANCEL:
                    continue
                   
            v_new = strline.replace("\r", "")
            self.SplitLine(v_new)
            index = index+1
        }

    def SplitLine(self,text): 
        list = []
        pos = 0
        # 是否有分割符
        ishas_split = False
        yinhao_pos_start = -1
        yinhao_pos_end = -1
        strYinhao = ""
        for i in range(0, len(text)):   
            word = text[i:i+1]

            if yinhao_pos_start >= 0:
                # //skip 引号
                if i <= yinhao_pos_end and i != str.length - 1 :
                    continue
                


            if word == self.KEY_WORD_SPLIT:
                ishas_split = True
                # //substring:pos to (i-1)
                len = (i - 1) - pos + 1
                strtmp = str.substr(pos, len)
                # //Debug.Log("SplitLine:" + strtmp)
                list.append(strtmp)
                pos = i + 1
            

            if (word == self.KEY_WORD_YINHAO) or (word == self.KEY_WORD_YINHAO2):
                strYinhao = word
                skip_step = 0
                # //查找下一个引号
                # //"亲,好玩,现在就去赞一个？","Pro, fun, and now to praise a?"
                # postmp = text.indexOf(strYinhao, i + 1)
                strtmp = text[i+1:]
                postmp = strtmp.find(strYinhao)
                if postmp >= 0:
                    yinhao_pos_start = i
                    yinhao_pos_end = postmp
                    skip_step = postmp - i + 1 
                # // i += skip_step
            
            if i == len(text) - 1 :
                if ishas_split == True: 
                    # //添加最后一个分割符后的子串
                    len = i - pos + 1
                    strtmp = text[pos:pos+len] 
                    # //Debug.Log("SplitLine:" + strtmp)
                    list.append(strtmp)

                else:
                    # //整个
                    list.append(str)
                
             

        # index = 0
        # for (let value of list) {
        #     //  Debug.Log("SplitLine list=" + value)
        #     index++
        # }
        self.listTable.append(list)

    def GetText(self,row,col): 
        # ret = ""
        # list = self.listTable[row]
        # ret = list[col]
        return self.listTable[row][col]

    def GetRowCount(self):
        return len(self.listTable)  
         


mainCSVParser = CSVParser()
 