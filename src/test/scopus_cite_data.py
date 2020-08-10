#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import requests
from selenium import webdriver

from src.Scopus_Crawler.scopus_config import headers, proxies, driver_path
from src.Scopus_Crawler.get_cookies import get_cookies
from src.Scopus_Crawler.data_write import write2sql
from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password


# 浏览器选项
options = webdriver.ChromeOptions()
# 添加代理地址和header
options.add_argument('--proxy-server=202.120.43.93:8059')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/81.0.4044.138 Safari/537.36')

# 期刊引证数据地址地址
base_url = 'https://www.scopus.com/source/retrieveDocs.uri?' \
           'sourceId=%s' \
           '&year=2019&docType=cc' \
           '&pg=%s'


def start_driver():
    # 启动浏览器
    driver = webdriver.Chrome(driver_path, options=options)
    return driver


def get_cite_data(input_data):
    count = 0
    while count < len(input_data):
        result_df_list = []
        # 启动浏览器并获取cookies
        driver = start_driver()
        cookies = get_cookies(driver)
        driver.close()
        try:
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                cite_journal_list = []
                get_page_url = base_url % (input_data[i][0], str(1))
                page_info = requests.get(get_page_url, proxies=proxies, headers=headers,
                                         timeout=300, cookies=cookies).json()
                cite_journal_list += [k['srctitle'] for k in page_info['docs']]
                for j in range(2, int(page_info['Pages']) + 1):
                    url = base_url % (input_data[i][0], str(j))
                    cite_info = requests.get(url, proxies=proxies, headers=headers, timeout=300, cookies=cookies)
                    cite_info_dict = cite_info.json()
                    cite_journal_list += [k['srctitle'] for k in cite_info_dict['docs']]

                cite_df_temp = pd.DataFrame(data=cite_journal_list, columns=['cite_journal'])
                cite_df_temp['cite_num'] = 1
                cite_journal_data = cite_df_temp.groupby(by=['cite_journal'], as_index=False).sum()
                cite_journal_data['scopus_journal_id'] = input_data[i][0]
                result_df_list.append(cite_journal_data)

            count = len(input_data)

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            count = i

        if result_df_list:
            all_data = pd.concat(result_df_list)
            write2sql([['scopus_cite_data', all_data]])


if __name__ == '__main__':
    dbutil = DBUtil(host, port, database, username, password)
    sql = 'select scopus_journal_id from scopus_journal_id where scopus_journal_id not ' \
          'in (select distinct scopus_journal_id from scopus_cite_data) and cite_num!="0"'
    journal_id_df = dbutil.get_allresult(sql, 'df')
    dbutil.close()

    input_data = journal_id_df.values.tolist()
    get_cite_data(input_data)
