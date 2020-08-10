#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import pandas as pd

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

apikey_list = ['2e63a421d8a260ed9b4f2403f0f6d5db', '20ca1709b7822de4cf70fb2e31e2ac0a',
               '4907f2ddcf925c9f7216aea58e164571', 'e5f9556e1909cc04391a81799355b1b4',
               'd8517c2e251906b5e3ae833e6b619e30']

base_url = 'https://api.elsevier.com/content/search/scopus?' \
           'query=AU-ID({})%20and%20FIRSTAUTH({})' \
           '&apiKey=4907f2ddcf925c9f7216aea58e164571' \
           '&start={}' \
           '&count=25'


def get_article(input_data):
    count = 0
    while count < len(input_data):
        all_person_data_list = []
        try:
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                for j in range(1000):
                    url = base_url.format(input_data[i][1], input_data[i][2], str(j*25))
                    author_article_info = requests.get(url=url, proxies=proxies, headers=headers).json()
                    if 'service-error' in author_article_info:
                        print(input_data[i][2])
                        break

                    if 'entry' not in author_article_info['search-results']:
                        break

                    if 'error' in author_article_info['search-results']['entry'][0]:
                        break

                    for article_dict in author_article_info['search-results']['entry']:
                        doi = article_dict.get('prism:doi', '')
                        eid = article_dict.get('eid', '')
                        scopus_article_id = article_dict['dc:identifier'][10:]
                        publish_year = article_dict.get('prism:coverDate', '')
                        all_person_data_list.append([input_data[i][0], input_data[i][1], doi,
                                                     publish_year, eid, scopus_article_id])

            count = len(input_data)

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            count = i

        if all_person_data_list:
            result_df = pd.DataFrame(data=all_person_data_list, columns=['person_id', 'scopus_id', 'doi',
                                                                         'publish_year', 'eid', 'scopus_article_id'])
            write2sql([['scopus_author_article', result_df]])


if __name__ == '__main__':
    dbutil = DBUtil(host, port, database, username, password)
    sql = "select person_id, scopus_id, name from scopus_author_name where person_id " \
          "not in (select person_id from scopus_author_article)"
    df = dbutil.get_allresult(sql, 'df')
    dbutil.close()

    input_data = df.values.tolist()
    get_article(input_data)
