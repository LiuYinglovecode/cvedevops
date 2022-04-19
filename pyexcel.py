import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
import time
import calendar
import os
#from pathlib import Path
path = os.getcwd()
# 默认csv文件在当前目录下，后续可根据实际情况修改
#path = '\test\test\csvfiles'
table_list = []
new_table_list = []
#def search(args):
with open('table_name.txt', 'r') as f:
    c=0
    a = []
    for l in f.readlines():
        l = l.strip()
        ts = calendar.timegm(time.gmtime())
        with open(l+'.sql','r') as f2:
            te = ''.join([str(i) for i in f2.read().splitlines()])    
            print(te)
            lc = 0
            f2.seek(0)
            for le in f2:
                if le != "\n":
                    lc += 1
            ll = lc - 5
            print("this is ll: \n",ll)
            f2.close()
            values = '%s'
#            values = 'INET_ATON(%s)'
            n = 1
            while n < ll:
                values = values + ',%s' 
                n = n + 1
            tnf = l + ".xlsx"
            # 将第一行作为第一列输出了
            emp = pd.read_excel(tnf, sheet_name='应急漏洞', usecols=['主机IP','主机系统类型','风险等级','漏洞','影响软件','状态','处理方法'])
#            emp = pd.read_excel(tnf, header=None, sheet_name=1, names=columns)
            df2 = emp['主机IP'].str.rsplit("（", expand=True)
#            df3 = emp['漏洞'].str.rsplit("",expand=True)
            emp["主机IP"]= df2[0]
            
            emp.head()
#            print("this is emphead: ",emp)
            try:
                conn = msql.connect(host='172.20.4.71', user='root',port=3310,
                                    password='#B7jxGg]SLC9R%',database='cve') 
                if conn.is_connected():
                    cursor = conn.cursor(prepared=True)
                    cursor.execute("select database();")
                    record = cursor.fetchone()
#                    sqlz = "ALTER TABLE " + l + " RENAME TO " + l + str(ts) + ";"
#                    print("this is alter table sql: ",sqlz)
#                    con = sqlz + te
#                    cursor.execute(con, multi=True)
                    print("connect successful")
                    for i,row in emp.iterrows():
                        sql = "INSERT INTO "+l+ " (ip,os, levels, vulneral, software, status, method) "+" VALUES"+" ("+values+")"
                        print("let's see sql: \n",sql)
                        cursor.execute(sql, tuple(row))
                        conn.commit()
            except Error as e:
                print("Error while connecting to MySQL",e)
