#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import requests
import json

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from src.Scopus_Crawler.scopus_config import headers

payload_data = {"pageNo": 0, "pageSize": 50000, "condition": {"name": "", "unitName": "", "awardId": "", "year": ""}}
base_url = 'http://api.bsef.baosteel.com/v1/api/applyer/list?domainId=1'

get_data = requests.post(url=base_url, data=json.dumps(payload_data), headers=headers, timeout=30)
data_dict = eval(get_data.text)
data_list = data_dict['data']['data']

data_df = pd.DataFrame(data=data_list)

school = pd.read_excel('C:/Users/Administrator/Desktop/test_data/ranking_scopus.xlsx')

data_df = pd.merge(data_df, school.loc[:, ['软科代码', '学校名称']], how='left', left_on='unitName', right_on='学校名称')

data_df.to_excel('C:/Users/Administrator/Desktop/0717.xlsx', sheet_name='Sheet1', index=False)
