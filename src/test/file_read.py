#! /usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import pandas as pd
from sqlalchemy import create_engine


author_list1 = pd.read_excel('C:/Users/Administrator/Desktop/0521.xlsx', sheet_name='Sheet1')
author_list2 = pd.read_excel('C:/Users/Administrator/Desktop/0521.xlsx', sheet_name='Sheet2')

author_list = pd.merge(author_list2, author_list1, how='outer', left_on='person_id', right_on='学者代码')
author_list.drop_duplicates(subset=['person_id'], inplace=True)

author_list['flag'] = 0
author_list.loc[author_list['scopus_id_x'] != author_list['scopus_id_y'], 'flag'] = 1

author_list.to_excel('C:/Users/Administrator/Desktop/test_data/temp_data.xlsx', index=False, encoding='utf-8')

# host = 'localhost'
# port = 3306
# database = 'local'
# username = 'root'
# password = 'admin'
#
# db_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=UTF8MB4". \
#             format(username=username, password=password, host=host, port=port, db=database)
#
# engine = create_engine(db_url)
#
# scopus_df = pd.read_sql('select * from scopus_ins', engine)
#
# ins_df = pd.read_excel('C:/Users/Administrator/Desktop/test_data/ins_list.xlsx')
#
# ins_df['英文校名'] = ins_df['英文校名'].astype('str')
# ins_df['ins_en'] = ins_df['英文校名'].apply(lambda x: x.lower().strip().replace('  ', ' '))
#
# scopus_df['ins_en'] = scopus_df['aff_name'].apply(lambda x: x.lower().strip().replace('  ', ' '))
#
# ranking_scopus = pd.merge(ins_df, scopus_df, on='ins_en', how='left')
#
# ranking_scopus.to_excel('C:/Users/Administrator/Desktop/test_data/ranking_scopus.xlsx', index=False, encoding='utf-8')
#
# ranking_scopus.dropna(subset=['aff_id'], inplace=True)
# ranking_scopus.drop_duplicates(subset=['aff_id'], inplace=True)
