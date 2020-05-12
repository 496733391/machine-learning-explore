#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

import requests
import pandas as pd
import re

from src.Scopus_Crawler.scopus_config import cookie, headers, ins_url, proxies
from src.Scopus_Crawler.scopus_config import host, port, database, username, password
from src.Scopus_Crawler.authorID_get import get_id
from src.Scopus_Crawler.get_data import catch_info
from src.Scopus_Crawler.update_cookies import update_cookies
from src.config.DBUtil import DBUtil


def match(author_name, author_ins, authorID_list):
    for author_id in authorID_list:
        url = ins_url % author_id
        print(url)
        try:
            passed_exp = requests.get(url,
                                      proxies=proxies,
                                      headers=headers,
                                      timeout=300,
                                      cookies=cookie
                                      )
            result_list = eval(passed_exp.text)
        except Exception:
            update_cookies()
            raise Exception('cookies已更新，请重新运行')

        institute_list = [i['affiliationName'].replace('  ', ' ').lower().strip() for i in result_list]
        print(institute_list, '\n')
        # institute_list = [re.sub(r'\s{2,}', ' ', i['affiliationName'].lower().strip()) for i in result_list]
        if len(set(author_ins).difference(set(institute_list))) == 1:
            print('只差一个的:', author_name, author_id, author_ins, institute_list,
                  list(set(author_ins).difference(set(institute_list))))
        if len(set(author_ins).difference(set(institute_list))) == 0:
            doc_num, cite_count = catch_info(author_id)
            return author_id, doc_num, cite_count, institute_list

    print('未找到对应学者记录：', author_name, author_ins)


if __name__ == '__main__':
    author_name = 'Chen Jie'
    author_ins = ['Wuhan University', 'Université du Québec à Montréal', 'Université du Québec à Montréal']
    author_ins = [i.lower() for i in author_ins]
    authorID_list = get_id(author_name, author_ins[0])
    author_id, doc_num, cite_count, institute_list = match(author_name, author_ins, authorID_list)
    print(author_id, doc_num, cite_count, institute_list)
    dbutil = DBUtil(host, port, database, username, password)
    sql = 'insert into author_info (name, scopus_id, doc_num, cite_count) values (%s, %s, %s, %s)'
    dbutil.insert_value(sql, [(author_name, author_id, doc_num, cite_count), (1, 2, 3, 4)])
    dbutil.execute_commit()
    dbutil.close()

