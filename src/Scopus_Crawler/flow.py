#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from selenium import webdriver
import pandas as pd
from selenium.webdriver import ChromeOptions
import datetime
import random

from src.Scopus_Crawler.scopus_config import driver_path, search_url
from src.Scopus_Crawler.get_cookies import get_cookies
from src.Scopus_Crawler.authorID_get import get_id
from src.Scopus_Crawler.person_match import match
from src.Scopus_Crawler.data_write import write2sql
from src.config.logConfig import logger_scopus as logger
from src.Scopus_Crawler.data_process import data_process, data_process2

# 浏览器选项
options = ChromeOptions()
# 添加代理地址和header
options.add_argument('--proxy-server=202.120.43.93:8059')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/81.0.4044.138 Safari/537.36')


def start_driver():
    # 启动浏览器
    driver = webdriver.Chrome(driver_path, options=options)

    return driver


def main_prog(input_data):
    '''

    :param input_data: [{'person_id':1234564, 'name':'liu bo', 'ins':['fudan university', 'xx university', 'xxx university'],
                        'ins_id':[111, 222, 333], 'name_zh':'刘博'}, {...}]
    :return:
    '''
    data_no = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(10, 99))
    logger.info('数据版本号: %s' % data_no)
    count = 0
    while count < len(input_data):
        all_aff_df = pd.DataFrame(data=None, columns=None)
        basic_info_df = pd.DataFrame(data=None, columns=None)
        mult_result_df = pd.DataFrame(data=None, columns=None)
        not_matched_df = pd.DataFrame(data=None, columns=None)
        # 启动浏览器并获取cookies
        driver = start_driver()
        cookies = get_cookies(driver)
        driver.close()
        try:
            # 开始对每位学者再scopus上进行匹配和信息获取
            for i in range(count, len(input_data)):
                person_id = input_data[i]['person_id']
                author_name = input_data[i]['name']
                author_name_zh = input_data[i]['name_zh']
                author_ins = input_data[i]['ins']
                author_ins_id = input_data[i]['ins_id']
                logger.info('当前进度：软科id：%s, 姓名：%s,%s' % (person_id, author_name_zh, author_name[0]))
                # 机构英文名称全部转为小写
                author_ins = [i.lower() for i in author_ins]

                # todo 0624临时修改
                # authorID_list = get_id(person_id, author_name, author_name_zh, author_ins[0])
                authorID_list = []
                for _name in author_name:
                    for _ins in author_ins:
                        authorID_list.extend(get_id(person_id, _name, author_name_zh, _ins))
                        if authorID_list:
                            break
                    if authorID_list:
                        break

                # 以机构对应的scopus_id匹配
                aff_df, basic_info, mult_re, not_match = match(cookies, person_id, author_name, author_name_zh,
                                                               author_ins_id, authorID_list)

                all_aff_df = all_aff_df.append(aff_df, ignore_index=True)
                basic_info_df = basic_info_df.append(basic_info, ignore_index=True)
                mult_result_df = mult_result_df.append(mult_re, ignore_index=True)
                not_matched_df = not_matched_df.append(not_match, ignore_index=True)

            # 结束循环
            count = len(input_data)

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            logger.info('ERROR:%s' % err)
            logger.info('当前进度：%s / %s' % (i+1, len(input_data)))
            count = i

        # 添加data_no字段
        for df in [all_aff_df, basic_info_df, mult_result_df, not_matched_df]:
            if len(df) > 0:
                df['data_no'] = data_no
        # 将已完成的部分进行数据写入
        write2sql([['author_info_new', basic_info_df], ['author_exp', all_aff_df],
                   ['mult_matched_author', mult_result_df], ['not_matched_author', not_matched_df]])


def temp(input_data):
    from src.config.DBUtil import DBUtil
    from src.Scopus_Crawler.scopus_config import host, port, database, username, password

    dbutil = DBUtil(host, port, database, username, password)
    sql = "SELECT person_id FROM author_info_new UNION SELECT person_id FROM mult_matched_author UNION SELECT " \
          "person_id FROM not_matched_author"
    df = dbutil.get_allresult(sql, 'df')
    dbutil.close()
    input_list = [str(i['person_id']) for i in input_data]
    diff = set(input_list).difference(set(df['person_id']))
    out_data = [i for i in input_data if str(i['person_id']) in diff]
    return out_data


if __name__ == '__main__':
    logger.info('********START********')
    logger.info('*********************')
    # 测试用，从本地excel中读数据
    # input_df = pd.read_excel('C:/Users/Administrator/Desktop/1-data20200702.xlsx')

    input_df = pd.read_excel('C:/Users/Administrator/Desktop/物理学人才清单_20200908.xlsx', sheet_name='Sheet2')
    input_df = input_df.loc[input_df['scopus机构ID'] != 0]
    input_df.rename(columns={'人才编号': 'person_id',
                             '姓名': 'name',
                             '英文名称': 'ins_en',
                             'scopus机构ID': 'aff_id'}, inplace=True)
    # 第二轮检索
    # first_not_matched = pd.read_excel('C:/Users/Administrator/Desktop/not_matched0701.xlsx')
    # input_df = pd.merge(input_df, first_not_matched, on='person_id')

    input_data = data_process2(input_df)

    # input_data = temp(input_data)

    main_prog(input_data)
    logger.info('*********END*********')
    logger.info('*********************')
