#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import pandas as pd

year_list = ['2015', '2016', '2017', '2018', '2019']
month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
day_list = month_list + [str(i) for i in list(range(13, 32))]

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
           'e/81.0.4044.138 Safari/537.36'}

gmw_url = 'https://epaper.gmw.cn/gmrb/html/%s-%s/%s/nbs.D110000gmrb_01.htm'

result_list = []
for year in year_list:
    for month in month_list:
        for day in day_list:
            print(year, month, day)
            url = gmw_url % (year, month, day)
            page = requests.get(url, headers)
            if page.status_code == 200:
                page_link = re.findall(r'''<a id=pageLink href=(.*?)>.*?</a>''', page.text)
                page_link = [k.strip() for k in page_link]
                page_link = [k.strip('.') for k in page_link]
                page_link = [k.strip('/') for k in page_link]
                page_text = re.findall(r'''<a id=pageLink href=.*?>(.*?)</a>''', page.text)
                domain_url = '/'.join(url.split('/')[:-1]) + '/'
                page_link = [domain_url + k for k in page_link]
                df = pd.DataFrame({'版块': page_text, '链接': page_link})
                df['date'] = year + month + day
                result_list.append(df)

gmw_df = pd.concat(result_list)
gmw_df.to_excel('C:/Users/Administrator/Desktop/1103光明日报.xlsx', sheet_name='Sheet1', index=False)
