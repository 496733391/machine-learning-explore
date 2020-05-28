#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

import requests
import pandas as pd

from src.Scopus_Crawler.scopus_config import headers, ins_url, proxies, aff_limit_high, aff_limit_low
from src.Scopus_Crawler.get_data import catch_info
from src.config.logConfig import logger_scopus as logger


def match(cookies, person_id, author_name, author_name_zh, author_ins, authorID_list):
    '''

    :param cookies: dict, cookies信息
    :param person_id: 软科学者ID
    :param author_name: str, 学者姓名
    :param author_name_zh: str, 学者姓名,中文
    :param author_ins: list, 学者机构信息,英文名称或scopus_id
    :param authorID_list: list, scopus学者id集合
    :return: 1、学者机构信息df，2、文献数和引用计数信息list，3、未匹配到所有机构时，只差一个机构的scopus学者id str
    '''
    not_matched_one = []
    matched_list = []
    temp_dict = {}
    for author_id in authorID_list:
        url = ins_url % author_id

        passed_exp = requests.get(url, proxies=proxies, headers=headers, timeout=300, cookies=cookies)
        result_list = eval(passed_exp.text)
        # todo 无ID的机构不计入机构数限制
        if (len(result_list) <= aff_limit_high) and (len(result_list) >= aff_limit_low):
            temp_dict[author_id] = result_list
            # 以机构对应的scopus_id匹配
            institute_list = [int(i['affiliationId']) for i in result_list]

            # 匹配的机构中只差一个的
            if len(set(author_ins).difference(set(institute_list))) == 1:
                logger.info('匹配的机构中只差一个的：软科id：%s, 姓名：%s,%s scopus_id：%s' % (person_id, author_name_zh, author_name, author_id))
                not_matched_one.append(author_id)

            # 机构完全匹配的
            if len(set(author_ins).difference(set(institute_list))) == 0:
                logger.info('匹配的记录：软科id：%s, 姓名：%s,%s scopus_id：%s' % (person_id, author_name_zh, author_name, author_id))
                matched_list.append(author_id)

    # 找到一个匹配的结果，直接获取数据
    if len(matched_list) == 1:
        logger.info('匹配成功的记录：软科id：%s, 姓名：%s,%s scopus_id：%s' % (person_id, author_name_zh, author_name, matched_list[0]))
        # 获取文献数量跟引用计数
        basic_info = catch_info(matched_list[0], cookies)
        basic_info['person_id'] = person_id
        basic_info['name'] = author_name
        basic_info['name_zh'] = author_name_zh
        basic_info['current_ins_id'] = author_ins[0]

        ins_result = temp_dict[matched_list[0]]
        # 机构信息转为dataFrame格式
        for element in ins_result:
            element['start_year'] = element['dateRange'][0]
            element['end_year'] = element['dateRange'][1]
            element.pop('dateRange')

        aff_df = pd.DataFrame(ins_result)
        rename_dict = {'affiliationCity': 'aff_city',
                       'affiliationName': 'aff_name',
                       'affiliationCountry': 'aff_country',
                       'affiliationId': 'aff_id',
                       'affiliationUrl': 'aff_url'}
        aff_df.rename(columns=rename_dict, inplace=True)
        aff_df['scopus_id'] = matched_list[0]
        aff_df['person_id'] = person_id
        aff_df['name'] = author_name
        aff_df['name_zh'] = author_name_zh
        aff_df['current_ins_id'] = author_ins[0]

        return aff_df, basic_info, pd.DataFrame(data=None, columns=None), pd.DataFrame(data=None, columns=None)

    # 找到多个匹配的结果，日志输出匹配的scopus_id清单
    elif len(matched_list) > 1:
        logger.info('找到多个匹配的结果：软科id：%s, 姓名：%s,%s,  scopus_id清单：%s'
                    % (person_id, author_name_zh, author_name, matched_list))

        mult_re = pd.DataFrame(pd.Series(matched_list), columns=['matched_id'])
        mult_re['person_id'] = person_id
        mult_re['name'] = author_name
        mult_re['name_zh'] = author_name_zh
        mult_re['current_ins_id'] = author_ins[0]
        return pd.DataFrame(data=None, columns=None), pd.DataFrame(data=None, columns=None), mult_re, pd.DataFrame(data=None, columns=None)

    # 未找到匹配的结果，日志输出相近的结果（机构匹配只相差一个）清单
    else:
        logger.info('未找到对应学者记录,结果相近的清单：软科id：%s, 姓名：%s,%s,  scopus_id清单：%s'
                    % (person_id, author_name_zh, author_name, not_matched_one))
        not_match = pd.DataFrame([{'person_id': person_id, 'name': author_name,
                                   'name_zh': author_name_zh, 'current_ins_id': author_ins[0]}])
        return pd.DataFrame(data=None, columns=None), pd.DataFrame(data=None, columns=None), pd.DataFrame(data=None, columns=None), not_match


if __name__ == '__main__':
    pass
