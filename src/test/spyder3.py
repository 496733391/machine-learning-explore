#! /usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from tqdm import tqdm
import time
import datetime
from bs4 import BeautifulSoup as bs
import re
import requests


base_url = 'https://www.researchgate.net/search/researcher?q='

# 检索的关键词，名+%2+姓
search_key = 'jianbo' + '%2B' + 'wang'
# Chrome驱动程序在电脑中的位置
location_driver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
# 页码
page_no = '&page=1'


class Crawler:
    def __init__(self):
        self.url = base_url + search_key + page_no

    # 启动Chrome浏览器驱动
    def start_brower(self):
        # 启动Chrome浏览器
        driver = webdriver.Chrome(location_driver)
        # 最大化窗口
        # driver.maximize_window()
        # 浏览器打开爬取页面
        driver.get(self.url)
        # 加载下一页
        # for i in tqdm(range(65)):
        #     driver.find_element_by_class_name('c-icon-pager-next').click()
        time.sleep(10)
        return driver

    def page_analy(self, driver):
        soup = bs(driver.page_source, 'lxml')
        result_list = soup.find_all(class_='nova-v-person-item__body')

        for result in result_list:
            for content in result.contents:
                name = content.find(itemprop='name').text
        return result_list

    def run(self):

        driver = self.start_brower()
        self.page_analy(driver)
        driver.close()
        print("Download has finished.")


if __name__ == '__main__':
    print(datetime.datetime.now())
    craw = Crawler()
    craw.run()
    print(datetime.datetime.now())
