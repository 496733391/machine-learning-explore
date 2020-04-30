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
import json


# Chrome驱动程序在电脑中的位置
location_driver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'


class CrawlerAuthorDetail:
    def __init__(self, url_list):
        self.url_list = url_list

    def start_chrome(self):
        driver = webdriver.Chrome(location_driver)
        return driver

    def catch_pipeline(self, driver, url):
        print(url)
        driver.get(url)
        random_second = random.uniform(0.5, 1)
        time.sleep(random_second)
        soup = bs(driver.page_source, 'lxml')
        author_information_dict = {}

        # 获取姓名
        name_info = soup.find('h1', class_='nova-e-text nova-e-text--size-m nova-e-text--family-sans-serif '
                                           'nova-e-text--spacing-none nova-e-text--color-inherit')
        name = '' if not name_info else name_info.contents[0].text
        author_information_dict['name'] = name

        # 需要人机验证时，中断
        if not name_info:
            return 0, 0

        # 获取学校
        institution_info = soup.find('div', class_='nova-e-text nova-e-text--size-l nova-e-text--family-sans-serif '
                                                   'nova-e-text--spacing-none nova-e-text--color-inherit '
                                                   'nova-v-institution-item__title')
        institution = '' if not institution_info else institution_info.text
        author_information_dict['institution'] = institution

        # 获取学院
        department_info = soup.find('li', class_='nova-e-list__item nova-v-institution-item__meta-data-item')
        department = '' if not department_info else department_info.contents[0].text
        author_information_dict['department'] = department

        # 获取当前职称
        current_position_info = soup.find('li', 'nova-e-list__item nova-v-institution-item__info-section-list-item')
        current_position = '' if not current_position_info else current_position_info.text
        author_information_dict['current_position'] = current_position

        # 研究方向
        expertise_info = soup.find_all('a', class_='nova-e-badge nova-e-badge--color-grey nova-e-badge--display-inline '
                                                   'nova-e-badge--luminosity-medium nova-e-badge--size-l '
                                                   'nova-e-badge--theme-ghost nova-e-badge--radius-full')
        expertise = ''
        if expertise_info:
            expertise_list = []
            for e in expertise_info:
                expertise_list.append(e.text)
            expertise = ' ; '.join(expertise_list)
        author_information_dict['expertise'] = expertise

        # 过往科研经历及所在机构
        experience_dict = {}
        experience_list = []
        experienced = soup.find(text='Research Experience')
        if experienced:
            basic_info = soup.find('div', class_='profile-content-item')
            experience_info = basic_info.find_all('div', class_='nova-c-card nova-c-card--spacing-s '
                                                                'nova-c-card--elevation-none')
            for i, experience in enumerate(experience_info):
                temp_dict = {}
                # 起止年月
                period_ = experience.find('div', class_='nova-e-text nova-e-text--size-m nova-e-text--family-sans-'
                                                        'serif nova-e-text--spacing-none nova-e-text--color-'
                                                        'inherit nova-c-qualifier__label')
                period = '' if not period_ else period_.text
                temp_dict['period'] = period
                # 机构名称
                institution_p_ = experience.find('div', class_='nova-e-text nova-e-text--size-l nova-e-text--family-'
                                                               'sans-serif nova-e-text--spacing-none nova-e-text--'
                                                               'color-inherit nova-v-job-item__title')
                institution_p = '' if not institution_p_ else institution_p_.text
                temp_dict['institution_p'] = institution_p
                # 学院名称
                department_p_ = experience.find('li', class_='nova-e-list__item nova-v-job-item__meta-data-item')
                department_p = '' if not department_p_ else department_p_.text
                temp_dict['department_p'] = department_p
                # 职称
                position_p_ = experience.find('li', class_='nova-e-list__item nova-v-job-item__info-section-list-item')
                position_p = '' if not position_p_ else position_p_.text
                temp_dict['position_p'] = position_p
                experience_dict[i] = temp_dict
                # 合并成字符串
                one_experience = ' , '.join([period, institution_p, department_p, position_p])
                experience_list.append(one_experience)
        author_information_dict['experience'] = experience_dict
        # 合并成字符串
        experience_list = ' ; '.join(experience_list)
        # 发表的文献
        publication_dict = {}
        publication_list = []
        publication = soup.find(text='Publications')
        if publication:
            publication_info = soup.find_all('div', class_='nova-v-publication-item__body')
            for i, publication in enumerate(publication_info):
                temp_dict = {}
                # 标题
                title_ = publication.find('a', class_='nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare')
                title = '' if not title_ else title_.text
                temp_dict['title'] = title
                # 文献类型
                type_ = publication.find('div', class_='nova-v-publication-item__meta-left')
                type = '' if not type_ else type_.text
                temp_dict['type'] = type
                # 发表年月
                publish_date_ = publication.find('li', class_='nova-e-list__item nova-v-publication-item__meta-data-item')
                publish_date = '' if not publish_date_ else publish_date_.text
                temp_dict['publish_date'] = publish_date

                publication_dict[i] = temp_dict
                # 合并成字符串
                one_publication = ' , '.join([title, type, publish_date])
                publication_list.append(one_publication)

        # 合并成字符串
        publication_list = ' ; '.join(publication_list)

        author_information = [url, name, institution, department, current_position,
                              expertise, experience_list, publication_list]
        author_information_dict['publication'] = publication_dict

        return author_information, author_information_dict

    def run(self, driver=None):
        final_result = []
        final_result_dict = {}
        # 循环抓取，需要进行人机验证时中断并重启
        complete_num = 0
        for i in range(100):
            print('剩余数量：%s ； 已完成数量：%s' % (len(self.url_list)-complete_num, complete_num))

            if complete_num == len(self.url_list):
                break

            wait_time = random.uniform(5, 10)
            time.sleep(wait_time)
            driver = self.start_chrome()

            temp_num = complete_num

            for i in range(len(self.url_list)-temp_num):
                author_information, author_information_dict = self.catch_pipeline(driver, self.url_list[i+temp_num])
                # 判断author_information是否为0，若为0则中断
                if author_information:
                    final_result.append(author_information)
                    final_result_dict[i+temp_num] = author_information_dict
                    complete_num += 1
                else:
                    driver.close()
                    break

        return final_result, final_result_dict

    def dict2json(self, result_dict):
        result_json = json.dumps(result_dict, indent=4)
        with open('result1.json', 'w') as js:
            js.write(result_json)


if __name__ == '__main__':
    print(datetime.datetime.now())
    url_list = ['https://www.researchgate.net/profile/Yuanzhen_Cai']
    craw = CrawlerAuthorDetail(url_list)
    final_result, final_result_dict = craw.run()
    craw.dict2json(final_result_dict)
    print(final_result)
    print(final_result_dict)
    print(datetime.datetime.now())
