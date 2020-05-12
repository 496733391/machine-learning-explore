#! /usr/bin/python
# -*- coding: utf-8 -*-

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
cookie = '''__cfduid=dbf2e076d5187308fd7dff007b95013a91588830445; scopus.machineID=C95FAA82D76902CFBA9ADB44D5C59CF2.wsnAw8kcdt7IPYLO0V48gA; optimizelyEndUserId=oeu1588830449793r0.7402451939845718; optimizelyBuckets=%7B%7D; xmlHttpRequest=true; optimizelySegments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22referral%22%7D; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; check=true; javaScript=true; screenInfo="1080:1920"; __cfruid=5ca423af20b11d1de7c7546b5e0d9f8730608346-1589245238; SCSessionID=486D55F30E9C7A41D6D249DA14D6C2F1.wsnAw8kcdt7IPYLO0V48gA; scopusSessionUUID=eee5c570-c7c7-4c55-8; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB1136D3FCD6965347F03D594F38844175AC31815238C25F4A1A616A0BCDCEF085BBAFDF2ADE925350150D7900CAD0CA8A6097EFB6981FBF7F8310679A72AA1BEB8; optimizelyPendingLogEvents=%5B%5D; mbox=PC#0d2fc3c7b0294bd788e2024d386337d6.22_0#1652510040|session#67a0fc2305e24036aa988cf8261491fa#1589267099; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=1075005958%7CMCIDTS%7C18394%7CMCMID%7C23612113200045070330531324322910847678%7CMCAAMLH-1589870040%7C11%7CMCAAMB-1589870040%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589272440s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-1185074918%7CvVersion%7C4.4.1; s_sess=%20s_cpc%3D0%3B%20c21%3Daffiliation%253Duniversity%2520of%2520quebec%3B%20e13%3Daffiliation%253Duniversity%2520of%2520quebec%253A1%3B%20c13%3Ddocument%2520count%2520%2528high-low%2529%3B%20s_sq%3D%3B%20e41%3D1%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Dsc%25253Asearch%25253Aaffiliation%252520results%252C37%252C37%252C1037%252C1920%252C937%252C1920%252C1080%252C1%252CP%3B%20s_ppv%3Dsc%25253Arecord%25253Aauthor%252520details%252C19%252C19%252C937%252C771%252C937%252C1920%252C1080%252C1%252CL%3B; s_pers=%20c19%3Dsc%253Arecord%253Aauthor%2520details%7C1589267040643%3B%20v68%3D1589265238665%7C1589267040657%3B%20v8%3D1589265253988%7C1683873253988%3B%20v8_s%3DLess%2520than%25201%2520day%7C1589267053988%3B'''

# headers
headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                          'e/81.0.4044.138 Safari/537.36'
}

# 学者机构信息地址
ins_url = 'https://www.scopus.com/author/affilHistory.uri?auId=%s'

# 学者详细页面地址
data_url = 'https://www.scopus.com/authid/detail.uri?authorId=%s'