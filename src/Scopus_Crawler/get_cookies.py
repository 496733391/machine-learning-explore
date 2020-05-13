#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json
base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from selenium import webdriver
from selenium.webdriver import ChromeOptions

from src.Scopus_Crawler.scopus_config import driver_path


def get_cookies(driver):
    driver.get('https://www.scopus.com/author/affilHistory.uri?auId=56425884500')
    driver.get('https://www.scopus.com/author/affilHistory.uri?auId=56425884500')
    cookies = driver.get_cookies()
    cookies_dict = {}
    for element in cookies:
        cookies_dict[element['name']] = element['value']
    driver.close()

    cookies_json = json.dumps(cookies_dict, indent=4)
    with open('cookies.json', 'w') as js:
        js.write(cookies_json)

    return cookies_dict


if __name__ == '__main__':
    # 单元测试用
    # 浏览器选项
    options = ChromeOptions()
    # 添加代理地址
    options.add_argument('--proxy-server=202.120.43.93:8059')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/81.0.4044.138 Safari/537.36')

    driver = webdriver.Chrome(driver_path, options=options)
    cookies = get_cookies(driver)
