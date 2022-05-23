# system vulnerability 对比系统漏洞库，并写入系统漏洞修改情况更新到excel中
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
import time
import calendar
import os
import numpy as np
path = os.getcwd()
table_list = []
new_table_list = []
fn = 'tobeperfect.xlsx'
with open('to_be_checked.txt', 'r') as f:
    c=0
    a = []
    for l in f.readlines():
        l = l.strip()
        ts = calendar.timegm(time.gmtime())
        tnf = l + ".xlsx"
        values = ',%s'
        emp = pd.read_excel(tnf, sheet_name='系统漏洞',usecols='A:S')
        fin = pd.read_excel(fn, sheet_name='系统漏洞',usecols='A:S')
        df2 = emp['主机IP'].str.rsplit("（", expand=True)
        emp["主机IP"]= df2[0]
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
                    if i == 1:
                        print("this is row: \n",row)
                    sql = "SELECT status,method FROM march_sys WHERE ip="+ "'"+ row[1] +"'"+ \
                    " AND os=" + "'" +row[4] + "'" +" AND vulneral="+ "'" +row[6] + "'" + " LIMIT 0, 1" +";"
                    print(sql)
                    cursor.execute(sql)
                    res = cursor.fetchall()
                    if not res:
                        print("list is empty, the ip is: ",row[1])
                    else:
                        if res[0][0]=='已处理':
                            fin.loc[i,'状态'] = res[0][0]
                            fin.loc[i,'处理方法'] = res[0][1]
                            writer = pd.ExcelWriter(fn)
                            fin.to_excel(writer, sheet_name='系统漏洞' ,index=False)
                            writer.save()
                    conn.commit()
        except Error as e:
            print("Error while connecting to MySQL",e)
