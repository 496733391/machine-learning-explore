#! /usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
from urllib.parse import quote
import requests
import pandas as pd
import time

appid = '20200807000535803'
secretKey = 'crKfyZviVDGI9OdRDVOX'

myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

fromLang = 'auto'
toLang = 'zh'
salt = 32768

df = pd.read_excel('C:/Users/Administrator/Desktop/journal_title.xlsx')

title_list = list(set(df['Title']))
result_list = []

for i in range(506):
    print(i)
    sub_title_list = title_list[50*i:50*(i+1)]
    q = '\n'.join(sub_title_list)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = myurl + '?appid=' + appid + '&q=' + quote(q) + '&from=' + fromLang + '&to=' + \
          toLang + '&salt=' + str(salt) + '&sign=' + sign
    trans_result = requests.get(url, timeout=10).json()
    result_list += trans_result['trans_result']
    time.sleep(1)

result_df = pd.DataFrame(data=result_list)
result_df.to_excel('C:/Users/Administrator/Desktop/期刊翻译结果.xlsx')
