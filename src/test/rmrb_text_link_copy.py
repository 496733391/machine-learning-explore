#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import pandas as pd
from selenium import webdriver

from src.Scopus_Crawler.scopus_config import headers, proxies, driver_path
from src.Scopus_Crawler.data_write import write2sql

# 浏览器选项
options = webdriver.ChromeOptions()
# 添加代理地址和header
options.add_argument('--proxy-server=202.120.43.93:8059')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/81.0.4044.138 Safari/537.36')

data_df = pd.read_excel('C:/Users/Administrator/Desktop/1103人民日报.xlsx')
data_list = data_df.values.tolist()

data_list = data_list[16000:]
count = 0
while count < len(data_list):
    result_list = []
    driver = webdriver.Chrome(driver_path, options=options)
    driver.get('http://www.apabi.com/sjtu/?pid=newspaper.page&issueid=nq.D110000renmrb_20151101&cult=CN')

    cookies = driver.get_cookies()
    cookies_dict = {}
    for element in cookies:
        cookies_dict[element['name']] = element['value']
    driver.close()
    try:
        for i in range(count, len(data_list)):
            print(i)
            data = data_list[i]
            url = data[1]
            # page = requests.get(url=url, headers=headers, proxies=proxies, cookies=cookies_dict)
            page = requests.get(url=url, headers=headers, cookies=cookies_dict)
            source = re.findall(r'''<div class="i-list_baokan t1_12">[\s\S]*?</div>''', page.text)
            if source:
                link_list = re.findall(r'''<li style=".*?"><a title=".*?" href="(.*?)">''', source[0])
                title_list = re.findall(r'''<li style=".*?"><a title="(.*?)" href=".*?''', source[0])
                domain_url = 'http://www.apabi.com/sjtu/'
                link_list = [domain_url + i for i in link_list]
                df = pd.DataFrame(data={'title': title_list, 'text_link': link_list})
                df['text_date'] = data[2]
                df['page_link'] = data[1]
                df['page_name'] = data[0]
                result_list.append(df)
        # 结束循环
        count = len(data_list)

    # 出现错误时，从错误处中断，再从该处开始
    except Exception as err:
        print('ERROR:%s' % err)
        print('当前进度：%s / %s' % (i + 1, len(data_list)))
        count = i

    if result_list:
        all_data_df = pd.concat(result_list)
        write2sql([['rmrb_copy', all_data_df]])
