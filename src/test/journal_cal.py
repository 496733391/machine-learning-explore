#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import copy
import json

from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password


def data_prepare():
    dbutil = DBUtil(host, port, database, username, password)
    sql = 'select scopus_journal_id, sum(cite_num+0) as cite_num_all from scopus_cite_data group by scopus_journal_id'
    df1 = dbutil.get_allresult(sql, 'df')

    sql = 'SELECT scopus_journal_id,cite_num+0 as cite_num_self from scopus_cite_data ' \
          'where scopus_journal_id=cite_journal_id'
    df2 = dbutil.get_allresult(sql, 'df')

    df1 = pd.merge(df1, df2, how='outer', on='scopus_journal_id')
    df1.fillna(0, inplace=True)
    df1['cite_num_noself'] = df1['cite_num_all'] - df1['cite_num_self']
    df1.to_excel('C:/Users/Administrator/Desktop/去除自引被引数据.xlsx', index=False)

    sql = 'select cite_journal_id as scopus_journal_id, sum(cite_num+0) as cite_num_all ' \
          'from scopus_cite_data group by cite_journal_id'
    df3 = dbutil.get_allresult(sql, 'df')
    df3 = pd.merge(df3, df2, how='outer', on='scopus_journal_id')
    df3.fillna(0, inplace=True)
    df3['cite_num_noself'] = df3['cite_num_all'] - df3['cite_num_self']
    df3.to_excel('C:/Users/Administrator/Desktop/去除自引引用数据.xlsx', index=False)


def process():
    # core_journal_data = pd.read_excel('C:/Users/Administrator/Desktop/各学科核心期刊-待筛选.xlsx', sheet_name='Sheet3')
    # core_journal_data.fillna(method='ffill', inplace=True)
    # core_journal_data['期刊ID'] = core_journal_data['期刊ID'].astype('str')
    # core_journal_data2 = pd.read_excel('C:/Users/Administrator/Desktop/Core_journal_list_wen.xlsx')
    # core_journal_data2['Source ID'] = core_journal_data2['Source ID'].astype('str')
    # core_journal_dict = {}
    # for subject, sub_df in core_journal_data.groupby('学科名称'):
    #     core_journal_dict[subject] = list(sub_df['期刊ID'])
    #
    # for subject, sub_df in core_journal_data2.groupby('一级学科名称'):
    #     core_journal_dict[subject] = list(sub_df['Source ID'])
    #
    # with open('core_journal.json', 'w', encoding='utf-8') as js:
    #     js.write(json.dumps(core_journal_dict, indent=4, ensure_ascii=False))
    #
    # citing_data = pd.read_excel('C:/Users/Administrator/Desktop/去除自引引用数据.xlsx')
    # cited_data = pd.read_excel('C:/Users/Administrator/Desktop/去除自引被引数据.xlsx')
    # citing_data['scopus_journal_id'] = citing_data['scopus_journal_id'].astype('str')
    # cited_data['scopus_journal_id'] = cited_data['scopus_journal_id'].astype('str')
    # citing_data.set_index('scopus_journal_id', inplace=True)
    # cited_data.set_index('scopus_journal_id', inplace=True)
    # citing_data_dict = citing_data.to_dict()['cite_num_noself']
    # cited_data_dict = cited_data.to_dict()['cite_num_noself']
    #
    # with open('citing_data.json', 'w') as js:
    #     js.write(json.dumps(citing_data_dict, indent=4))
    #
    # with open('cited_data.json', 'w') as js:
    #     js.write(json.dumps(cited_data_dict, indent=4))

    core_journal_data = pd.read_excel('C:/Users/Administrator/Desktop/core_journal-new.xlsx')
    core_journal_data['scopus_journal_id'] = core_journal_data['scopus_journal_id'].astype('str')
    core_journal_data = core_journal_data.loc[core_journal_data['Core journal'].notnull()]
    core_journal_dict = {}
    for subject, sub_df in core_journal_data.groupby('Core journal'):
        if subject not in ['公安学', '马克思主义理论', '军事思想及军事历史', '中国史', '中医学', '中国语言文学',
                           '公安技术', '中药学', '军事装备学', '中西医结合', '战略学', '兵器科学与技术']:
            core_journal_dict[subject] = list(sub_df['scopus_journal_id'])

    with open('core_journal.json', 'w', encoding='utf-8') as js:
        js.write(json.dumps(core_journal_dict, indent=4, ensure_ascii=False))


def rf_cal():
    dbutil = DBUtil(host, port, database, username, password)
    sql = 'select scopus_journal_id, cite_num+0 as cite_num, cite_journal_id from scopus_cite_data ' \
          'where scopus_journal_id!=cite_journal_id'
    all_cite_data = dbutil.get_allresult(sql, 'df')

    # with open('core_journal.json', 'r', encoding='utf-8') as cj:
    #     core_journal = json.load(cj)

    core_journal = {}
    already_data = pd.read_excel('C:/Users/Administrator/Desktop/分学科结果.xlsx')
    already_data['scopus_journal_id'] = already_data['scopus_journal_id'].astype('str')
    for subject, sub_df in already_data.groupby('subject'):
        core_journal[subject] = list(sub_df['scopus_journal_id'])

    rf_cited_list = []
    rf_citing_list = []
    for subject, sub_journal in core_journal.items():
        print(subject)
        sub_cited_df_temp = all_cite_data.loc[all_cite_data['cite_journal_id'].isin(sub_journal)]
        sub_cited_df = sub_cited_df_temp.groupby('scopus_journal_id', as_index=False)['cite_num'].sum()
        sub_citing_df_temp = all_cite_data.loc[all_cite_data['scopus_journal_id'].isin(sub_journal)]
        sub_citing_df = sub_citing_df_temp.groupby('cite_journal_id', as_index=False)['cite_num'].sum()

        sub_cited_df['subject'] = subject
        rf_cited_list.append(sub_cited_df)

        sub_citing_df['subject'] = subject
        rf_citing_list.append(sub_citing_df)

    rf_cited_df = pd.concat(rf_cited_list)
    rf_citing_df = pd.concat(rf_citing_list)

    # dbutil.df_insert('rf_cited_data', rf_cited_df)
    # dbutil.df_insert('rf_citing_data', rf_citing_df)

    select_journal = pd.read_excel('C:/Users/Administrator/Desktop/未被分学科期刊.xlsx')
    select_journal['Scopus Source ID'] = select_journal['Scopus Source ID'].astype('str')
    rf_cited_df = rf_cited_df.loc[rf_cited_df['scopus_journal_id'].isin(list(select_journal['Scopus Source ID']))]
    rf_citing_df = rf_citing_df.loc[rf_citing_df['cite_journal_id'].isin(list(select_journal['Scopus Source ID']))]

    dbutil.df_insert('rf_cited_data_last', rf_cited_df)
    dbutil.df_insert('rf_citing_data_last', rf_citing_df)

    dbutil.close()


def last_process():
    dbutil = DBUtil(host, port, database, username, password)

    # sql = 'select scopus_journal_id, cite_num as rf_cited_num, subject from rf_cited_data'
    # rf_cited_data = dbutil.get_allresult(sql, 'df')
    #
    # sql = 'select cite_journal_id as scopus_journal_id, cite_num as rf_citing_num, subject from rf_citing_data'
    # rf_citing_data = dbutil.get_allresult(sql, 'df')

    sql = 'select scopus_journal_id, cite_num as rf_cited_num, subject from rf_cited_data_last'
    rf_cited_data = dbutil.get_allresult(sql, 'df')

    sql = 'select cite_journal_id as scopus_journal_id, cite_num as rf_citing_num, subject from rf_citing_data_last'
    rf_citing_data = dbutil.get_allresult(sql, 'df')

    sql = 'select * from cited_data'
    sum_cited_data = dbutil.get_allresult(sql, 'df')

    sql = 'select * from citing_data'
    sum_citing_data = dbutil.get_allresult(sql, 'df')

    rf_cited_data = pd.merge(rf_cited_data, sum_cited_data, how='left', on='scopus_journal_id')
    rf_cited_data['rf_cited_value'] = rf_cited_data['rf_cited_num'] / rf_cited_data['cited_num']
    rf_cited_sum = rf_cited_data.groupby('scopus_journal_id', as_index=False)['rf_cited_value'].sum()
    rf_cited_sum.rename(columns={'rf_cited_value': 'rf_cited_sum'}, inplace=True)
    rf_cited_data = pd.merge(rf_cited_data, rf_cited_sum, on='scopus_journal_id')
    rf_cited_data['rf_cited_percent'] = rf_cited_data['rf_cited_value'] / rf_cited_data['rf_cited_sum']

    rf_citing_data = pd.merge(rf_citing_data, sum_citing_data, how='left', on='scopus_journal_id')
    rf_citing_data['rf_citing_value'] = rf_citing_data['rf_citing_num'] / rf_citing_data['citing_num']
    rf_citing_sum = rf_citing_data.groupby('scopus_journal_id', as_index=False)['rf_citing_value'].sum()
    rf_citing_sum.rename(columns={'rf_citing_value': 'rf_citing_sum'}, inplace=True)
    rf_citing_data = pd.merge(rf_citing_data, rf_citing_sum, on='scopus_journal_id')
    rf_citing_data['rf_citing_percent'] = rf_citing_data['rf_citing_value'] / rf_citing_data['rf_citing_sum']

    rf_data = pd.merge(rf_cited_data, rf_citing_data, how='outer', on=['scopus_journal_id', 'subject'])

    rf_data.drop(columns=['cited_num', 'citing_num'], inplace=True)
    rf_data = pd.merge(rf_data, sum_cited_data, how='left', on='scopus_journal_id')
    rf_data = pd.merge(rf_data, sum_citing_data, how='left', on='scopus_journal_id')
    rf_data.fillna(0, inplace=True)
    rf_data['scopus_journal_id'] = rf_data['scopus_journal_id'].astype('int64')

    journal_name_data = pd.read_excel('C:/Users/Administrator/Desktop/Journal Citation Score 2019带一级学科信息20200726.xlsx')
    journal_name_data.drop_duplicates(subset=['Scopus Source ID'], inplace=True, ignore_index=True)

    with open('core_journal.json', 'r', encoding='utf-8') as cj:
        core_journal = json.load(cj)

    journal_name_data_temp = journal_name_data.loc[:, ['Scopus Source ID', 'Scholarly Output']]
    journal_name_data_temp['Scopus Source ID'] = journal_name_data_temp['Scopus Source ID'].astype('str')
    core_journal_article_num = {}
    for subject, value in core_journal.items():
        core_journal_article_num[subject] = sum(journal_name_data_temp[journal_name_data_temp['Scopus Source ID'].isin(value)]['Scholarly Output'])

    rf_data['cited_citing_sum'] = rf_data['citing_num'] + rf_data['cited_num']
    rf_data['cited_citing_percent_sum'] = rf_data['rf_cited_percent'] + rf_data['rf_citing_percent']
    # 获取中文名称
    journal_name_zh = pd.read_excel('C:/Users/Administrator/Desktop/期刊翻译结果.xlsx')
    rf_data = pd.merge(rf_data, journal_name_zh, how='left', on='scopus_journal_id')

    # rf_data.to_excel('C:/Users/Administrator/Desktop/rf_data.xlsx', index=False)

    rf_data.to_excel('C:/Users/Administrator/Desktop/rf_data_last.xlsx', index=False)

    rf_data_result = rf_data

    core_journal_num_dict = {}
    for subject, value in core_journal.items():
        core_journal_num_dict[subject] = len(value)

    rf_data_result['core_journal数量'] = rf_data_result['subject']
    rf_data_result['core_journal数量'].replace(core_journal_num_dict, inplace=True)
    rf_data_result['core_journal数量'] = rf_data_result['core_journal数量'].astype('int64')

    rf_data_result['core_journal发文数量'] = rf_data_result['subject']
    rf_data_result['core_journal发文数量'].replace(core_journal_article_num, inplace=True)
    rf_data_result['core_journal发文数量'] = rf_data_result['core_journal发文数量'].astype('int64')

    rf_data_result1 = copy.deepcopy(rf_data_result)
    rf_data_result2 = copy.deepcopy(rf_data_result)

    # 分学科结果，原始结果
    # 合并core_journal学科
    select_core_journal = pd.read_excel('C:/Users/Administrator/Desktop/core_journal-new.xlsx')
    select_core_journal = select_core_journal.loc[select_core_journal['Core journal'].notnull(),
                                                  ['scopus_journal_id', 'Core journal']]
    rf_data_result2 = pd.merge(rf_data_result2, select_core_journal, how='left', on='scopus_journal_id')

    rf_data_result2 = rf_data_result2.loc[(rf_data_result2['cited_citing_percent_sum'] >= 0.4) |
                                          (rf_data_result2['subject'] == rf_data_result2['Core journal'])]

    # rf_data_result2.to_excel('C:/Users/Administrator/Desktop/分学科结果.xlsx', index=False)

    rf_data_result2.to_excel('C:/Users/Administrator/Desktop/分学科结果last.xlsx', index=False)


if __name__ == '__main__':
    # process()
    rf_cal()
    last_process()
