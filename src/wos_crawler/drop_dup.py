#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd

from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password

dbutil = DBUtil(host, port, database, username, password)
sql = 'select * from wos_article_data'
already_df = dbutil.get_allresult(sql, 'df')

already_df.drop_duplicates(subset=['UT'], ignore_index=True, inplace=True)

dbutil.df_insert('wos_article_data_final', already_df)
dbutil.close()
