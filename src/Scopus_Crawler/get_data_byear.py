#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import requests
import re

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from src.Scopus_Crawler.scopus_config import headers, proxies
from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password

cookies_dict = {
    "AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg": "1075005958%7CMCIDTS%7C18398%7CMCMID%7C10394718433892749470441349151435529195%7CMCAAMLH-1590126415%7C11%7CMCAAMB-1590126415%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589528816s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-18405%7CvVersion%7C4.4.1",
    "s_sess": "%20e41%3D1%3B%20s_cpc%3D1%3B%20s_cc%3Dtrue%3B",
    "AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg": "1",
    "AWSELB": "CB9317D502BF07938DE10C841E762B7A33C19AADB15C8FD0598CF175B6FA51BC89CCC52E73B1C9F31FEF25EE745B461328A50F1497A31AAC5A6BDE3E4B4DACF34F3854CEEB4D17C7E9C8E95F300E46E30B28FCE797",
    "scopus.machineID": "0C3E0F5C649ED5D199AE9BDF700B1DFE.wsnAw8kcdt7IPYLO0V48gA",
    "scopusSessionUUID": "bd1d5e97-dbc2-4b41-8",
    "SCSessionID": "0C3E0F5C649ED5D199AE9BDF700B1DFE.wsnAw8kcdt7IPYLO0V48gA",
    "s_pers": "%20v8%3D1589521616312%7C1684129616312%3B%20v8_s%3DFirst%2520Visit%7C1589523416312%3B%20c19%3Dsc%253Aerror%253A404%7C1589523416320%3B%20v68%3D1589521615023%7C1589523416329%3B",
    "__cfduid": "d3bcf7dc446bbf984c4b2e76be7f7a4a11589521612"
}


def crawl_info(author_id):
    url = 'https://www.scopus.com/author/highchart.uri?authorId=%s' % author_id[0]
    print(url)
    detail = requests.get(url, proxies=proxies, headers=headers, timeout=300, cookies=cookies_dict)
    doc_year = re.findall(r'Tooltip":"([0-9]+ ,[0-9]+),doc', detail.text)
    cite_year = re.findall(r'Tooltip":"([0-9]+ ,[0-9]+),cita', detail.text)
    doc_df = pd.DataFrame(data=[i.split(' ,') for i in doc_year], columns=['year', 'doc_num_byear'])
    if len(cite_year) > 0:
        cite_df = pd.DataFrame(data=[i.split(' ,') for i in cite_year], columns=['year', 'cite_count_byear'])
        result_df = pd.merge(doc_df, cite_df, on='year', how='outer').fillna(0)
    else:
        doc_df['cite_count_byear'] = 0
        result_df = doc_df

    result_df['scopus_id'] = author_id[0]
    result_df['person_id'] = author_id[1]

    return result_df


if __name__ == '__main__':
    # 单元测试用
    dbutil = DBUtil(host, port, database, username, password)
    author_id_list = dbutil.get_allresult('select scopus_id, person_id from author_info')

    all_re = pd.DataFrame(data=None, columns=None)
    try:
        for i, author_id in enumerate(author_id_list[1747:]):
            all_re = all_re.append(crawl_info(author_id), ignore_index=True)

    except Exception as err:
        print(i)
        print(err)

    dbutil.df_insert('author_info_new', all_re)
    dbutil.close()
