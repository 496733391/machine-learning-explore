#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pandas as pd

data = pd.read_excel('C:/Users/Administrator/Desktop/学科点信息.xlsx', sheet_name='硕士一级学科')
index_list = []
for i in range(len(data['col1'].values)):
    if isinstance(data.loc[i, 'col1'], str):
        if '按地区、单位排列' in data.loc[i, 'col1']:
            index_list.append(i)

select_index_list = [j + 2 for j in index_list]
select_index_list.insert(0, 0)
page_num_index = [j - 2 for j in index_list]
result_list = []
for k in range(len(select_index_list)-1):
    select_df = data.loc[select_index_list[k]:select_index_list[k+1]-6]
    select_df1 = select_df.loc[:, ['col1', 'col2']]
    select_df2 = select_df.loc[:, ['col3', 'col4']]
    select_df2.rename(columns={'col3': 'col1', 'col4': 'col2'}, inplace=True)
    result = pd.concat([select_df1, select_df2])
    result['页码'] = data.loc[page_num_index[k], 'col1']
    result_list.append(result)

final = pd.concat(result_list)
final.to_excel('C:/Users/Administrator/Desktop/硕士一级学科.xlsx', index=False)
