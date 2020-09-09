#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd

classify_result = pd.read_excel('C:/Users/Administrator/Desktop/分学科结果.xlsx')

classify_result_dict = {}
for scopus_jounal_id, sub_df in classify_result.groupby('scopus_journal_id'):
    classify_result_dict[scopus_jounal_id] = list(sub_df['subject'])

origin_data = pd.read_excel('C:/Users/Administrator/Desktop/Journal Citation Score 2019带一级学科信息20200726.xlsx')
origin_data = origin_data.loc[:, ['Scopus Source ID', 'WoS匹配学科名称', 'ASJC匹配学科名称']]
origin_data_dict = {}
for scopus_journal_id, sub_df in origin_data.groupby('Scopus Source ID'):
    origin_data_dict[scopus_journal_id] = list(sub_df['WoS匹配学科名称']) + list(sub_df['ASJC匹配学科名称'])

select_list = []
for key, value in classify_result_dict.items():
    if len(set(value).intersection(set(origin_data_dict[key]))) == 0:
    # if value not in origin_data_dict[key]:
        select_list.append(key)

print(len(select_list))
err_result = classify_result.loc[classify_result['scopus_journal_id'].isin(select_list)]
err_result.to_excel('C:/Users/Administrator/Desktop/待查结果.xlsx', index=False)
