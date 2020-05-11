#! /usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
import re

first_name = 'liu'
last_name = 'bo'
institute = '+'.join(['wuhan', 'university'])

# scopus检索网页
url = 'https://www.scopus.com/results/authorNamesList.uri?origin=searchauthorlookup&src=al&edit=&poppUp=&' \
      'basicTab=&affiliationTab=&advancedTab=&st1={}&st2={}&institute={}&orcidId=&authSubject=LFSC&_authSub' \
      'ject=on&authSubject=HLSC&_authSubject=on&authSubject=PHSC&_authSubject=on&authSubject=SOSC&_authSubj' \
      'ect=on&s=AUTHLASTNAME%28liu%29+AND+AUTHFIRST%28bo%29&sdt=al&sot=al&searchId=42a0860e2008958faf4e6c64' \
      '4b496275&exactSearch=on&sid=42a0860e2008958faf4e6c644b496275'.format(first_name, last_name, institute)
# chrome浏览器driver路径
driver_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
# 浏览器选项
options = ChromeOptions()
# 添加代理地址
options.add_argument('--proxy-server=202.120.43.93:8059')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/81.0.4044.138 Safari/537.36')
# 启动浏览器
driver = webdriver.Chrome(driver_path, options=options)
# 打开网页，等待2s
driver.get(url)

try:
    driver.find_element_by_id('_pendo-close-guide_').click()
except Exception:
    pass

# 每页显示200条结果
driver.find_element_by_xpath('//span[@class="ui-selectmenu-text" and text()="20"]').click()
driver.find_element_by_id('ui-id-16').click()
time.sleep(1)
authorID_list = re.findall('authorId=([0-9]+)', driver.page_source)
