#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pandas as pd

from src.Scopus_Crawler.scopus_config import headers

# base_url = 'https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&' \
#            'f985=&is_dual_class=&keyword=&page={}&province_id=&request_type=2&school_type=&signsafe=&size=20' \
#            '&sort=view_total&type=&uri=apidata/api/gk/school/lists'
#
# info_list = []
# for i in range(1, 149):
#     print(i)
#     url = base_url.format(i)
#     school_info = requests.get(url=url, headers=headers).json()
#     info_list.extend(school_info['data']['item'])
#
# for dic in info_list:
#     del dic['special']
#
# df = pd.DataFrame(data=info_list)
# df = df.loc[:, ['name', 'school_id']]

# df.to_excel('C:/Users/Administrator/Desktop/school0925.xlsx', index=False)

df = pd.read_excel('C:/Users/Administrator/Desktop/school0925.xlsx')

school_url = 'https://static-data.eol.cn/www/2.0/school/{}/info.json'
result_list = []
for items in df.values.tolist():
    print(items)
    url = school_url.format(items[1])
    school_page = requests.get(url=url, headers=headers).json()
    if school_page:
        result_list.append([items[0], items[1], school_page['data']['create_date']])

result_df = pd.DataFrame(data=result_list, columns=['学校名称', '学校ID', '创建时间'])
result_df.to_excel('C:/Users/Administrator/Desktop/result0925.xlsx', index=False)
