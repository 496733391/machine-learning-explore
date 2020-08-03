#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re

# headers
headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                          'e/81.0.4044.138 Safari/537.36'
}

provinces = ['北京', '天津', '河北', '山西', '内蒙古', '宁夏', '青海', '陕西', '甘肃', '新疆', '辽宁', '吉林', '黑龙江',
            '山东', '江苏', '上海', '浙江', '安徽', '福建', '江西', '河南', '湖南', '湖北', '四川', '贵州', '云南', 
            '重庆', '西藏', '广东', '广西', '海南', '香港', '澳门', '台湾']
base_url = 'http://wcame.bjmu.edu.cn/universities.php?cid=37&location='

result_list = []
for provin in provinces:
    url = base_url + provin
    page_info = requests.get(headers=headers, url=url, timeout=30)
    soup = bs(page_info.text, 'lxml')
    elements = soup.find_all(name='tr', attrs={"onclick": re.compile(r"window.open(\s\w+)?")})
    for element in elements:
        info = element.text.strip().split('\n')
        result_list.append(info)

result_df = pd.DataFrame(data=result_list, columns=['所在地', '院校名称', '认证状态', '认证时间',
                                                    '有效期截止', '进展报告', '综合报告'])

result_df.to_excel('C:/Users/Administrator/Desktop/0709.xlsx', sheet_name='Sheet1', index=False)

