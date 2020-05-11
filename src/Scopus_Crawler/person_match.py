#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pandas as pd


url = 'https://www.scopus.com/author/affilHistory.uri?auId=%s' % '55574235694'

proxies = {
            "http": "http://202.120.43.93:8059"
}

headers = {
            'cookie': '''__cfduid=dbf2e076d5187308fd7dff007b95013a91588830445; scopus.machineID=C95FAA82D76902CFBA9ADB44D5C59CF2.wsnAw8kcdt7IPYLO0V48gA; optimizelyEndUserId=oeu1588830449793r0.7402451939845718; optimizelyBuckets=%7B%7D; xmlHttpRequest=true; optimizelySegments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22referral%22%7D; SCSessionID=2124BA38BFEF1E7C34A347A7F3CF4559.wsnAw8kcdt7IPYLO0V48gA; scopusSessionUUID=7cbddfe2-8e72-4e68-a; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB12CA18A85FC5003408C9F825583DD87FBDA0059DCC2B58C406B42DD27F8E7D7A5A31AAC5A6BDE3E4B4DACF34F3854CEEB48CF4F88CC1DCB7CF6083FBE33078A1E; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; optimizelyPendingLogEvents=%5B%5D; check=true; javaScript=true; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=1075005958%7CMCIDTS%7C18394%7CMCMID%7C23612113200045070330531324322910847678%7CMCAAMLH-1589799591%7C11%7CMCAAMB-1589799591%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589201991s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-1185074918%7CvVersion%7C4.4.1; screenInfo="1080:1920"; __cfruid=86710e451586a8cd87e1b0c953beac7cd8a65baa-1589194807; mbox=PC#0d2fc3c7b0294bd788e2024d386337d6.22_0#1652439616|session#a362a7c92a214b80811b75d62d5c2208#1589196650; s_sess=%20s_cpc%3D0%3B%20c21%3Dlastname%253Dliu%2526firstname%253Dbo%2526affiliation%253Dwuhan%2520university%3B%20e13%3Dlastname%253Dliu%2526firstname%253Dbo%2526affiliation%253Dwuhan%2520university%253A1%3B%20c13%3Ddocument%2520count%2520%2528high-low%2529%3B%20s_sq%3D%3B%20e41%3D1%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Dsc%25253Asearch%25253Aauthor%252520results%252C33%252C33%252C1137%252C1920%252C937%252C1920%252C1080%252C1%252CP%3B%20s_ppv%3Dsc%25253Arecord%25253Aauthor%252520details%252C20%252C20%252C937%252C771%252C937%252C1920%252C1080%252C1%252CL%3B; s_pers=%20c19%3Dsc%253Arecord%253Aauthor%2520details%7C1589196617455%3B%20v68%3D1589194814267%7C1589196617472%3B%20v8%3D1589194823468%7C1683802823468%3B%20v8_s%3DLess%2520than%25201%2520day%7C1589196623468%3B''',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                          'e/81.0.4044.138 Safari/537.36'
}

passed_exp = requests.get(url,
                          proxies=proxies,
                          headers=headers,
                          timeout=300,
                          )

result_list = eval(passed_exp.text)
institute_list = [i['affiliationName'].replace('  ', ' ').lower().strip() for i in result_list]
print(institute_list)
