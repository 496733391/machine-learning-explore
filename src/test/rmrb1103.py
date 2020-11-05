#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import pandas as pd
from selenium import webdriver

from src.Scopus_Crawler.scopus_config import headers, proxies, driver_path

# 浏览器选项
options = webdriver.ChromeOptions()
# 添加代理地址和header
options.add_argument('--proxy-server=202.120.43.93:8059')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/81.0.4044.138 Safari/537.36')

driver = webdriver.Chrome(driver_path, options=options)
driver.get('http://www.apabi.com/sjtu/?pid=newspaper.page&issueid=nq.D110000renmrb_20151101&cult=CN')

cookies = driver.get_cookies()
cookies_dict = {}
for element in cookies:
    cookies_dict[element['name']] = element['value']
driver.close()

year_list = ['2015', '2016', '2017', '2018', '2019']
month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
day_list = month_list + [str(i) for i in list(range(13, 32))]

rmrb_url = 'http://www.apabi.com/sjtu/?pid=newspaper.page&issueid=nq.D110000renmrb_%s%s%s&cult=CN'

result_list = []
for year in year_list:
    for month in month_list:
        for day in day_list:
            print(year, month, day)
            url = rmrb_url % (year, month, day)
            page = requests.get(url=url, headers=headers, proxies=proxies, cookies=cookies_dict)
            if page.status_code == 200:
                page_link = re.findall(r'''<dt><a href="(.*?)" title=".*?"><input class="newsMetaid".*?</a></dt>''', page.text)
                page_text = re.findall(r'''<dt><a href=".*?" title="(.*?)"><input class="newsMetaid".*?</a></dt>''', page.text)
                domain_url = 'http://www.apabi.com/sjtu/'
                page_link = [domain_url + k for k in page_link]
                df = pd.DataFrame({'版块': page_text, '链接': page_link})
                df['date'] = year + month + day
                result_list.append(df)

rmrb_df = pd.concat(result_list)
rmrb_df.to_excel('C:/Users/Administrator/Desktop/1103人民日报.xlsx', sheet_name='Sheet1', index=False)
