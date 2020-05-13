#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

import requests
import json
import pandas as pd

from src.Scopus_Crawler.scopus_config import headers, ins_url, proxies
from src.Scopus_Crawler.get_data import catch_info
from src.config.logConfig import logger_scopus as logger


def match(cookies, author_name, author_ins, authorID_list):
    '''

    :param cookies: dict, cookies信息
    :param author_name: str, 学者姓名
    :param author_ins: list, 学者机构信息
    :param authorID_list: list, scopus学者id集合
    :return: 1、学者机构信息df，2、文献数和引用计数信息list，3、未匹配到所有机构时，只差一个机构的scopus学者id str
    '''
    not_matched_one = []
    for author_id in authorID_list:
        url = ins_url % author_id
        logger.info('----' + url + '----')

        passed_exp = requests.get(url, proxies=proxies, headers=headers, timeout=300, cookies=cookies)
        result_list = eval(passed_exp.text)

        institute_list = [i['affiliationName'].replace('  ', ' ').lower().strip() for i in result_list]

        # 匹配的机构中只差一个的
        if len(set(author_ins).difference(set(institute_list))) == 1:
            logger.info('匹配的机构中只差一个的：%s, %s' % (author_name, author_id))
            not_matched_one.append(author_id)

        # 机构完全匹配的
        if len(set(author_ins).difference(set(institute_list))) == 0:
            logger.info('已找到对应学者记录：%s, %s' % (author_name, author_id))
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

            return aff_df, [author_name, author_id, doc_num, cite_count], ''

    logger.info('未找到对应学者记录：%s, %s', author_name, ';'.join(author_ins))

    return pd.DataFrame(data=None, columns=None), [], author_name + ' : ' + ','.join(not_matched_one) + '\n'


if __name__ == '__main__':
    with open('cookies.json', 'r') as js:
        cookies = json.load(js)

    author_name = 'Chen Jie'
    author_ins = ['Wuhan University', 'Université du Québec à Montréal', 'Université du Québec à Montréal']
    author_ins = [i.lower() for i in author_ins]

    authorID_list = []
    aff_df, basic_info, not_matched_one = match(cookies, author_name, author_ins, authorID_list)
