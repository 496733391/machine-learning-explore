#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import re
import time

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from src.Scopus_Crawler.scopus_config import driver_path, headers


# options = webdriver.ChromeOptions()
# options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                      'Chrome/81.0.4044.138 Safari/537.36')
# driver = webdriver.Chrome(driver_path, options=options)
#
# base_url = 'http://www.gx211.com/collegemanage/search.aspx?id=1'
#
# final_list = []
# driver.get(base_url)
#
# soup = bs(driver.page_source, 'lxml')
# school_info = soup.find_all(class_='trs')
# for element in school_info:
#     info_list = [i.text for i in element.contents]
#     final_list.append(info_list[:-1])
#
# page_no = 1
# while page_no < 107:
#     time.sleep(1)
#     driver.find_element_by_id('Lk_Down').click()
#     soup = bs(driver.page_source, 'lxml')
#     school_info = soup.find_all(class_='trs')
#     for element in school_info:
#         info_list = [i.text for i in element.contents]
#         final_list.append(info_list[:-1])
#
#     current_page = soup.find(id='Lb_PageIndex')
#     print(current_page.text)
#     if current_page.text == '107':
#         break
#
# school_df = pd.DataFrame(data=final_list, columns=['高校名称', '地区', '类别', '性质', '211', '985'])
# school_df.to_excel('C:/Users/Administrator/Desktop/0716school.xlsx', sheet_name='Sheet1', index=False)

base_url = 'http://www.gx211.com/collegemanage/content%s_11.shtml'

school_df = pd.read_excel('C:/Users/Administrator/Desktop/0716school.xlsx', sheet_name='Sheet1', index=False)

school_id_list = school_df['id'].values.tolist()

count = 0
result_list = []

while count < len(school_id_list):
    try:
        for i in range(count, len(school_id_list)):
            time.sleep(0.5)
            print('当前进度：%s / %s' % (i + 1, len(school_id_list)))
            url = base_url % school_id_list[i]
            school_subject_page = requests.get(url=url, timeout=30, headers=headers)
            soup = bs(school_subject_page.text, 'lxml')
            # subject_list = soup.find_all(class_='trs')
            # if not subject_list:
            #     print("无专业：%s" % school_id_list[i])
            # for subject in subject_list:
            #     temp_list = [ele.string for ele in subject.contents]
            #     temp_list[1] = int(re.findall(r'[0-9]+', temp_list[1])[0])
            #     temp_list[2] = int(re.findall(r'[0-9]+', temp_list[2])[0])
            #     result_list.append([school_id_list[i]] + temp_list[:-1])
            tt = soup.find_all(class_='ListH3')
            result_list.append([school_id_list[i], tt[1].text.strip().split('\r\n\r\n')[1][5:]])

        # 结束循环
        count = len(school_id_list)

    # 出现错误时，从错误处中断，再从该处开始
    except Exception as err:
        print('ERROR:%s' % err)
        count = i

# subject_df = pd.DataFrame(data=result_list, columns=['id', '具体专业', '专业大类', '专业小类'])
# subject_df.to_excel('C:/Users/Administrator/Desktop/0716subject.xlsx', sheet_name='Sheet1', index=False)
temp_df = pd.DataFrame(data=result_list, columns=['id', '更新时间'])
temp_df.to_excel('C:/Users/Administrator/Desktop/更新时间.xlsx', sheet_name='Sheet1', index=False)
