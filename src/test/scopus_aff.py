#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup as bs

base_url = 'https://www.scopus.com/affil/profile.uri?afid=%s&origin=AffiliationProfile'

proxies = {
            "http": "http://202.120.43.93:8059"
}

headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                          'e/81.0.4044.138 Safari/537.36'
}

result_list = []
try:
    for i in range(60000000, 60003005):
        url = base_url % i
        print(i)
        text = requests.get(url,
                            proxies=proxies,
                            headers=headers,
                            timeout=300,
                            )
        if 'Error message' in text.text:
            print('***' + str(i) + '***')

        else:
            soup = bs(text.text, 'lxml')
            print(soup.find(class_='h4 wordBreakWord marginLeft1').text)
            result_list.append(str(i) + ';' + soup.find(class_='h4 wordBreakWord marginLeft1').text + '\n')

except Exception:
    pass

with open('result.txt', 'w', encoding='utf-8') as f:
    f.writelines(result_list)
