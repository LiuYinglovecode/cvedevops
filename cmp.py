# emergency vulnerability
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
import time
import calendar
import os
import numpy as np
path = os.getcwd()
# 默认csv文件在当前目录下，后续可根据实际情况修改
#path = '\test\test\csvfiles'
table_list = []
new_table_list = []
fn = 'tobefilled.xlsx'
with open('to_be_checked.txt', 'r') as f:
    c=0
    a = []
    for l in f.readlines():
        l = l.strip()
        ts = calendar.timegm(time.gmtime())
        tnf = l + ".xlsx"
        values = ',%s'
        emp = pd.read_excel(tnf, sheet_name='应急漏洞',usecols='A:U')
        fin = pd.read_excel(fn, sheet_name='应急漏洞',usecols='A:U')
        emp.head()
        #print("this is emphead: ",emp3)
        try:
            conn = msql.connect(host='172.20.4.71', user='root',port=3310,
                                password='#B7jxGg]SLC9R%',database='cve')
            if conn.is_connected():
                cursor = conn.cursor(prepared=True)
                cursor.execute("select database();")
                record = cursor.fetchone()
#                    cursor.execute(con, multi=True)
                print("connect successful")
                for i,row in fin.iterrows():
#                    print(row)

                    sql = "SELECT status,method FROM march WHERE ip="+ "'"+ row[2] +"'"+ \
                    " AND os=" + "'" +row[5] + "'" +" AND vulneral="+ "'" +row[7] + "'" + " LIMIT 0, 1" +";"
#                    print(sql)
#                    cursor.execute(sql, tuple(row))
                    cursor.execute(sql)
                    res = cursor.fetchall()
                    if not res:
                        print("list is empty, the ip is: ",row[2])
                    else:
                        if res[0][0]=='已处理':
                            fin.loc[i,'状态'] = res[0][0]
                            fin.loc[i,'处理方法'] = res[0][1]
                            writer = pd.ExcelWriter(fn)
                            fin.to_excel(writer, sheet_name='应急漏洞' ,index=False)
                            writer.save()
                    conn.commit()
        except Error as e:
            print("Error while connecting to MySQL",e)
