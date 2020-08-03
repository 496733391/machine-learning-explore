#! /usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import pandas as pd
from sqlalchemy import create_engine


def deal1():
    from src.config.DBUtil import DBUtil
    from src.Scopus_Crawler.scopus_config import host, port, database, username, password

    dbutil = DBUtil(host, port, database, username, password)
    sql = "select DISTINCT person_id, name, scopus_id from author_info_new where data_no='2020060819255418'"
    author_list1 = dbutil.get_allresult(sql, 'df')
    dbutil.close()

    author_list2 = pd.read_excel('C:/Users/Administrator/Desktop/test_data/test_data2.xlsx', sheet_name='Sheet1')
    author_list2['学者代码'] = author_list2['学者代码'].astype('str')

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


def deal7():
    df = pd.read_excel('C:/Users/Administrator/Desktop/期刊名称人名列表.xlsx')
    df['ins'] = df['JCR期刊列表'].apply(lambda x: x.replace('&', '%26'))
    df['name'] = '0'
    for i in range(len(df)):
        lis = df.loc[i, '姓名'].split(' ')
        print(lis)
        lis.insert(0, lis[-1])
        lis.pop()
        df.loc[i, 'name'] = ' '.join(lis)

    df['person_id'] = df.index
    df.to_excel('C:/Users/Administrator/Desktop/0618webofscience.xlsx', sheet_name='Sheet1', index=False)


def deal8():
    df = pd.read_excel('C:/Users/Administrator/Desktop/0618webofscience.xlsx')
    from src.config.DBUtil import DBUtil
    from src.Scopus_Crawler.scopus_config import host, port, database, username, password

    dbutil = DBUtil(host, port, database, username, password)
    sql = "select distinct (person_id+0) as person_id from not_find where person_id not in (select person_id from find_result)"
    not_find = dbutil.get_allresult(sql, 'df')
    dbutil.close()
    result = pd.merge(not_find, df, how='left', on='person_id')
    result.to_excel('C:/Users/Administrator/Desktop/未搜索到结果清单.xlsx', sheet_name='Sheet1', index=False)


def deal9():
    from src.config.DBUtil import DBUtil
    from src.Scopus_Crawler.scopus_config import host, port, database, username, password

    dbutil = DBUtil(host, port, database, username, password)
    sql = "select person_id+0 as person_id, find_num, ins from find_result"
    find_result = dbutil.get_allresult(sql, 'df')
    find_result['s_num'] = '0'
    for i in range(len(find_result)):
        temp_list = find_result.loc[i, 'ins'][:-1].split(' (')
        find_result.loc[i, 'ins'] = temp_list[0]
        find_result.loc[i, 's_num'] = temp_list[1]

    df = pd.read_excel('C:/Users/Administrator/Desktop/0618webofscience.xlsx')
    result = pd.merge(find_result, df, on='person_id', how='left')
    result.set_index(['person_id', 'JCR期刊列表', '姓名', 'find_num', 'ins_x'], inplace=True)
    result.to_excel('C:/Users/Administrator/Desktop/有搜索结果的数据.xlsx', sheet_name='Sheet1')


def deal10():
    from src.config.DBUtil import DBUtil
    from src.Scopus_Crawler.scopus_config import host, port, database, username, password

    dbutil = DBUtil(host, port, database, username, password)
    sql = "select person_id+0 as person_id from (select DISTINCT person_id from find_result UNION select " \
          "person_id from not_find) a ORDER BY person_id"
    df = dbutil.get_allresult(sql, 'df')

    df2 = pd.read_excel('C:/Users/Administrator/Desktop/0618webofscience.xlsx')
    df3 = df2.loc[~df2['person_id'].isin(list(df['person_id']))]
    df3.to_excel('C:/Users/Administrator/Desktop/data_left.xlsx', sheet_name='Sheet1', index=False)


def deal11():
    df1 = pd.read_excel('C:/Users/Administrator/Desktop/test_data/ranking_scopus.xlsx', sheet_name='Sheet1')
    df2 = pd.read_excel('C:/Users/Administrator/Desktop/test_data/机构清单.xlsx')
    df3 = pd.read_excel('C:/Users/Administrator/Desktop/test_data/机构名称对照.xlsx')

    df2 = pd.merge(df2, df1.loc[:, ['软科代码', '学校名称', 'aff_id', 'ins_en']], how='left', left_on='机构代码', right_on='软科代码')
    for i in range(len(df3)):
        df3.loc[i, '头衔当选单位'] = df3.loc[i, '头衔当选单位'].strip()

    for i in range(len(df2)):
        df2.loc[i, '机构名称'] = df2.loc[i, '机构名称'].strip()
        if str(type(df2.loc[i, '学校名称'])) != "<class 'float'>":
            df2.loc[i, '学校名称'] = df2.loc[i, '学校名称'].strip()

    df2 = pd.merge(df2, df3, left_on='学校名称', right_on='头衔当选单位', how='left')
    df2 = pd.merge(df2, df3, left_on='机构名称', right_on='头衔当选单位', how='left')
    df2['aff_id_x'].fillna(df2['aff_id_y'], inplace=True)
    df2['ins_en_x'].fillna(df2['ins_en_y'], inplace=True)
    df2['aff_id_x'].fillna(df2['aff_id'], inplace=True)
    df2['ins_en_x'].fillna(df2['ins_en'], inplace=True)
    df2['学校名称'].fillna(df2['机构名称'], inplace=True)
    df2 = df2.loc[:, ['机构代码', '机构名称', '学校名称', 'aff_id_x', 'ins_en_x']]
    df2.rename(columns={'aff_id_x': 'scopus机构ID', 'ins_en_x': '英文名称'}, inplace=True)

    df2.to_excel('C:/Users/Administrator/Desktop/机构数据.xlsx', sheet_name='Sheet1', index=False)


def deal12():
    df = pd.read_excel('C:/Users/Administrator/Desktop/机构数据.xlsx', sheet_name='Sheet3')
    df['百度搜索链接'] = 'https://www.baidu.com/s?wd=' + df['学校名称']
    df.to_excel('C:/Users/Administrator/Desktop/机构数据2.xlsx', sheet_name='Sheet1', index=False)


def deal13():
    df = pd.read_excel('C:/Users/Administrator/Desktop/人才名单_20200628.xlsx')
    df1 = df.loc[:, ['人才编号', '姓名', '当选单位名称']]
    df2 = df.loc[:, ['人才编号', '姓名', '现职单位名称']]
    df3 = df.loc[:, ['人才编号', '姓名', '当选前单位信息']]
    df1.dropna(inplace=True)
    df2.dropna(inplace=True)
    df3.dropna(inplace=True)
    df2.rename(columns={'现职单位名称': '当选单位名称'}, inplace=True)
    df3.rename(columns={'当选前单位信息': '当选单位名称'}, inplace=True)
    result = pd.concat([df1, df2, df3], ignore_index=True)
    result.drop_duplicates(subset=['人才编号', '当选单位名称'], inplace=True)

    ins_data = pd.read_excel('C:/Users/Administrator/Desktop/机构数据.xlsx')
    result = pd.merge(result, ins_data, how='left', left_on='当选单位名称', right_on='机构名称')
    final_result1 = []
    final_result2 = []
    for value, sub_df in result.groupby('人才编号'):
        temp_df = sub_df.dropna()
        if len(temp_df) > 0:
            final_result1.append(temp_df)
        else:
            final_result2.append(sub_df)

    result1 = pd.concat(final_result1)
    result2 = pd.concat(final_result2)
    result1.drop_duplicates(subset=['人才编号', 'scopus机构ID'], inplace=True)
    result1.to_excel('C:/Users/Administrator/Desktop/1-data20200628.xlsx', sheet_name='Sheet1', index=False)
    result2.to_excel('C:/Users/Administrator/Desktop/2-data20200628.xlsx', sheet_name='Sheet1', index=False)


def deal14():
    df1 = pd.read_excel('C:/Users/Administrator/Desktop/人才名单_20200628.xlsx')
    df2 = pd.read_excel('C:/Users/Administrator/Desktop/not_matched0702.xlsx')
    result = pd.merge(df2, df1, how='left', left_on='person_id', right_on='人才编号')
    result.to_excel('C:/Users/Administrator/Desktop/data20200702.xlsx', sheet_name='Sheet1', index=False)


def deal15():
    df1 = pd.read_excel('C:/Users/Administrator/Desktop/data20200702.xlsx')
    df2 = pd.read_excel('C:/Users/Administrator/Desktop/文科类.xlsx')
    result = df1.loc[~df1['person_id'].isin(list(df2['person_id']))]
    result_list = result.values.tolist()
    three = [one_p for one_p in result_list if len(one_p[1].strip()) >= 3]
    two = [one_p for one_p in result_list if len(one_p[1].strip()) < 3]

    three_df = pd.DataFrame(data=three, columns=result.columns)
    two_df = pd.DataFrame(data=two, columns=result.columns)

    three_df.to_excel('C:/Users/Administrator/Desktop/1-data20200702.xlsx', sheet_name='Sheet1', index=False)
    two_df.to_excel('C:/Users/Administrator/Desktop/2-data20200702.xlsx', sheet_name='Sheet1', index=False)


def deal16():
    df1 = pd.read_excel('C:/Users/Administrator/Desktop/有结果的学者-抓取学科用.xlsx')
    df2 = pd.read_excel('C:/Users/Administrator/Desktop/人才名单_20200628.xlsx')
    df3 = pd.read_excel('C:/Users/Administrator/Desktop/学科匹配-姜晓丹-20200726.xlsx')
    df4 = pd.read_excel('C:/Users/Administrator/Desktop/待查数据0729.xlsx')
    df1 = df1.loc[~df1['person_id'].isin(list(df3['人才编号']))]
    df1 = df1.loc[~df1['person_id'].isin(list(df4['人才编号']))]
    df2.sort_values(by=['人才编号', '参考学科名称'], inplace=True, ignore_index=True)
    df2.drop_duplicates(subset=['人才编号'], inplace=True, ignore_index=True)
    result = pd.merge(df1, df2, how='left', left_on='person_id', right_on='人才编号')

    result.to_excel('C:/Users/Administrator/Desktop/0729抓取学科用.xlsx', sheet_name='Sheet1', index=False)


def deal17():
    # journal_data = pd.read_excel('C:/Users/Administrator/Desktop/jcr_data/JCR完整期刊关键词列表 - 用于core journal筛选.xlsx')
    # subject_data = pd.read_excel('C:/Users/Administrator/Desktop/jcr_data/JCR期刊软科学科映射.xlsx')
    # journal_data.fillna('aaaa', inplace=True)
    # subject_data.fillna('aaaa', inplace=True)
    #
    # journal_data.drop('Key word 6', axis=1, inplace=True)
    #
    # for column in journal_data.columns:
    #     journal_data[column] = journal_data[column].str.strip()
    #
    # for column in subject_data.columns:
    #     subject_data[column] = subject_data[column].str.strip()
    #
    # journal_data.replace({'aaaa': None}, inplace=True)
    # subject_data.replace({'aaaa': None}, inplace=True)
    #
    # subject_dict = {}
    # for i in range(subject_data.shape[0]):
    #     subject_dict[subject_data.loc[i, 'WOS学科英文名'].upper()] = subject_data.loc[i, '2018软科学科英文名']
    #
    # journal_data.replace(subject_dict, inplace=True)
    # for i in range(len(journal_data)):
    #     temp_list = journal_data.loc[i, ['Research area 1', 'Research area 2', 'Research area 3',
    #                                      'Research area 4', 'Research area 5', 'Research area 6']].values.tolist()
    #     if journal_data.loc[i, 'Research area 2'] in temp_list[:1]:
    #         journal_data.loc[i, 'Research area 2'] = None
    #     if journal_data.loc[i, 'Research area 3'] in temp_list[:2]:
    #         journal_data.loc[i, 'Research area 3'] = None
    #     if journal_data.loc[i, 'Research area 4'] in temp_list[:3]:
    #         journal_data.loc[i, 'Research area 4'] = None
    #     if journal_data.loc[i, 'Research area 5'] in temp_list[:4]:
    #         journal_data.loc[i, 'Research area 5'] = None
    #     if journal_data.loc[i, 'Research area 6'] in temp_list[:5]:
    #         journal_data.loc[i, 'Research area 6'] = None
    #
    # journal_data.to_excel('C:/Users/Administrator/Desktop/jcr_data/journal_data.xlsx', sheet_name='Sheet1', index=False)
    # subject_data.to_excel('C:/Users/Administrator/Desktop/jcr_data/subject_data.xlsx', sheet_name='Sheet1', index=False)
    journal_data = pd.read_excel('C:/Users/Administrator/Desktop/jcr_data/journal_data.xlsx')
    title_data = pd.read_excel('C:/Users/Administrator/Desktop/jcr_data/Abb_article&reference.xlsx')
    journal_data = pd.merge(journal_data, title_data, how='left', left_on='Full Journal Title', right_on='Full title')
    journal_data.to_excel('C:/Users/Administrator/Desktop/jcr_data/journal_data.xlsx', sheet_name='Sheet1', index=False)


def deal18():
    update = pd.read_excel('C:/Users/Administrator/Desktop/更新时间.xlsx')
    school = pd.read_excel('C:/Users/Administrator/Desktop/0716school.xlsx')
    result = pd.merge(school, update, on='id')
    result.to_excel('C:/Users/Administrator/Desktop/07161.xlsx', sheet_name='Sheet1', index=False)


def deal19():
    df1 = pd.read_excel('C:/Users/Administrator/Desktop/待查数据.xlsx')
    df2 = pd.read_excel('C:/Users/Administrator/Desktop/人才名单_20200628.xlsx')
    df1['person_id'] = df1['person_id'].astype('str')
    df3 = df1.loc[:, ['scopus_id', 'person_id']]
    df3.drop_duplicates(subset=['scopus_id', 'person_id'], inplace=True, ignore_index=True)
    df2['人才编号'] = df2['人才编号'].astype('str')
    df2 = pd.merge(df3, df2, how='left', left_on='person_id', right_on='人才编号')
    df2.sort_values(by=['scopus_id', 'person_id'], inplace=True, ignore_index=True)
    df2.to_excel('C:/Users/Administrator/Desktop/待查数据0729.xlsx', sheet_name='Sheet1', index=False)


if __name__ == '__main__':
    deal16()
