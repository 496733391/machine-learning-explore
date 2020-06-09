#! /usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import pandas as pd
from sqlalchemy import create_engine


def deal1():
    author_list1 = pd.read_excel('C:/Users/Administrator/Desktop/0528.xlsx', sheet_name='Sheet2')
    # select_no = []
    # for i in range(0, len(author_list1)):
    #     if len(author_list1.loc[i, 'name_zh']) > 2:
    #         select_no.append(i)
    #
    # author_list1 = author_list1.loc[select_no, :]
    # author_list1 = author_list1.loc[:500]

    author_list2 = pd.read_excel('C:/Users/Administrator/Desktop/test_data/test_data2.xlsx', sheet_name='Sheet1')

    author_list = pd.merge(author_list1, author_list2, how='left', left_on='person_id', right_on='学者代码')
    author_list.drop_duplicates(subset=['person_id'], inplace=True, keep='first')
    author_list.reset_index(drop=True, inplace=True)

    author_list['详细链接'] = 'a'
    author_list['百度搜索链接'] = 'b'
    author_list['搜索链接'] = 'c'

    search_url = 'https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al' \
                 '&st1={}' \
                 '&st2={}' \
                 '&orcidId=&affilName={}' \
                 '&sot=anl&sdt=anl&sl=64&resultsPerPage=200&offset=1&jtp=false&currentPage=1&exactAuthorSearch=true'

    for i in range(len(author_list)):
        author_list.loc[i, '详细链接'] = 'https://www.scopus.com/authid/detail.uri?authorId=%s' % author_list.loc[i, 'scopus_id']
        first_name = author_list.loc[i, 'name'].split(' ')[0].lower()
        last_name = author_list.loc[i, 'name'].split(' ')[1].lower()
        ins_name = '+'.join(author_list.loc[i, 'ins_en'].split(' ')).lower()
        author_list.loc[i, '搜索链接'] = search_url.format(first_name, last_name, ins_name)
        author_list.loc[i, '百度搜索链接'] = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=%s' \
                                       % author_list.loc[i, '头衔当选单位'] + author_list.loc[i, '姓名']

    author_list.to_excel('C:/Users/Administrator/Desktop/check_data.xlsx', index=False, encoding='utf-8')


def deal2():
    author_list = pd.read_excel('C:/Users/Administrator/Desktop/check_data.xlsx', sheet_name='Sheet1')
    ins_list = pd.read_excel('C:/Users/Administrator/Desktop/ins0528.xlsx', sheet_name='Sheet2')

    result = pd.merge(author_list, ins_list, how='inner', left_on='学者代码', right_on='person_id')
    result = result.loc[:, ['姓名', '学者代码', 'aff_name', 'start_year', 'end_year']]
    result.to_excel('C:/Users/Administrator/Desktop/机构信息0528.xlsx', index=False, encoding='utf-8')


def deal3():
    author_list = pd.read_excel('C:/Users/Administrator/Desktop/物理学高端人才清单.xlsx', sheet_name='Sheet3')
    result_df = pd.DataFrame(data=None, columns=None)
    for value, sub_df in author_list.groupby('人才代码'):
        lis = sub_df['头衔当选单位'].tolist() + sub_df['参考现职工作单位'].tolist()
        temp_df = pd.DataFrame(data=lis, columns=['单位名称'])
        temp_df['代码'] = sub_df.iloc[0]['人才代码']
        temp_df['姓名'] = sub_df.iloc[0]['人才姓名']
        result_df = result_df.append(temp_df, ignore_index=True)

    result_df.drop_duplicates(subset=['代码', '单位名称'], inplace=True, ignore_index=True)
    ins_df = pd.read_excel('C:/Users/Administrator/Desktop/test_data/ranking_scopus.xlsx', sheet_name='Sheet1')
    ins_df = ins_df.loc[:, ['学校名称', 'ins_en', 'aff_id']]
    result_df = pd.merge(result_df, ins_df, how='left', left_on='单位名称', right_on='学校名称')

    result_df.to_excel('C:/Users/Administrator/Desktop/result_df.xlsx', index=False, encoding='utf-8')


def deal4():
    author_list = pd.read_excel('C:/Users/Administrator/Desktop/result_df.xlsx', sheet_name='Sheet1')
    ins_list = pd.read_excel('C:/Users/Administrator/Desktop/result_df.xlsx', sheet_name='Sheet2')

    null_data = author_list.loc[author_list['aff_id'].isnull()]
    author_list.dropna(subset=['aff_id'], inplace=True)
    null_data = pd.merge(null_data, ins_list, how='left', on='单位名称')
    null_data.drop(columns=['ins_en', 'aff_id'], inplace=True)
    null_data.rename(columns={'ins_name': 'ins_en', 'ins_id': 'aff_id'}, inplace=True)

    author_list = author_list.append(null_data, ignore_index=True)
    author_list.rename(columns={'单位名称': '当选头衔单位', '代码': '学者代码'}, inplace=True)

    author_list.to_excel('C:/Users/Administrator/Desktop/test_data/test_data2.xlsx', sheet_name='Sheet1', index=False)


def deal5():
    from src.config.DBUtil import DBUtil
    from src.Scopus_Crawler.scopus_config import host, port, database, username, password

    dbutil = DBUtil(host, port, database, username, password)
    sql = "select DISTINCT person_id from mult_matched_author where data_no='2020052716115197'"
    df = dbutil.get_allresult(sql, 'df')
    dbutil.close()

    df2 = pd.read_excel('C:/Users/Administrator/Desktop/test_data/test_data2.xlsx')

    df2['学者代码'] = df2['学者代码'].astype('str')
    result = pd.merge(df, df2, how='left', left_on='person_id', right_on='学者代码')
    result.drop_duplicates(subset=['person_id'], inplace=True, ignore_index=True)

    result.to_excel('C:/Users/Administrator/Desktop/0605.xlsx', sheet_name='Sheet1', index=False)


def deal6():
    from src.config.DBUtil import DBUtil
    from src.Scopus_Crawler.scopus_config import host, port, database, username, password

    dbutil = DBUtil(host, port, database, username, password)
    sql = "select person_id, name from not_matched_author where data_no='2020060819255418'"
    df = dbutil.get_allresult(sql, 'df')
    dbutil.close()

    df2 = pd.read_excel('C:/Users/Administrator/Desktop/test_data/test_data2.xlsx')

    df2['学者代码'] = df2['学者代码'].astype('str')
    result = pd.merge(df, df2, how='left', left_on='person_id', right_on='学者代码')
    result.sort_values(by=['学者代码'], inplace=True, ignore_index=True)

    search_url = 'https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al' \
                 '&st1={}' \
                 '&st2={}' \
                 '&orcidId=&affilName={}' \
                 '&sot=anl&sdt=anl&sl=64&resultsPerPage=200&offset=1&jtp=false&currentPage=1&exactAuthorSearch=true'

    for i in range(len(result)):
        first_name = result.loc[i, 'name'].split(' ')[0].lower()
        last_name = result.loc[i, 'name'].split(' ')[1].lower()
        ins_name = '+'.join(result.loc[i, 'ins_en'].split(' ')).lower()
        result.loc[i, '搜索链接'] = search_url.format(first_name, last_name, ins_name)

    result.to_excel('C:/Users/Administrator/Desktop/0609not.xlsx', sheet_name='Sheet1', index=False)


if __name__ == '__main__':
    deal6()
