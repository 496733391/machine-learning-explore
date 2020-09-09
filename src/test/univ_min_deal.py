#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd

source_data = pd.read_excel('C:/Users/Administrator/Desktop/中国矿业大学（北京）论文抓取表.xlsx', sheet_name='Sheet2')
source_data['期刊名称'] = source_data['期刊名称'].str.upper()
source_data = source_data.loc[source_data['出版年份'].notnull()]

subejct_data = pd.read_excel('C:/Users/Administrator/Desktop/cssc-category-mapping.xlsx', sheet_name='Sheet3')
subejct_data = subejct_data.loc[subejct_data['一级学科名称'].notnull()]
subejct_data['一级学科代码'] = subejct_data['一级学科代码'].astype('int')
subejct_data['一级学科代码'] = subejct_data['一级学科代码'].astype('str')
subejct_data.reset_index(drop=True, inplace=True)
for i in range(len(subejct_data)):
    if len(subejct_data.loc[i, '一级学科代码']) < 4:
        subejct_data.loc[i, '一级学科代码'] = '0' + subejct_data.loc[i, '一级学科代码']

# 期刊数据
journal_data = pd.read_excel('C:/Users/Administrator/Desktop/wos_journal_data.xlsx')
journal_data['journalTitle'] = journal_data['journalTitle'].str.upper()
# merge获得影响因子
source_data = pd.merge(source_data, journal_data, left_on='期刊名称', right_on='journalTitle')

find_subject_list = ['0819', '0837', '0816', '0818', '0802', '0814', '0817', '1201', '0701', '0801', '0808',
                     '0812', '0830', '1204', '0811', '0305', '0502', '0702']

# 筛选第一作者和通讯作者
source_data['通讯作者及地址'].fillna('0', inplace=True)
select_dict = {}
for wos_id, sub_df in source_data.groupby('WOS文献ID'):
    if 'China Univ Min & Technol' in sub_df.iloc[0]['通讯作者及地址']:
        select_dict[wos_id] = '通讯作者'
    elif 'China Univ Min & Technol' in sub_df.iloc[0]['所有作者地址'].split('; [')[0]:
        select_dict[wos_id] = '第一作者'


source_data = source_data.loc[source_data['WOS文献ID'].isin(select_dict.keys())]
source_data['通讯作者或第一作者'] = source_data['WOS文献ID']
source_data['通讯作者或第一作者'].replace(select_dict, inplace=True)

# 按照期刊筛选出安全科学的另做处理
safety_journal_list = ['PROCESS SAFETY PROGRESS', 'SAFETY SCIENCE', 'FIRE TECHNOLOGY', 'JOURNAL OF SAFETY RESEARCH',
                       'FIRE AND MATERIALS', 'JOURNAL OF FIRE SCIENCES']
safety_data = source_data.loc[source_data['期刊名称'].isin(safety_journal_list), :]
safety_data['一级学科名称'] = '安全科学与工程'
safety_data['一级学科代码'] = '0837'

# 每篇文章拆分学科
temp_df_list = []
for wos_id, sub_df in source_data.groupby('WOS文献ID'):
    subject_list = sub_df.iloc[0]['学科'].split('; ')
    temp_df = pd.DataFrame(data=subject_list, columns=['WOS学科'])
    temp_df['WOS文献ID'] = wos_id
    temp_df_list.append(temp_df)

all_subject = pd.concat(temp_df_list)
all_subject['WOS学科'] = all_subject['WOS学科'].str.upper()
# 合并
source_data = pd.merge(source_data, all_subject, on='WOS文献ID')
# merge教育部一级学科
source_data = pd.merge(source_data, subejct_data, left_on='WOS学科', right_on='category_name')

# 合并安全工程的结果
source_data = source_data.append(safety_data, ignore_index=True)
# 按照学科，年份，影响因子，被引次数排序，取结果
source_data.sort_values(by=['一级学科名称', '出版年份', 'journalImpactFactor', '被引次数'],
                        ascending=[1, 1, 0, 0], inplace=True, ignore_index=True)

year_dict = {2016: 1, 2017: 1, 2018: 1, 2019: 1, 2020: 5/3}
subject_num_dict = {'矿业工程': 25, '测绘科学与技术': 15, '地质资源与地质工程': 15, '机械工程': 4, '土木工程': 4,
                    '化学工程与技术': 4, '管理科学与工程': 2, '数学': 3, '力学': 4, '电气工程': 2,
                    '计算机科学与技术': 2, '环境科学与工程': 4, '控制科学与工程': 2,
                    '外国语言文学': 2, '物理学': 2, '安全科学与工程': 25}

result_df = pd.DataFrame()
for year, year_time in year_dict.items():
    for subject, subject_num in subject_num_dict.items():
        take_num = round(year_time * subject_num) - 1
        temp_df = source_data.loc[(source_data['出版年份'] == year) & (source_data['一级学科名称'] == subject), :]
        temp_df.sort_values(by=['journalImpactFactor', '被引次数'], ascending=[0, 0], inplace=True, ignore_index=True)
        result_df = result_df.append(temp_df.loc[:take_num], ignore_index=True)

result_df.to_excel('C:/Users/Administrator/Desktop/中国矿业大学（北京）论文数据.xlsx', index=False)


