#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd

from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password


# dbutil = DBUtil(host, port, database, username, password)
#
# sql = 'select * from scopus_cite_data'
# df1 = dbutil.get_allresult(sql, 'DF')
#
# df2 = pd.read_excel('C:/Users/Administrator/Desktop/temp.xlsx', sheet_name='Sheet2')
# df2['Scopus Source ID'] = df2['Scopus Source ID'].astype('str')
#
# df1 = pd.merge(df1, df2, left_on='cite_journal', right_on='Title', how='left')
#
# df1 = df1.loc[df1['scopus_journal_id'] == df1['Scopus Source ID']]
#
# df1.to_excel('C:/Users/Administrator/Desktop/self_cite_data.xlsx', index=False)
#
# dbutil.close()

df1 = pd.read_excel('C:/Users/Administrator/Desktop/temp.xlsx', sheet_name='Sheet3')
df2 = pd.read_excel('C:/Users/Administrator/Desktop/temp.xlsx', sheet_name='Sheet4')

df = pd.merge(df2, df1, on='Scopus Source ID', how='left')
df.fillna(0, inplace=True)

df['no_self_cite_num'] = df['Citation Count'] - df['cite_num']
df.to_excel('C:/Users/Administrator/Desktop/temp2.xlsx', index=False)
