#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
import time

from src.Scopus_Crawler.scopus_config import headers

url = 'http://www.hanban.org/hanbancn/template/ciotab_cn1.htm?v1'

page_info = requests.get(url, headers=headers)
soup = bs(page_info.text, 'lxml')

result_list = []

land_name_list = ['亚洲', '非洲', '美洲', '欧洲', '大洋洲']
temp_list = ['nation', 'nation2', 'nation3', 'nation4', 'nation5']
temp_list2 = ['tcon_nationBox', 'tcon_nationBox2', 'tcon_nationBox3', 'tcon_nationBox4', 'tcon_nationBox5']
land_list = soup.find_all(class_='tcon')
for i in range(len(land_list)):
    nation_info = land_list[i].find(class_=temp_list[i])
    nation_list_temp = nation_info.find_all('li')
    nation_list = [k.text for k in nation_list_temp]

    tcon_nationBox = land_list[i].find(class_=temp_list2[i])
    tcon_naton_list = tcon_nationBox.find_all(class_='tcon_nation')
    for j in range(len(tcon_naton_list)):
        ky_and_course = tcon_naton_list[j].find_all('ul')
        ky_list = ky_and_course[0].find_all('li')
        course_list = ky_and_course[1].find_all('li')
        for ky in ky_list:
            try:
                if nation_list[j] != '欧盟':
                    result_list.append([land_name_list[i], nation_list[j], '孔子学院', ky.text.strip(), ky.find('a').get('href').strip()])
            except Exception:
                print([land_name_list[i], nation_list[j], '孔子学院', ky.text.strip()])

        for course in course_list:
            try:
                result_list.append([land_name_list[i], nation_list[j], '孔子课堂', course.text.strip(), course.find('a').get('href').strip()])
            except Exception:
                print([land_name_list[i], nation_list[j], '孔子课堂', course.text.strip()])

# result_df = pd.DataFrame(data=result_list, columns=['洲', '国家', '类型', '名称', 'url'])
# result_df.to_excel('C:/Users/Administrator/Desktop/孔子学院数据.xlsx', index=False)

final_result_list = []
# result_list = result_list[8:]
for i in range(len(result_list)):
    college_page = requests.get(result_list[i][4], headers=headers, timeout=10)
    page_soup = bs(college_page.text, 'lxml')
    print(i, result_list[i])

    if 'zhuanti' in result_list[i][4]:
        info_list = page_soup.find(class_='main_leftCon').find_all('table')
    else:
        info_list = page_soup.find(class_='main_leftCon').find_all('p')

    if info_list:
        city_t = re.findall(r'所在城市\s+(.*)', info_list[0].text)
        city = '' if not city_t else city_t[0].strip()

        own_inf_t = re.findall(r'承办机构：(.*)[\s]*', info_list[1].text)
        own_inf = '' if not own_inf_t else own_inf_t[0].strip()

        co_info_t = re.findall(r'合作机构：(.*)[\s]*', info_list[1].text)
        co_info = '' if not co_info_t else co_info_t[0].strip()

        build_date_t = re.findall(r'设立时间：(.*)', info_list[2].text)
        build_date = '' if not build_date_t else build_date_t[0]

        contact_person_t = re.findall(r'联系人：(.*)\s+', info_list[3].text)
        contact_person = '' if not contact_person_t else contact_person_t[0]

        address_t = re.findall(r'地址：(.*)\s+', info_list[3].text)
        address = '' if not address_t else address_t[0]

        phone_number_t = re.findall(r'电话：(.*)\s+', info_list[3].text)
        phone_number = '' if not phone_number_t else phone_number_t[0]

        fax_t = re.findall(r'传真：(.*)\s+', info_list[3].text)
        fax = '' if not fax_t else fax_t[0]

        email_address_t = re.findall(r'邮箱：(.*)', info_list[3].text)
        email_address = '' if not email_address_t else email_address_t[0]

        try:
            url_t = re.findall(r'网址\s+(.*)', info_list[4].text)
            url = '' if not url_t else url_t[0]
        except Exception:
            url = ''

        final_result_list.append(result_list[i] + [city, own_inf, co_info, build_date, contact_person, address,
                                                   phone_number, fax, email_address, url])

final_result_df = pd.DataFrame(data=final_result_list,
                               columns=['洲', '国家', '类型', '名称', 'url', '所在城市', '承办机构', '合作机构',
                                        '设立时间', '联系人', '地址', '电话', '传真', '邮箱', '学院网址'])
final_result_df.to_excel('C:/Users/Administrator/Desktop/孔子学院数据.xlsx', index=False)

