#! /usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import pandas as pd
from sqlalchemy import create_engine


def deal1():
    author_list1 = pd.read_excel('C:/Users/Administrator/Desktop/0526.xlsx', sheet_name='Sheet2')
    select_no = []
    for i in range(0, len(author_list1)):
        if len(author_list1.loc[i, 'name_zh']) > 2:
            select_no.append(i)

    author_list1 = author_list1.loc[select_no, :]
    author_list1 = author_list1.loc[:500]

    author_list2 = pd.read_excel('C:/Users/Administrator/Desktop/test_data/test_data.xlsx', sheet_name='Sheet1')

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
        first_name = author_list.loc[i, 'NAME'].split(' ')[0].lower()
        last_name = author_list.loc[i, 'NAME'].split(' ')[1].lower()
        ins_name = '+'.join(author_list.loc[i, 'ins_en'].split(' ')).lower()
        author_list.loc[i, '搜索链接'] = search_url.format(first_name, last_name, ins_name)
        author_list.loc[i, '百度搜索链接'] = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=%s' \
                                       % author_list.loc[i, '头衔当选单位'] + author_list.loc[i, '姓名']

    author_list.to_excel('C:/Users/Administrator/Desktop/check_data.xlsx', index=False, encoding='utf-8')


def deal2():
    author_list = pd.read_excel('C:/Users/Administrator/Desktop/check_data.xlsx', sheet_name='Sheet1')
    ins_list = pd.read_excel('C:/Users/Administrator/Desktop/ins0526.xlsx', sheet_name='Sheet2')

    result = pd.merge(author_list, ins_list, how='inner', left_on='学者代码', right_on='person_id')
    result = result.loc[:, ['姓名', '学者代码', 'aff_name', 'start_year', 'end_year']]
    result.to_excel('C:/Users/Administrator/Desktop/机构信息0526.xlsx', index=False, encoding='utf-8')


if __name__ == '__main__':
    deal2()
