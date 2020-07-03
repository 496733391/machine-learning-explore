#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

import requests
import re
from bs4 import BeautifulSoup as bs
import pandas as pd

post_url1 = 'https://gaokao.chsi.com.cn/zyk/zybk/xkCategory.action'

post_url2 = 'https://gaokao.chsi.com.cn/zyk/zybk/specialityesByCategory.action'

headers = {
# 'Accept-Encoding': 'gzip, deflate, br',
# 'Accept-Language': 'zh-CN,zh;q=0.9',
# 'Connection': 'keep-alive',
# 'Content-Length': '12',
# 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
# 'Host': 'gaokao.chsi.com.cn',
# 'Origin': 'https://gaokao.chsi.com.cn',
# 'Referer': 'https://gaokao.chsi.com.cn/zyk/zybk/',
# 'Sec-Fetch-Dest': 'empty',
# 'Sec-Fetch-Mode': 'cors',
# 'Sec-Fetch-Site': 'same-origin',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
# 'X-Requested-With': 'XMLHttpRequest'
}


def get_subject():
    result_list = []

    for i in range(105001, 105014):
        print(i)
        parent_data = 'key=' + str(i)
        parent_class = requests.post(post_url1, data=parent_data, headers=headers, timeout=30)
        p_soup = bs(parent_class.text, 'lxml')
        temp = p_soup.find_all('li')
        parent_subject = [ele.text.replace('\ue6a2', '') for ele in temp]

        for j in range(1, 34):
            if j < 10:
                data = 'key=' + str(i) + '0' + str(j)
            else:
                data = 'key=' + str(i) + str(j)

            print(data)
            child_class = requests.post(post_url2, data=data, headers=headers, timeout=30)

            if '程序异常' not in child_class.text:
                soup = bs(child_class.text, 'lxml')
                table_list = soup.find_all('tr')
                for k in range(1, len(table_list)):
                    element = table_list[k].find_all('td')
                    one_sub = [i, parent_subject[j-1], element[0].text, element[1].text, element[2].contents[0].attrs['href']]
                    result_list.append(one_sub)

    result_df = pd.DataFrame(data=result_list, columns=['p_code', 'parent_subject', 'child_subject', 'subject_code', 'url'])
    result_df.to_excel('C:/Users/Administrator/Desktop/0701subject.xlsx', encoding='utf8', index=False)


from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password

dbutil = DBUtil(host, port, database, username, password)
sql = "SELECT * from 0701temp"
df = dbutil.get_allresult(sql, 'df')
dbutil.close()

pcode_dict = {
'105001': '哲学',
'105002': '经济学',
'105003': '法学',
'105004': '教育学',
'105005': '文学',
'105006': '历史学',
'105007': '理学',
'105008': '工学',
'105009': '农学',
'105010': '医学',
'105012': '管理学',
'105013': '艺术学',
}

df.replace(pcode_dict, inplace=True)

df.to_excel('C:/Users/Administrator/Desktop/0701subject.xlsx', encoding='utf8', index=False)

data_list = df.values.tolist()

base_url = 'https://gaokao.chsi.com.cn'

df_list = []

for data in data_list:
    print(data[-2])
    school_url = base_url + data[-1]
    sp_page = requests.get(school_url, headers=headers, timeout=30)
    p_soup = bs(sp_page.text, 'lxml')
    temp = p_soup.find_all(class_='showLayer1')
    sp_school = [element.attrs['title'] for element in temp]
    sub_df = pd.DataFrame(data=sp_school, columns=['school'])
    sub_df['subject_code'] = data[-2]
    df_list.append(sub_df)

result_df = pd.concat(df_list)
result_df.to_excel('C:/Users/Administrator/Desktop/0702subject.xlsx', encoding='utf8', index=False)
