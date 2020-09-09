#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import json

from src.Scopus_Crawler.scopus_config import headers, proxies
from src.Scopus_Crawler.data_write import write2sql
from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password


post_url_base = 'https://incites.clarivate.com/incites-app/explore/%s/organization/data/table/page'

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


def get_doc_data(input_data, school, value):
    headers['content-type'] = 'application/json'
    post_url = post_url_base % value[1]
    if school == 'Chinese Academy of Medical Sciences - Peking Union Medical College':
        del post_data['filters']['orgtype']
    count = 0
    while count < len(input_data):
        result_df_list = []
        try:
            session = requests.session()
            session.post(url=login_url, data=login_data, proxies=proxies, headers=headers_login, timeout=300)
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                for year in range(2015, 2020):
                    # post_data['filters']['sbjname']['is'] = input_data[i][2]
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
                        data_df['edition'] = input_data[i][0][2]
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
            all_data_df = all_data_df.loc[all_data_df['orgName'] == value[0]]
            all_data_df['orgName'] = school
            # write2sql([['wos_doc_data_copy', all_data_df]])
            write2sql([['wos_doc_data', all_data_df]])


if __name__ == '__main__':
    dbutil = DBUtil(host, port, database, username, password)
    sql = 'select journalTitle, category_name, edition, category_id from wos_journal_data where flag="Q1"'
    input_df = dbutil.get_allresult(sql, 'df')
    input_df['journalTitle'] = input_df['journalTitle'].str.upper()
    dbutil.close()

    # df2 = pd.read_excel('C:/Users/Administrator/Desktop/cssc-category-mapping.xlsx', sheet_name='Sheet1')
    # df2['id'] = df2['id'].astype('str')
    # for i in range(len(df2)):
    #     if len(df2.loc[i, 'id']) < 4:
    #         df2.loc[i, 'id'] = '0' + df2.loc[i, 'id']
    #
    # input_df = pd.merge(input_df, df2, on='category_id')

    input_data = []
    # for value, sub_df in input_df.groupby(['id', 'Description']):
    for value, sub_df in input_df.groupby(['category_id', 'category_name', 'edition']):
        # input_data.append([value, list(sub_df['journalTitle']), list(set(sub_df['category_name']))])
        input_data.append([value, list(sub_df['journalTitle'])])

    school_dict = {'China University of Geosciences(Beijing)':
                   ['China University of Geosciences', '5a03a409-513b-4db8-ad43-31d2c3e9f5db'],
                   'China University of Geosciences(Wuhan)':
                   ['China University of Geosciences', '7b5de7a9-2641-4e23-a118-2c83d56d6a5c'],
                   'China University of Petroleum(Beijing)':
                   ['China University of Petroleum', 'ffb5a986-c76a-4d11-86fc-dca038694452'],
                   'China University of Petroleum(Qingdao)':
                   ['China University of Petroleum', 'd0f07501-f876-45c9-b121-85efdf742468'],
                   'China University of Mining & Technology(Xuzhou)':
                   ['China University of Mining & Technology', '9a9f5022-7d44-413f-a8ce-6173bdb7c8fc'],
                   'China University of Mining & Technology(Beijing)':
                   ['China University of Mining & Technology', '3a104a0a-69f0-4a6d-afa7-b41871ba739b'],
                   'Chinese Academy of Medical Sciences - Peking Union Medical College':
                   ['Chinese Academy of Medical Sciences - Peking Union Medical College',
                    'd887bf41-4950-4b9b-a40c-604df4ae9c70']}

    for school, value in school_dict.items():
        get_doc_data(input_data, school, value)

