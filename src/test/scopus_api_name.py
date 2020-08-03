#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import requests

from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password
from src.Scopus_Crawler.data_write import write2sql

proxies = {
            "http": "http://202.120.43.93:8059"
}

# headers
headers = {
            'Accept': 'application/json'
}

base_url = 'https://api.elsevier.com/content/search/author?query=AU-ID(%s)&apiKey=7f59af901d2d86f78a1fd60c1bf9426a'


def get_name(input_data):
    count = 0
    while count < len(input_data):
        all_person_data_list = []
        try:
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                url = base_url % input_data[i][1]
                author_info = requests.get(url=url, proxies=proxies, headers=headers).json()
                author_name = author_info['search-results']['entry'][0]['preferred-name']['surname'] + ' ' + \
                              author_info['search-results']['entry'][0]['preferred-name']['initials']
                all_person_data_list.append([input_data[i][0], input_data[i][1], author_name])

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            count = i


if __name__ == '__main__':
    dbutil = DBUtil(host, port, database, username, password)
    sql = "select distinct person_id, scopus_id from author_info_new where person_id " \
          "not in (select person_id from scopus_author_name) and flag!=0"
    df = dbutil.get_allresult(sql, 'df')
    dbutil.close()

    input_data = df.values.tolist()
    get_name(input_data)
