#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pymysql
import requests
from selenium import webdriver
import pandas as pd
import json

from src.Scopus_Crawler.scopus_config import headers, proxies, driver_path
from src.Scopus_Crawler.get_cookies import get_cookies
from src.Scopus_Crawler.data_write import write2sql
from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password


login_url = 'https://login.incites.clarivate.com/?DestApp=IC2&locale=en_US&Alias=IC2'
login_data = 'username=529483331%40qq.com&password=Qizhaowen%40199479&IPStatus=IPValid'
headers_login = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                  'e/81.0.4044.138 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded'
}

post_url_base = 'https://incites.clarivate.com/incites-app/drilldowns/0/organization/dbd_39/data?' \
                  'key={}&dataColumn=jifdocsq1&skip=0&take=10000&sortBy=undefined&sortOrder=undefined' \
                  '&citedOrCiting=undefined&isSourceYear=undefined'

post_data_detail = {"filters": {"location": {"is": ["CHINA MAINLAND"]}, "personIdTypeGroup": {"is": "name"},
                                "personIdType": {"is": "fullName"}, "schema": {"is": "China SCADC Subject 97 Narrow"},
                                "sbjname": {"is": ["0101 Philosophy"]}, "publisherType": {"is": "All"},
                                "fundingAgencyType": {"is": "All"}, "articletype": {"is": ["Article"]}}, "pinned": []}


def get_doc_data(input_data):
    headers['content-type'] = 'application/json'
    count = 0
    while count < len(input_data):
        result_df_list = []
        try:
            session = requests.session()
            session.post(url=login_url, data=login_data, headers=headers_login, timeout=300)
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                post_url = post_url_base.format(input_data[i][1])
                post_data_detail['filters']['sbjname']['is'] = input_data[i][3] + ' ' + input_data[i][4]
                doc_data = session.post(url=post_url, data=json.dumps(post_data_detail), headers=headers, timeout=300).json()
                if doc_data['items']:
                    for item in doc_data['items']:
                        item['title'] = item['a']['title']
                        del item['a']

                    data_df = pd.DataFrame(data=doc_data['items'])
                    data_df['category_id'] = input_data[i][3]
                    data_df['category_name'] = input_data[i][4]
                    data_df['orgName'] = input_data[i][0]
                    result_df_list.append(data_df)

            count = len(input_data)
            session.close()

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            session.close()
            count = i

        if result_df_list:
            all_data_df = pd.concat(result_df_list)
            write2sql([['wos_doc_data_detail', all_data_df]])


if __name__ == '__main__':
    dbutil = DBUtil(host, port, database, username, password)
    sql = 'select orgName, `key`, year, category_id, category_name from wos_doc_data_copy'
    input_df = dbutil.get_allresult(sql, 'df')
    input_df.drop_duplicates(subset=['orgName', 'key', 'category_id', 'category_name'], inplace=True)
    dbutil.close()

    input_data = input_df.values.tolist()

    for rdd in range(9):
        get_doc_data(input_data[5000*rdd:5000*rdd+5000])
