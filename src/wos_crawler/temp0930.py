#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime

from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.data_write import write2sql
from src.Scopus_Crawler.scopus_config import host, port, database, username, password

# dbutil = DBUtil(host, port, database, username, password)
# sql = 'select * from wos_doc_data_copy'
# data = dbutil.get_allresult(sql, 'df')
# print('读取源数据完成')
# df = pd.read_excel('C:/Users/Administrator/Desktop/校名映射表.xlsx')
# data = pd.merge(data, df, how='left', on='orgName')
#
# print('merge完成')
# print('开始写入数据库')
# write2sql([['wos_doc_data0930', data]])
# print('写入数据库完成')


dbutil = DBUtil(host, port, database, username, password)
sql = 'select * from wos_doc_data_detail'
data = dbutil.get_allresult(sql, 'df')
print('读取源数据完成')
df = pd.read_excel('C:/Users/Administrator/Desktop/校名映射表.xlsx')
data = pd.merge(data, df, how='left', on='orgName')

data1 = data.loc[0:499999]
data2 = data.loc[500000:999999]
data3 = data.loc[1000000:1499999]
data4 = data.loc[1500000:1999999]
data5 = data.loc[2000000:2499999]
data6 = data.loc[2500000:2999999]
data7 = data.loc[3000000:]

data_list = [data1, data2, data3, data4, data5, data6, data7]

i = 0
for data in data_list:
    print(i)
    write2sql([['wos_doc_data_detail0930', data]])
    i += 1

