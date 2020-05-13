#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

import requests
from bs4 import BeautifulSoup as bs

from src.Scopus_Crawler.scopus_config import headers, data_url, proxies


def catch_info(author_id):
    url = data_url % author_id
    print(url)
    detail = requests.get(url,
                          proxies=proxies,
                          headers=headers,
                          timeout=300,
                          )

    soup = bs(detail.text, 'lxml')
    doc_element = soup.find('div', class_='panel-body')

    doc_num = doc_element.find('span', class_='fontLarge').text
    cite_count = soup.find(id='totalCiteCount').text

    return doc_num, cite_count


if __name__ == '__main__':
    # 单元测试用
    author_id = '56425884500'
    doc_num, cite_count = catch_info(author_id)
    print(doc_num, cite_count)
