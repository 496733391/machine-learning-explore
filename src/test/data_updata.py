#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password


dbutil = DBUtil(host, port, database, username, password)
data_df = pd.read_excel('C:/Users/Administrator/Desktop/待查数据0729.xlsx')
# person_id_list = data_df.loc[data_df['是否匹配'] == 0]['人才编号'].values.tolist()
person_id_list = data_df['人才编号'].values.tolist()
person_id_list = [str(i) for i in person_id_list]

for person_id in set(person_id_list):
    sql = 'update h_index set flag=0 where person_id="%s"' % person_id
    dbutil.execute_sql(sql)
    dbutil.execute_commit()
    sql = 'update author_info_new set flag=0 where person_id="%s"' % person_id
    dbutil.execute_sql(sql)
    dbutil.execute_commit()
    sql = 'update author_exp set flag=0 where person_id="%s"' % person_id
    dbutil.execute_sql(sql)
    dbutil.execute_commit()
    sql = 'update article_cite_data set flag=0 where person_id="%s"' % person_id
    dbutil.execute_sql(sql)
    dbutil.execute_commit()

dbutil.close()
