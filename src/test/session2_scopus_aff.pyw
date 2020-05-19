#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import smtplib
from email.utils import formataddr
from email.mime.text import MIMEText

import os
import sys
base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../../")
sys.path.insert(0, base_dir)

from src.config.logConfig import logger_aff2 as logger

from_addr = '496733391@qq.com'
password = 'tfqyucjemdpvcabc'
to_addr = '496733391@qq.com'

base_url = 'https://www.scopus.com/affil/profile.uri?afid=%s&origin=AffiliationProfile'

proxies = {
            "http": "http://202.120.43.93:8059"
}

headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                          'e/81.0.4044.138 Safari/537.36'
}

temp_i = 60140006
while temp_i < 60160006:
    result_list = []
    try:
        for i in range(temp_i, 60160006):
            url = base_url % i
            logger.info('%s' % i)
            text = requests.get(url, proxies=proxies, headers=headers, timeout=300)
            if 'Error message' in text.text:
                logger.info('***%s***' % i)

            else:
                soup = bs(text.text, 'lxml')
                result_list.append(str(i) + ';' + soup.find(class_='h4 wordBreakWord marginLeft1').text + '\n')
                logger.info(str(i) + ';' + soup.find(class_='h4 wordBreakWord marginLeft1').text)

        # 若循环正常结束，结束while循环，发送邮件通知
        temp_i = 60160006

        msg = MIMEText('session2已结束运行', 'plain', 'utf-8')
        msg['From'] = formataddr(("private_message", from_addr))
        msg['To'] = formataddr(("private_message", to_addr))
        msg['Subject'] = "scopus机构数据获取邮件通知"

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

    except Exception as err:
        logger.info('ERROR: %s' % err)
        logger.info('出现报错中断，从断点处再开始: %s' % i)
        temp_i = i

        msg = MIMEText('session2出现报错中断，断点: %s' % i, 'plain', 'utf-8')
        msg['From'] = formataddr(("private_message", from_addr))
        msg['To'] = formataddr(("private_message", to_addr))
        msg['Subject'] = "scopus机构数据获取邮件通知"

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

    with open('C:/Users/Administrator/Desktop/machine-learning-explore/src/test/result2.txt', 'a', encoding='utf-8') as f:
        f.writelines(result_list)
