#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs

from src.config.logConfig import logger_aff4 as logger

base_url = 'https://www.scopus.com/affil/profile.uri?afid=%s&origin=AffiliationProfile'

proxies = {
            "http": "http://202.120.43.93:8059"
}

headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                          'e/81.0.4044.138 Safari/537.36'
}

temp_i = 60124723
while temp_i < 60130006:
    result_list = []
    try:
        for i in range(temp_i, 60130006):
            url = base_url % i
            logger.info('%s' % i)
            text = requests.get(url, proxies=proxies, headers=headers, timeout=300)
            if 'Error message' in text.text:
                logger.info('***%s***' % i)

            else:
                soup = bs(text.text, 'lxml')
                result_list.append(str(i) + ';' + soup.find(class_='h4 wordBreakWord marginLeft1').text + '\n')
                logger.info(str(i) + ';' + soup.find(class_='h4 wordBreakWord marginLeft1').text)

        # 若循环正常结束，结束while循环
        temp_i = 60130006

    except Exception as err:
        logger.info('ERROR: %s' % err)
        logger.info('出现报错中断，从断点处再开始: %s' % i)
        temp_i = i

    with open('result4.txt', 'a', encoding='utf-8') as f:
        f.writelines(result_list)
