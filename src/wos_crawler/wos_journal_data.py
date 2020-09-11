#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import requests
from selenium import webdriver
import pandas as pd
import json

from src.Scopus_Crawler.scopus_config import headers, proxies, driver_path
from src.Scopus_Crawler.get_cookies import get_cookies
from src.Scopus_Crawler.data_write import write2sql
from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password

# 浏览器选项
options = webdriver.ChromeOptions()
# 添加代理地址和header
options.add_argument('--proxy-server=202.120.43.93:8059')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/81.0.4044.138 Safari/537.36')

base_url = 'https://jcr.clarivate.com/AllCategoriesJson.action?_dc=1597229885149&jcrYear=2019' \
           '&edition=SSCI' \
           '&subjectCategoryScheme=WoS&page=1&start=0&limit=25'

journal_data_url = 'https://jcr.clarivate.com/JournalHomeGridJson.action?_dc=1597233012104&jcrYear=2019' \
                   '&edition={}' \
                   '&categoryIds={}' \
                   '&subjectCategoryScheme=WoS&jifQuartile=&impactFactorRangeFrom=&impactFactorRangeTo=&averageJifP' \
                   'ercentileRangeFrom=&averageJifPercentileRangeTo=&OAFlag=N&page=1&start=0&limit=10000' \
                   '&sort=%5B%7B%22property%22%3A%22journalImpactFactor%22%2C%22direction%22%3A%22DESC%22%7D%5D'

post_url = 'https://incites.clarivate.com/incites-app/explore/0/organization/data/table/page'

login_url = 'https://login.incites.clarivate.com/?DestApp=IC2&locale=en_US&Alias=IC2'
login_data = 'username=496733391%40qq.com&password=liang950113ZOU%21&IPStatus=IPValid'
headers_login = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                              'e/81.0.4044.138 Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded'
}


post_data = {"take": 100000, "skip": 0, "sortBy": "timesCited", "sortOrder": "desc",
             "indicators": ["key", "seqNumber", "orgName", "rank", "wosDocuments", "norm", "timesCited",
                            "percentCited", "hasProfile"],
             "filters": {"orgtype": {"is": ["Academic"]}, "location": {"is": ["CHINA MAINLAND"]},
                         "personIdTypeGroup": {"is": "name"}, "personIdType": {"is": "fullName"},
                         "schema": {"is": "Web of Science"}, "sbjname": {"is": ["ACOUSTICS"]},
                         "jrnname": {"is": ["ACOUSTICS AUSTRALIA"]}, "publisherType": {"is": "All"},
                         "articletype": {"is": ["Article"]}, "period": {"is": [2015, 2015]}}, "pinned": []}


def start_driver():
    # 启动浏览器
    driver = webdriver.Chrome(driver_path, options=options)
    return driver


def get_subject_data():
    # 启动浏览器并获取cookies
    driver = start_driver()
    cookies = get_cookies(driver, url=base_url)
    driver.close()
    subject_info = requests.get(journal_data_url, proxies=proxies, headers=headers, timeout=300, cookies=cookies).json()
    df = pd.DataFrame(data=subject_info['data'])
    df['group'] = 'SSCI'
    df.to_excel('C:/Users/Administrator/Desktop/SSCI.xlsx', index=False)


def get_journal_data(input_data):
    count = 0
    result_df_list = []
    while count < len(input_data):
        # 启动浏览器并获取cookies
        driver = start_driver()
        cookies = get_cookies(driver, url=base_url)
        driver.close()
        try:
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                url = journal_data_url.format(input_data[i][2], input_data[i][0])
                data_info = requests.get(url, proxies=proxies, headers=headers,
                                         timeout=300, cookies=cookies).json()
                data = []
                for ele in data_info['data']:
                    del ele['cites']
                    del ele['articles']
                    data.append(ele)

                data_df = pd.DataFrame(data=data)
                data_df['category_name'] = input_data[i][1]
                data_df['category_id'] = input_data[i][0]
                result_df_list.append(data_df)

            count = len(input_data)

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            count = i

    all_data_df = pd.concat(result_df_list)
    all_data_df.to_excel('C:/Users/Administrator/Desktop/wos_journal_data.xlsx', index=False)


def get_doc_data(input_data):
    headers['content-type'] = 'application/json'
    count = 0
    while count < len(input_data):
        result_df_list = []
        try:
            session = requests.session()
            session.post(url=login_url, data=login_data, proxies=proxies, headers=headers_login, timeout=300)
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                for year in range(2015, 2020):
                    post_data['filters']['sbjname']['is'] = input_data[i][0][1]
                    post_data['filters']['jrnname']['is'] = input_data[i][1]
                    post_data['filters']['period']['is'] = [year, year]
                    doc_data = session.post(url=post_url, data=json.dumps(post_data), headers=headers,
                                            proxies=proxies, timeout=300).json()
                    if doc_data['items']:
                        for item in doc_data['items']:
                            item['doc_num'] = item['wosDocuments']['value']
                            del item['wosDocuments']

                        data_df = pd.DataFrame(data=doc_data['items'])
                        data_df['year'] = year
                        data_df['category_id'] = input_data[i][0][0]
                        data_df['category_name'] = input_data[i][0][1]
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
            write2sql([['wos_doc_data_copy', all_data_df]])


if __name__ == '__main__':
    # dbutil = DBUtil(host, port, database, username, password)
    # sql = 'select category_id, category_name, edition from wos_subject'
    # input_df = dbutil.get_allresult(sql, 'df')
    # dbutil.close()
    # input_data = input_df.values.tolist()
    # get_journal_data(input_data)

    dbutil = DBUtil(host, port, database, username, password)
    sql = 'select journalTitle, category_name, edition, category_id from wos_journal_data where flag="Q1"'
    input_df = dbutil.get_allresult(sql, 'df')
    input_df['journalTitle'] = input_df['journalTitle'].str.upper()
    dbutil.close()

    input_df = pd.read_excel('C:/Users/Administrator/Desktop/wos_journal_data.xlsx')
    input_df['journalTitle'] = input_df['journalTitle'].str.upper()

    # df2 = pd.read_excel('C:/Users/Administrator/Desktop/cssc-category-mapping.xlsx', sheet_name='Sheet1')
    # df2['id'] = df2['id'].astype('str')
    # for i in range(len(df2)):
    #     if len(df2.loc[i, 'id']) < 4:
    #         df2.loc[i, 'id'] = '0' + df2.loc[i, 'id']

    # input_df = pd.merge(input_df, df2, on='category_id')

    input_data = []
    # for value, sub_df in input_df.groupby(['id', 'Description']):
    for value, sub_df in input_df.groupby(['category_id', 'category_name', 'edition']):
        # input_data.append([value, list(sub_df['journalTitle']), list(set(sub_df['category_name']))])
        input_data.append([value, list(sub_df['journalTitle'])])

    get_doc_data(input_data)

