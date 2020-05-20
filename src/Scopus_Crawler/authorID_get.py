#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

from bs4 import BeautifulSoup as bs
import re
import requests

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from src.Scopus_Crawler.scopus_config import headers, search_url, proxies
from src.config.logConfig import logger_scopus as logger


def get_id(person_id, name, author_name_zh, institution):
    logger.info('当前搜索：软科id：%s, 姓名：%s, %s, 机构：%s' % (person_id, author_name_zh, name, institution))
    # 将姓名拆分为list
    name_list = re.split(r'\s+', name)
    first_name = name_list[0].lower()
    last_name = name_list[1].lower()
    # 将机构名称拆分为list
    institute_list = re.split(r'\s+', institution)
    institute = '+'.join(institute_list).lower()
    # scopus检索网页
    url = search_url.format(first_name, last_name, institute)
    # 请求网页
    page_source = requests.get(url, proxies=proxies, headers=headers, timeout=300)
    soup = bs(page_source.text, 'lxml')

    authorID_list = []
    # 只匹配链接中的人名
    name_matched = soup.find_all('a', class_='docTitle')
    for element in name_matched:
        scopus_text_list = element.text.replace('–', '').replace('\'', '').strip().split(' ')
        scopu_text = scopus_text_list[0] + ' ' + ''.join(scopus_text_list[1:])
        if scopu_text.lower() == ', '.join(name_list).lower():
            author_id = re.findall(r'authorId=([0-9]+)', element.attrs['href'])
            authorID_list.extend(author_id)
    # 如果上一步骤无匹配的结果，则链接中的人名与其它写法都进行匹配
    if not authorID_list:
        search_list = soup.find_all('tr', class_='searchArea')
        for search_result in search_list:
            title_name = search_result.find('a', class_='docTitle')
            if title_name:
                text_list = [title_name.text]
                other_name = search_result.find_all('div', class_='txtSmaller')
                for element in other_name:
                    text_list.append(element.text)

                for text in text_list:
                    one_text_lis = text.replace('–', '').replace('\'', '').strip().split(' ')
                    one_text = one_text_lis[0] + ' ' + ''.join(one_text_lis[1:])
                    if one_text.lower() == ', '.join(name_list).lower():
                        author_id = re.findall(r'authorId=([0-9]+)', title_name.attrs['href'])
                        authorID_list.extend(author_id)
                        break

    return authorID_list


if __name__ == '__main__':
    pass
