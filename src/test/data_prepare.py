#! /usr/bin/python
# -*- coding: utf-8 -*-


import pandas as pd

author_list = pd.read_excel('C:/Users/Administrator/Desktop/test_data/author_list.xlsx')
ins_list = pd.read_excel('C:/Users/Administrator/Desktop/test_data/ins_list.xlsx')
scopus_list = pd.read_excel('C:/Users/Administrator/Desktop/test_data/scopus_list.xlsx')

ins_list['英文校名'] = ins_list['英文校名'].astype('str')
ins_list['ins_en'] = ins_list['英文校名'].apply(lambda x: x.lower())

scopus_list['ins_en'] = scopus_list['aff_name'].apply(lambda x: x.lower())

ranking_scopus = pd.merge(ins_list, scopus_list, on='ins_en', how='left')
ranking_scopus.dropna(subset=['aff_id'], inplace=True)

temp = pd.merge(author_list, ranking_scopus, left_on='头衔当选单位', right_on='学校名称', how='left')

result = temp.loc[:, ['学者代码', '姓名', '头衔当选单位', '软科代码', 'ins_en', 'aff_id']]

result.to_excel('C:/Users/Administrator/Desktop/test_data/test_data.xlsx', index=False, encoding='utf-8')
