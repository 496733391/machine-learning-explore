#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

from src.Scopus_Crawler.scopus_config import headers, data_url, proxies


# def catch_info(author_id):
#     url = data_url % author_id
#     detail = requests.get(url,
#                           proxies=proxies,
#                           headers=headers,
#                           timeout=300,
#                           )
#
#     soup = bs(detail.text, 'lxml')
#     doc_element = soup.find('div', class_='panel-body')
#
#     doc_num = doc_element.find('span', class_='fontLarge').text
#     cite_count = soup.find(id='totalCiteCount').text
#
#     return doc_num, cite_count


def catch_info(author_id, cookies):
    url = data_url % author_id
    detail = requests.get(url, proxies=proxies, headers=headers, timeout=300, cookies=cookies)
    doc_year = re.findall(r'Tooltip":"([0-9]+ ,[0-9]+),doc', detail.text)
    cite_year = re.findall(r'Tooltip":"([0-9]+ ,[0-9]+),cita', detail.text)
    doc_df = pd.DataFrame(data=[i.split(' ,') for i in doc_year], columns=['year', 'doc_num_byear'])
    if len(cite_year) > 0:
        cite_df = pd.DataFrame(data=[i.split(' ,') for i in cite_year], columns=['year', 'cite_count_byear'])
        result_df = pd.merge(doc_df, cite_df, on='year', how='outer').fillna(0)
    else:
        doc_df['cite_count_byear'] = 0
        result_df = doc_df

    result_df['scopus_id'] = author_id

    return result_df


if __name__ == '__main__':
    # 单元测试用
    author_id = '56425884500'
    result_df = catch_info(author_id)
