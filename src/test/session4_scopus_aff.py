#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs

base_url = 'https://www.scopus.com/affil/profile.uri?afid=%s&origin=AffiliationProfile'

proxies = {
            "http": "http://202.120.43.93:8059"
}

cookies = '''__cfduid=dbf2e076d5187308fd7dff007b95013a91588830445; scopus.machineID=C95FAA82D76902CFBA9ADB44D5C59CF2.wsnAw8kcdt7IPYLO0V48gA; optimizelyEndUserId=oeu1588830449793r0.7402451939845718; optimizelyBuckets=%7B%7D; xmlHttpRequest=true; optimizelySegments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22referral%22%7D; check=true; SCSessionID=4FDF36DC0486D356F1F0C43FB41D289A.wsnAw8kcdt7IPYLO0V48gA; scopusSessionUUID=b4f73fa3-f237-450a-9; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB1394850C713694D89FCE17D14E54BB0A7F00B0E1C9FEB62BF7355C4501BA647738278FC278415EC1A7924B82E83258A30CDEF842435DA8F7D41161E65D1E3A3AF; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=1075005958%7CMCIDTS%7C18396%7CMCMID%7C23612113200045070330531324322910847678%7CMCAAMLH-1589935617%7C11%7CMCAAMB-1589935617%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589338017s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-1185074918%7CvVersion%7C4.4.1; __cfruid=213b832b63414e6a7408533122877b1f1d8feab7-1589330818; javaScript=true; screenInfo="1080:1920"; optimizelyPendingLogEvents=%5B%5D; mbox=PC#0d2fc3c7b0294bd788e2024d386337d6.22_0#1652580280|session#321264b621fe4c1a9ba70d1626a90309#1589336550; s_sess=%20s_cpc%3D0%3B%20s_sq%3D%3B%20e41%3D1%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Dsc%25253Arecord%25253Aaffiliation%252520details%252C79%252C79%252C937%252C1920%252C937%252C1920%252C1080%252C1%252CP%3B%20s_ppv%3Dsc%25253Arecord%25253Aaffiliation%252520details%252C79%252C79%252C937%252C771%252C937%252C1920%252C1080%252C1%252CL%3B; s_pers=%20c19%3Dsc%253Arecord%253Aaffiliation%2520details%7C1589337280557%3B%20v68%3D1589335479479%7C1589337280566%3B%20v8%3D1589335493066%7C1683943493066%3B%20v8_s%3DLess%2520than%25201%2520day%7C1589337293066%3B'''

headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                          'e/81.0.4044.138 Safari/537.36',
            'cookies': cookies
}

temp_i = 60030050
while temp_i < 60050006:
    result_list = []
    try:
        for i in range(temp_i, 60050006):
            url = base_url % i
            print(i)
            text = requests.get(url, proxies=proxies, headers=headers, timeout=300)
            if 'Error message' in text.text:
                print('***' + str(i) + '***')

            else:
                soup = bs(text.text, 'lxml')
                print(soup.find(class_='h4 wordBreakWord marginLeft1').text)
                result_list.append(str(i) + ';' + soup.find(class_='h4 wordBreakWord marginLeft1').text + '\n')

        # 若循环正常结束，结束while循环
        temp_i = 60050006

    except Exception:
        print('出现报错中断，从断点处再开始: %s' % i)
        temp_i = i

    with open('result4.txt', 'a', encoding='utf-8') as f:
        f.writelines(result_list)
