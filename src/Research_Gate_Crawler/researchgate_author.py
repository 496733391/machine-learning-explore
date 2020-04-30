#! /usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from tqdm import tqdm
import time
import datetime
from bs4 import BeautifulSoup as bs
import re
import requests
import random
import pandas as pd


base_url = 'https://www.researchgate.net/search/researcher?q='

# 检索的关键词，名+%2B+姓
name_list = ['Jianbo', 'Wang']
search_key = '%2B'.join(name_list)
# Chrome驱动程序在电脑中的位置
location_driver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'


class CrawlerAuthor:
    def __init__(self):
        self.url = base_url + search_key

    # 启动Chrome浏览器驱动
    def start_brower(self):
        # 启动Chrome浏览器
        driver = webdriver.Chrome(location_driver)
        # 最大化窗口
        # driver.maximize_window()
        return driver

    def catch_pipeline(self, driver):
        final_result = []
        # 逐页抓取
        for i in range(1, 11):
            url = self.url + '&page=%s' % i
            # req = requests.get(url=url)
            driver.get(url)
            random_seconds = random.uniform(4, 6)
            time.sleep(random_seconds)
            soup = bs(driver.page_source, 'lxml')
            onepage_result = soup.find_all(class_='nova-v-person-item__body')
            # 每页逐条抓取
            for result in onepage_result:
                for content in result.contents:
                    # 姓名
                    name = content.find(itemprop='name').text
                    # 若人名与search_key不同，停止
                    if name != ' '.join(name_list):
                        return final_result

                    information_list = content.find_all(class_='nova-e-list__item nova-v-person-item__info-section-list-item')
                    all_text = []
                    for information in information_list:
                        all_text.append(information.text)
                    # 判断是否包含院校信息
                    ins = content.find_all(text='Institution')
                    # 学校
                    if ins:
                        institution = all_text[0]
                        all_text.remove(institution)
                    else:
                        institution = None
                    dep = content.find_all(text='Department')
                    # 学院
                    if dep:
                        department = all_text[0]
                        all_text.remove(department)
                    else:
                        department = None
                    # 最后发表文章
                    las = content.find_all(text='Latest publication')
                    if las:
                        last_publication = all_text[-1]
                        all_text.remove(last_publication)
                    else:
                        last_publication = None
                    # 研究方向
                    if len(all_text) > 0:
                        skill = ','.join(all_text)
                    else:
                        skill = None

                    result_list = [name, institution, department, skill, last_publication]
                    print(name, '|', institution, '|', department, '|', skill, '|', last_publication)
                    final_result.append(result_list)

        return final_result

    def run(self):
        driver = self.start_brower()
        final_result = self.catch_pipeline(driver)
        driver.close()
        result_df = pd.DataFrame(data=final_result, columns=['name', 'institution', 'department', 'skill', 'last_publication'])
        result_df.to_excel('test_result.xlsx', index=False)


if __name__ == '__main__':
    print('#######', datetime.datetime.now())
    craw = CrawlerAuthor()
    craw.run()
    print('#######', datetime.datetime.now())
