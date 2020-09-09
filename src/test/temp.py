#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import json
from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password

# with open('subject_core_journal.json', 'r') as js:
#     subject_core_journal_dict = json.load(js)
#
# subjcet = []
# core_journal = []
# for key, value in subject_core_journal_dict.items():
#     if value:
#         subjcet += [key]*len(value)
#         core_journal += value
#
# df = pd.DataFrame(data={'subject': subjcet, 'core_journal': core_journal})
# df1 = pd.read_excel('C:/Users/Administrator/Desktop/jcr_data/Abb_article&reference.xlsx')
# df = pd.merge(df, df1, how='left', left_on='core_journal', right_on='Abb')
# df.to_excel('C:/Users/Administrator/Desktop/各学科核心期刊-待筛选.xlsx', index=False)


# dbutil = DBUtil(host, port, database, username, password)
# sql = 'select scopus_journal_id, sum(cite_num+0) as cite_num from scopus_cite_data0810 group by scopus_journal_id'
# df1 = dbutil.get_allresult(sql=sql, data_type='df')
# sql = 'select scopus_journal_id, cite_num+0 as cite_num2 from scopus_journal_id'
# df2 = dbutil.get_allresult(sql=sql, data_type='df')
# df = pd.merge(df1, df2, on='scopus_journal_id')


