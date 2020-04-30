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
from sqlalchemy import create_engine, types

from researchgate_author_detail import CrawlerAuthorDetail


base_url1 = 'https://www.researchgate.net/institution/'
base_url2 = '/members'

# 检索的关键词，名+%2B+姓
name_list = ['Fourth', 'Military', 'Medical', 'University']
search_key = '_'.join(name_list)
# Chrome驱动程序在电脑中的位置
location_driver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
# 数据库信息
host = 'localhost'
port = '3306'
database = 'local'
username = 'root'
password = 'admin'


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
        # max_page = max(page_no)
        max_page = 1
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
        url_list = url_list[:30]

        author_craw = CrawlerAuthorDetail(url_list)
        final_result, final_result_dict = author_craw.run()
        author_craw.dict2json(final_result_dict)
        result_df = pd.DataFrame(data=final_result, columns=['name', 'institution', 'department', 'current_position',
                                                             'expertise', 'experience_list', 'publication_list'])

        time_num = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        all_experience = pd.DataFrame(data=None, columns=None)
        all_publication = pd.DataFrame(data=None, columns=None)
        for i in range(len(result_df)):
            result_df.loc[i, 'person_id'] = time_num + str(i)
            if result_df.loc[i, 'experience_list']:
                experience_list = result_df.loc[i, 'experience_list'].split(' ; ')
                experience_list = [e.split(' , ') for e in experience_list]
                experience_df = pd.DataFrame(data=experience_list,
                                             columns=['period', 'institution_p', 'department_p', 'position_p'])
                experience_df['person_id'] = time_num + str(i)
                all_experience = all_experience.append(experience_df, ignore_index=True)

            if result_df.loc[i, 'publication_list']:
                publication_list = result_df.loc[i, 'publication_list'].split(' ; ')
                publication_list = [p.split(' , ') for p in publication_list]
                publication_df = pd.DataFrame(data=publication_list,
                                              columns=['title', 'pub_type', 'publish_date'])
                publication_df['person_id'] = time_num + str(i)
                all_publication = all_publication.append(publication_df, ignore_index=True)

        basic_info = result_df.drop(['experience_list', 'publication_list'], axis=1)

        basic_info.to_excel('basic_info.xlsx', index=False)
        all_publication.to_excel('all_publication.xlsx', index=False)
        all_experience.to_excel('all_experience.xlsx', index=False)

        return basic_info, all_experience, all_publication

    def w2sql(self, df, table_name):
        db_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=UTF8MB4". \
            format(username=username, password=password, host=host, port=port, db=database)

        engine = create_engine(db_url)

        datatype = {c: types.VARCHAR(df[c].str.len().max()) for c in df.columns[df.dtypes == 'object'].tolist()}

        df.to_sql(table_name, engine, index=False, if_exists='append', dtype=datatype)


if __name__ == '__main__':
    print(datetime.datetime.now())
    craw = CrawlerUniversity()
    # author_url = craw.run()
    basic_info, all_experience, all_publication = craw.main_prog()
    craw.w2sql(basic_info, 'basic_info')
    craw.w2sql(all_experience, 'experience_passed')
    craw.w2sql(all_publication, 'publication')
    print(datetime.datetime.now())
