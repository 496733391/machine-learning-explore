#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import math
import pandas as pd
from datetime import datetime

from src.Scopus_Crawler.scopus_config import proxies
from src.Scopus_Crawler.data_write import write2sql
from src.wos_crawler.author_name_deal import pinyin_trans
from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password


# drop_list = ['BA', 'BE', 'GP', 'BF', 'CA', 'SE', 'BS', 'CT', 'CY',
#              'CL', 'SP', 'HO', 'AB', 'FX', 'NR', 'PU', 'PI', 'PA',
#              'BN', 'J9', 'JI', 'PD', 'PU', 'SU', 'SI', 'MA', 'D2',
#              'EA', 'OA', 'HC', 'HP', 'DA', 'PN']
#
# dbutil = DBUtil(host, port, database, username, password)
# sql = 'select * from wos_article_data'
# already_df = dbutil.get_allresult(sql, 'df')
#
# already_df.drop(columns=drop_list, inplace=True)
# column_length = {c: already_df[c].str.len().max() for c in
#                  already_df.columns[already_df.dtypes == 'object'].tolist()}
# print(column_length)
#
# already_df = already_df.loc[:10000]
#
# print(datetime.now())
# dbutil.df_insert('wos_article_data_final', already_df)
# dbutil.close()
# print(datetime.now())


dbutil = DBUtil(host, port, database, username, password)
sql = 'select person_id, affiliation, timesCited, doc_num, author_position, period, hindex, ' \
      'highly_cited_paper, inter_colla, prsnName from incites_author_data1008'
data = dbutil.get_allresult(sql, 'df')

df = pd.read_excel('C:/Users/Administrator/Desktop/wos机构清理.xlsx', sheet_name='Sheet17')
df['人才编号'] = df['人才编号'].astype('str')
df.drop_duplicates(subset=['人才编号', 'wos机构名称'], inplace=True, ignore_index=True)

result = pd.merge(df, data, left_on=['人才编号', 'wos机构名称'], right_on=['person_id', 'affiliation'], how='inner')
for info, sub_df in result.groupby(['person_id', 'period']):
      result.loc[(result['person_id'] == info[0]) & (result['period'] == info[1]), 'hindex'] = sub_df['hindex'].max()
# result['timesCited'] = result['timesCited'].astype('int')
result = result.groupby(by=['人才编号', '姓名', 'author_position', 'period', 'hindex', 'prsnName'], as_index=False).sum()
df = df.loc[~df['人才编号'].isin(list(result['人才编号']))]
df = pd.merge(df, data, left_on=['人才编号'], right_on=['person_id'], how='inner')
df.to_excel('C:/Users/Administrator/Desktop/no_result1009.xlsx', index=False)
result.to_excel('C:/Users/Administrator/Desktop/result1009.xlsx', index=False)
