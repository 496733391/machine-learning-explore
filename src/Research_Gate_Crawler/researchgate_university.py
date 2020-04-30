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

from researchgate_author_detail import CrawlerAuthorDetail


base_url1 = 'https://www.researchgate.net/institution/'
base_url2 = '/members'

# 检索的关键词，名+%2B+姓
name_list = ['Fourth', 'Military', 'Medical', 'University']
search_key = '_'.join(name_list)
# Chrome驱动程序在电脑中的位置
location_driver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'


class CrawlerUniversity:
    def __init__(self):
        self.url = base_url1 + search_key + base_url2

    # 启动Chrome浏览器驱动
    def start_brower(self):
        # 启动Chrome浏览器
        driver = webdriver.Chrome(location_driver)
        # 最大化窗口
        # driver.maximize_window()
        return driver

    def catch_pipeline(self, driver):
        # 获取最大页码
        driver.get(self.url)
        random_seconds = random.uniform(2, 4)
        time.sleep(random_seconds)
        page_list = bs(driver.page_source, 'lxml').find_all(rel='noindex, follow')
        page_no = []
        for element in page_list:
            page_no.append(int(element.text))
        max_page = max(page_no)
        author_url = []
        # 逐页抓取
        for i in range(1, max_page + 1):
            url = self.url + '/%i' % i
            # req = requests.get(url=url)
            driver.get(url)
            random_seconds = random.uniform(2, 4)
            time.sleep(random_seconds)
            html = driver.page_source
            soup = bs(html, 'lxml')
            author_link = soup.find_all(class_='display-name')
            print(len(author_link))
            for author in author_link:
                author_url.append(author.get('href'))

        return author_url

    def run(self):
        driver = self.start_brower()
        author_url = self.catch_pipeline(driver)
        driver.close()

        return author_url

    def main_prog(self):
        driver = self.start_brower()
        author_url = self.catch_pipeline(driver)
        driver.close()
        url_list = ['https://www.researchgate.net/' + i for i in author_url]

        # test
        url_list = url_list[:20]

        author_craw = CrawlerAuthorDetail(url_list)
        final_result, final_result_dict = author_craw.run()
        author_craw.dict2json(final_result_dict)
        result_df = pd.DataFrame(data=final_result, columns=['name', 'institution', 'department', 'current_position',
                                                             'expertise', 'experience_list', 'publication_list'])
        result_df.to_excel('result.xlsx', index=False)


if __name__ == '__main__':
    print(datetime.datetime.now())
    craw = CrawlerUniversity()
    # author_url = craw.run()
    craw.main_prog()
    print(datetime.datetime.now())
