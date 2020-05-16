#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import json

url = 'https://www.scopus.com/author/affilHistory.uri?auId=56425884500'

proxies = {"http": "http://202.120.43.93:8059"}

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
           'e/81.0.4044.138 Safari/537.36'}

with open('C:/Users/Administrator/Desktop/machine-learning-explore/src/Scopus_Crawler/cookies.json', 'r') as f:
    cookies = json.load(f)

text = requests.get(url, proxies=proxies, headers=headers, timeout=300, cookies=cookies)

result_list = eval(text.text)
for element in result_list:
    element['start_year'] = element['dateRange'][0]
    element['end_year'] = element['dateRange'][1]
    element.pop('dateRange')

result_df = pd.DataFrame(result_list)
rename_dict = {
 'affiliationCity': 'aff_city',
 'affiliationName': 'aff_name',
 'affiliationCountry': 'aff_country',
 'affiliationId': 'aff_id',
 'affiliationUrl': 'aff_url',
}
result_df.rename(columns=rename_dict, inplace=True)

print(result_df)
