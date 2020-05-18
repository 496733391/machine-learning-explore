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

temp1 = temp.loc[:, ['学者代码', '姓名', '现在工作单位代码', '现在工作单位名称', 'Scopus代码', 'Scopus名称']]
temp1['Scopus名称'] = temp1['Scopus名称'].apply(lambda x: x.lower())
temp1.rename(columns={'现在工作单位代码': '软科代码', '现在工作单位名称': '头衔当选单位',
                      'Scopus代码': 'aff_id', 'Scopus名称': 'ins_en'}, inplace=True)
temp2 = temp.loc[:, ['学者代码', '姓名', '软科代码', '头衔当选单位', 'aff_id', 'ins_en']].dropna(subset=['aff_id'])

result = temp1.append(temp2, ignore_index=True)
result.drop_duplicates(['学者代码', 'aff_id'], inplace=True, ignore_index=True)

result.to_excel('C:/Users/Administrator/Desktop/test_data/test_data.xlsx', index=False, encoding='utf-8')
