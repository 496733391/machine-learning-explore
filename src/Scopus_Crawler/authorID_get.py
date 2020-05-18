#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup as bs
import time
import re

from src.Scopus_Crawler.scopus_config import driver_path, search_url
from src.config.logConfig import logger_scopus as logger


def get_id(driver, person_id, name, author_name_zh, institution):
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
    # 打开网页
    driver.get(url)

    authorID_list = []
    # 每页显示200条结果
    try:
        driver.find_element_by_xpath('//span[@class="ui-selectmenu-text" and text()="20"]').click()
        driver.find_element_by_id('ui-id-16').click()
        time.sleep(1)

        soup = bs(driver.page_source, 'lxml')

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

    except Exception as err:
        logger.info('ERROR:%s' % err)
        logger.info('当前作者无搜索结果：软科id：%s, 姓名：%s, %s, 机构：%s' % (person_id, author_name_zh, name, institution))
        raise Exception('private error')

    if not authorID_list:
        logger.info('当前作者无搜索结果：软科id：%s, 姓名：%s, %s, 机构：%s' % (person_id, author_name_zh, name, institution))
        raise Exception('private error')

    return authorID_list


if __name__ == '__main__':
    # 单元测试用
    # 浏览器选项
    options = ChromeOptions()
    # 添加代理地址
    options.add_argument('--proxy-server=202.120.43.93:8059')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/81.0.4044.138 Safari/537.36')

    driver = webdriver.Chrome(driver_path, options=options)

    author_name = 'Cai Liang'
    author_ins = 'fudan university'
    authorID_list = get_id(driver, author_name, author_ins)
    print(authorID_list)
