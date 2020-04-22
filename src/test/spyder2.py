#! /usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from tqdm import tqdm
import time
from bs4 import BeautifulSoup as bs


base_url_part = 'https://scholar.google.com.hk/scholar?hl=zh-CN&as_sdt=0%2C5&q='
search_query = 'shanghai+university'  # 检索的关键词
location_driver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'  # Chrome驱动程序在电脑中的位置


class Crawler:
    def __init__(self):
        self.url = base_url_part + search_query
        self.url = 'http://xueshu.baidu.com/s?wd=清华大学&pn=0&tn=SE_baiduxueshu_' \
                   'c1gjeupa&ie=utf-8&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&sc_hit=1'

    # 启动Chrome浏览器驱动
    def start_brower(self):
        # 启动Chrome浏览器
        driver = webdriver.Chrome(location_driver)
        # 最大化窗口
        driver.maximize_window()
        # 浏览器打开爬取页面
        driver.get(self.url)
        return driver

    def page_analy(self, driver):
        type(driver.page_source)
        return

    def run(self):

        driver = self.start_brower()
        self.page_analy(driver)
        driver.close()
        print("Download has finished.")


if __name__ == '__main__':
    craw = Crawler()
    craw.run()