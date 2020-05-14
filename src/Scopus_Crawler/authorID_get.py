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


def get_id(driver, name, institution):
    logger.info('当前搜索：姓名：%s，机构：%s' % (name, institution))
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

    try:
        driver.find_element_by_id('_pendo-close-guide_').click()
    except Exception:
        pass

    # 每页显示200条结果
    driver.find_element_by_xpath('//span[@class="ui-selectmenu-text" and text()="20"]').click()
    driver.find_element_by_id('ui-id-16').click()
    time.sleep(1)

    soup = bs(driver.page_source, 'lxml')
    name_matched = soup.find_all('a', class_='docTitle')
    authorID_list = []
    for element in name_matched:
        if element.text.strip().lower() == ', '.join(name_list).lower():
            author_id = re.findall(r'authorId=([0-9]+)', element.attrs['href'])
            authorID_list.extend(author_id)

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
