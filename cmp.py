#comparison_values = df1.values == df2.values

#rows,cols=np.where(comparison_values==False)

#for item in zip(rows,cols):
#    df1.iloc[item[0], item[1]] = 
#    '{} --> {}'.format(df1.iloc[item[0], item[1]],df2.iloc[item[0], item[1]])
#df1.to_excel('./Excel_diff.xlsx',index=False,header=True)
#print (comparison_values)

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
with open('to_be_checked.txt', 'r') as f:
    c=0
    a = []
    for l in f.readlines():
        l = l.strip()
        ts = calendar.timegm(time.gmtime())
        tnf = l + ".xlsx"
        values = ',%s'
        # 将第一行作为第一列输出了
        emp = pd.read_excel(tnf, sheet_name='应急漏洞', usecols=['主机IP','主机系统类型','漏洞','状态'])
#        emp = emp2.insert(21,'处理方法','Null')
#        emp = pd.read_excel(tnf, header=None, sheet_name=1, names=columns)
        df2 = emp['主机IP'].str.rsplit("（", expand=True)
        emp["主机IP"]= df2[0]
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
                for i,row in emp.iterrows():
                    sql = "SELECT status,method FROM march WHERE ip="+ "'"+ row[0] +"'"+ \
                    " AND os=" + "'" +row[1] + "'" +" AND vulneral="+ "'" +row[2] + "'" + " LIMIT 0, 1" +";"
#                    cursor.execute(sql, tuple(row))
                    print(sql)
                    cursor.execute(sql)
                    res = cursor.fetchall()
                    print(res)
                    conn.commit()
        except Error as e:
            print("Error while connecting to MySQL",e)
