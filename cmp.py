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
#from openpyxl import load_workbook
import numpy as np
#from pathlib import Path
path = os.getcwd()
# 默认csv文件在当前目录下，后续可根据实际情况修改
#path = '\test\test\csvfiles'
table_list = []
new_table_list = []
#def search(args):
fn = 'tobefilled.xlsx'
with open('to_be_checked.txt', 'r') as f:
    c=0
    a = []
    for l in f.readlines():
        l = l.strip()
        ts = calendar.timegm(time.gmtime())
        tnf = l + ".xlsx"
        values = ',%s'
        # 将第一行作为第一列输出了
        emp = pd.read_excel(tnf, sheet_name='应急漏洞',usecols='A:U')
#        emp2 = pd.read_excel(tnf, sheet_name='应急漏洞',index_col=0)
#        emp = emp2.insert(21,'处理方法','Null')
#        emp = pd.read_excel(tnf, header=None, sheet_name=1, names=columns)
#        df2 = emp['主机IP'].str.rsplit("（", expand=True)
#        emp["主机IP"]= df2[0]
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
#                    print(row)
                    sql = "SELECT status,method FROM march WHERE ip="+ "'"+ row[2] +"'"+ \
                    " AND os=" + "'" +row[5] + "'" +" AND vulneral="+ "'" +row[7] + "'" + " LIMIT 0, 1" +";"
                    print(sql)
#                    cursor.execute(sql, tuple(row))
                    cursor.execute(sql)
                    res = cursor.fetchall()
                    if not res:
                        print("list is empty, the ip is: ",row[2])
                    else:
                        if res[0][0]=='已处理':
                            #writer = pd.ExcelWriter(tnf)
                            #emp.to_excel(writer, index=False)
                            #df2.to_excel(writer, startcol=7,startrow=6, header=None)
                            #writer.save()
#                            emp["主机IP"] = np.where(df["主机IP"] == row[0], res[0][0], "待处理")
#                            ip = row['主机IP'].str.rsplit("（", expand=True)
                            #print(type(row['主机IP']))
#                            ip = row['主机IP'].rsplit("（")[0]
                            emp.loc[(emp["主机IP"] == row[2]) & (emp["主机系统类型"]==row[5]) & (emp['漏洞']==row[7]),"状态"] = "已处理" 
                            writer = pd.ExcelWriter(fn)
                            emp.to_excel(writer, sheet_name='应急漏洞' ,index=False)
                            writer.save()
                            #print(emp2)
                    conn.commit()
        except Error as e:
            print("Error while connecting to MySQL",e)
