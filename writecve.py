# 将应急漏洞写入数据库
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
import time
import calendar
import os
path = os.getcwd()
# 默认csv文件在当前目录下，后续可根据实际情况修改
#path = '\test\test\csvfiles'
table_list = []
new_table_list = []
with open('cve_table', 'r') as f:
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
            ll = lc - 6
            print("this is ll: \n",ll)
            f2.close()
            values = '%s'
            n = 1
            while n < ll:
                values = values + ',%s' 
                n = n + 1
            tnf = "march.xlsx"
            emp = pd.read_excel(tnf, sheet_name='应急漏洞', usecols=['漏洞','发现时间'])
#            emp = pd.read_excel(tnf, header=None, sheet_name=1, names=columns)
#            df2 = emp['主机IP'].str.rsplit("（", expand=True)
            df3 = emp['漏洞'].str.rsplit(" ",expand=True)
            emp["漏洞"]= df3[0]
            emp.head()
            try:
                conn = msql.connect(host='172.20.4.71', user='root',port=3310,
                                    password='#B7jxGg]SLC9R%',database='cve') 
                if conn.is_connected():
                    cursor = conn.cursor(prepared=True)
                    cursor.execute("select database();")
                    record = cursor.fetchone()
                    print("connect successful")
                    for i,row in emp.iterrows():
                        sql = "INSERT IGNORE INTO "+l+ " (name,create_time) "+" VALUES"+" ("+values+")"+";"
                        print("let's see sql: \n",sql)
                        cursor.execute(sql, tuple(row))
                        conn.commit()
            except Error as e:
                print("Error while connecting to MySQL",e)
