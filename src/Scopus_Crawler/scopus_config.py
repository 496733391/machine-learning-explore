#! /usr/bin/python
# -*- coding: utf-8 -*-

import json

# 数据库信息
host = 'localhost'
port = 3306
database = 'local'
username = 'root'
password = 'admin'

# chrome浏览器driver路径
driver_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

# 搜索页面地址
search_url = 'https://www.scopus.com/results/authorNamesList.uri?origin=searchauthorlookup&src=al&edit=&poppUp=&' \
              'basicTab=&affiliationTab=&advancedTab=&' \
              'st1={}&' \
              'st2={}&' \
              'institute={}' \
              '&orcidId=&authSubject=LFSC&_authSub' \
              'ject=on&authSubject=HLSC&_authSubject=on&authSubject=PHSC&_authSubject=on&authSubject=SOSC&_authSubj' \
              'ect=on&s=AUTHLASTNAME%28liu%29+AND+AUTHFIRST%28bo%29&sdt=al&sot=al&searchId=42a0860e2008958faf4e6c64' \
              '4b496275&exactSearch=on&sid=42a0860e2008958faf4e6c644b496275'

# 代理地址
proxies = {
            "http": "http://202.120.43.93:8059"
}

# cookies
# with open('cookies.json', 'r') as js:
#     cookie = json.load(js)

# headers
headers = {
            # 'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                          'e/81.0.4044.138 Safari/537.36'
}

# 学者机构信息地址
ins_url = 'https://www.scopus.com/author/affilHistory.uri?auId=%s'

# 学者详细页面地址
data_url = 'https://www.scopus.com/authid/detail.uri?authorId=%s'