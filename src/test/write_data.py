#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from itertools import product
import json

from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password

with open('core_journal.json', 'r', encoding='utf-8') as cj:
    core_journal = json.load(cj)
with open('cited_data.json', 'r') as cd:
    cited_data = json.load(cd)
with open('citing_data.json', 'r') as cd:
    citing_data = json.load(cd)

dbutil = DBUtil(host, port, database, username, password)
cited_df = pd.DataFrame(data={'scopus_journal_id': list(cited_data.keys()), 'cited_num': list(cited_data.values())})
citing_df = pd.DataFrame(data={'scopus_journal_id': list(citing_data.keys()), 'citing_num': list(citing_data.values())})

subjcet_list = []
journal_id_list = []
for key, value in core_journal.items():
    subjcet_list.extend([key] * len(value))
    journal_id_list.extend(value)

core_journal_df = pd.DataFrame(data={'subject': subjcet_list, 'scopus_journal_id': journal_id_list})

# dbutil.df_insert('core_journal', core_journal_df)
# dbutil.df_insert('cited_data', cited_df)
# dbutil.df_insert('citing_data', citing_df)

