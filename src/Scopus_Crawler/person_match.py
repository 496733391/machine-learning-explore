#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

import requests
import pandas as pd

from src.Scopus_Crawler.scopus_config import headers, ins_url, proxies
from src.Scopus_Crawler.get_data import catch_info


def match(cookies, author_name, author_ins, authorID_list):
    not_matched_one = []
    for author_id in authorID_list:
        url = ins_url % author_id
        print(url)

        passed_exp = requests.get(url, proxies=proxies, headers=headers, timeout=300, cookies=cookies)
        result_list = eval(passed_exp.text)

        institute_list = [i['affiliationName'].replace('  ', ' ').lower().strip() for i in result_list]

        # 匹配的机构中只差一个的
        if len(set(author_ins).difference(set(institute_list))) == 1:
            not_matched_one.append(author_id)

        # 机构完全匹配的
        if len(set(author_ins).difference(set(institute_list))) == 0:
            # 获取文献数量跟引用计数
            doc_num, cite_count = catch_info(author_id)

            # 机构信息转为dataFrame格式
            for element in result_list:
                element['start_year'] = element['dateRange'][0]
                element['end_year'] = element['dateRange'][1]
                element.pop('dateRange')

            aff_df = pd.DataFrame(result_list)
            rename_dict = {'affiliationCity': 'aff_city',
                           'affiliationName': 'aff_name',
                           'affiliationCountry': 'aff_country',
                           'affiliationId': 'aff_id',
                           'affiliationUrl': 'aff_url'}
            aff_df.rename(columns=rename_dict, inplace=True)
            aff_df['scopus_id'] = author_id

            return aff_df, [author_name, author_id, doc_num, cite_count], {}

    print('未找到对应学者记录：', author_name, author_ins)

    return pd.DataFrame(data=None, columns=None), [], {author_name: not_matched_one}


if __name__ == '__main__':
    author_name = 'Chen Jie'
    author_ins = ['Wuhan University', 'Université du Québec à Montréal', 'Université du Québec à Montréal']
    author_ins = [i.lower() for i in author_ins]
    authorID_list = []
    author_id, doc_num, cite_count, institute_list = match(author_name, author_ins, authorID_list)
    print(author_id, doc_num, cite_count, institute_list)
    # sql = 'insert into author_info (name, scopus_id, doc_num, cite_count) values (%s, %s, %s, %s)'
    # dbutil.insert_value(sql, [(author_name, author_id, doc_num, cite_count), (1, 2, 3, 4)])


