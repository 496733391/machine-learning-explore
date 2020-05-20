#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from selenium import webdriver
from selenium.webdriver import ChromeOptions

# 浏览器选项
options = ChromeOptions()
# 添加代理地址
options.add_argument('--proxy-server=202.120.43.93:8059')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/81.0.4044.138 Safari/537.36')

# chrome浏览器driver路径
driver_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

# 启动浏览器
driver = webdriver.Chrome(driver_path, options=options)
driver.get('https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al&st1=an&st2=lizhe&orcidId=&affilName=beijing+forestry+university&sid=bcd74feed117cffa8a2e8afaef599991&sot=anl&sdt=anl&sl=64&s=AUTHLASTNAME%28liu%29+AND+AUTHFIRST%28wei%29+AND+AFFIL%28wuhan+university%29&resultsPerPage=200&offset=1&jtp=false&currentPage=1&exactAuthorSearch=true')
driver.get('https://www.scopus.com/author/affilHistory.uri?auId=56425884500')
cookies = driver.get_cookies()
cookies_dict = {}
for element in cookies:
    cookies_dict[element['name']] = element['value']
print(cookies_dict)
driver.close()

