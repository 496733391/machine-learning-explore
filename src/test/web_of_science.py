#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

import requests
import re
from bs4 import BeautifulSoup as bs
import pandas as pd

from src.Scopus_Crawler.scopus_config import proxies
from src.Scopus_Crawler.data_write import write2sql


url = 'http://www.webofscience.com/'
post_url = 'http://apps.webofknowledge.com/UA_GeneralSearch.do'

headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53'
                  '7.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}

data_ini = 'fieldCount=2&' \
       'action=search&' \
       'product=WOS&' \
       'search_mode=GeneralSearch&' \
       'SID={}&' \
       'max_field_count=25&' \
       'max_field_notice=%E6%B3%A8%E6%84%8F%3A+%E6%97%A0%E6%B3%95%E6%B7%BB%E5%8A%A0%E5%8F%A6%E4%B8%80%E5%AD%97%E6%AE%B5%E3%80%82&' \
       'input_invalid_notice=%E6%A3%80%E7%B4%A2%E9%94%99%E8%AF%AF%3A+%E8%AF%B7%E8%BE%93%E5%85%A5%E6%A3%80%E7%B4%A2%E8%AF%8D%E3%80%82&' \
       'exp_notice=%E6%A3%80%E7%B4%A2%E9%94%99%E8%AF%AF%3A+%E4%B8%93%E5%88%A9%E6%A3%80%E7%B4%A2%E8%AF%8D%E5%8F%AF%E4%BB%A5%E5%9C%A8%E5%A4%9A%E4%B8%AA%E5%AE%B6%E6%97%8F%E4%B8%AD%E6%89%BE%E5%88%B0+%28&' \
       'input_invalid_notice_limits=+%3Cbr%2F%3E%E6%B3%A8%E6%84%8F%3A+%E6%BB%9A%E5%8A%A8%E6%A1%86%E4%B8%AD%E6%98%BE%E7%A4%BA%E7%9A%84%E5%AD%97%E6%AE%B5%E5%BF%85%E9%A1%BB%E8%87%B3%E5%B0%91%E4%B8%8E%E4%B8%80%E4%B8%AA%E5%85%B6%E4%BB%96%E6%A3%80%E7%B4%A2%E5%AD%97%E6%AE%B5%E7%9B%B8%E7%BB%84%E9%85%8D%E3%80%82&' \
       'sa_params=WOS%7C%7C{}%7Chttp%3A%2F%2Fapps.webofknowledge.com%7C%27&' \
       'formUpdated=true&' \
       'value%28input1%29={}&' \
       'value%28select1%29=AU&' \
       'value%28hidInput1%29=&' \
       'value%28bool_1_2%29=AND&' \
       'value%28input2%29={}&' \
       'value%28select2%29=SO&' \
       'value%28hidInput2%29=&' \
       'limitStatus=collapsed&' \
       'ss_lemmatization=On&' \
       'ss_spellchecking=Suggest&' \
       'SinceLastVisit_UTC=&' \
       'SinceLastVisit_DATE=&' \
       'period=Range+Selection&' \
       'range=ALL&' \
       'startYear=1985&' \
       'endYear=2020&' \
       'editions=SCI&' \
       'editions=SSCI&' \
       'editions=AHCI&' \
       'editions=ISTP&' \
       'editions=ISSHP&' \
       'editions=ESCI&' \
       'editions=CCR&' \
       'editions=IC&' \
       'update_back2search_link_param=yes&' \
       'ssStatus=display%3Anone&' \
       'ss_showsuggestions=ON&' \
       'ss_numDefaultGeneralSearchFields=1&' \
       'ss_query_language=&' \
       'rs_sort_by=PY.D%3BLD.D%3BSO.A%3BVL.D%3BPG.A%3BAU.A'

# 数据源
source_data = pd.read_excel('C:/Users/Administrator/Desktop/data_left.xlsx')
# source_data = source_data.loc[:, ['JCR期刊列表', 'name', 'ins', '姓名', 'person_id']]
source_list = source_data.values.tolist()

count = 0
while count < len(source_list):
    # 建立连接session
    session = requests.session()
    first = session.get(url, headers=headers, proxies=proxies)
    # 获取sid
    sid = re.findall(r'SID=(\w+)&', first.url)[0]
    find_df_list = []
    not_find = []
    try:
        # 开始循环获取数据
        for i in range(count, len(source_list)):
            # 每过150条重启session
            if i % 150 == 0:
                print('重启seesion')
                session.close()
                session = requests.session()
                first = session.get(url, headers=headers, proxies=proxies)
                # 获取sid
                sid = re.findall(r'SID=(\w+)&', first.url)[0]

            name = source_list[i][3]
            journal = source_list[i][2]

            data = data_ini.format(sid, sid, name, journal)
            search_page = session.post(post_url, data=data, proxies=proxies, headers=headers, timeout=30)

            print(str(i) + ' == ' + name + ' == ' + journal + ' == ' + str(search_page.status_code))

            if search_page.status_code == 200:
                soup = bs(search_page.text, 'lxml')

                find_num = re.findall(r'FINAL_DISPLAY_RESULTS_COUNT = ([0-9]+);', search_page.text)[0]
                ins = soup.find(id='OrgEnhancedName_tr')
                ins_list = [i for i in ins.text.strip().split('\n') if i]
                ins_list.pop()
                ins_list = [i.replace('\u200e', '') for i in ins_list]
                temp_df = pd.DataFrame(data=ins_list, columns=['ins'])
                temp_df['person_id'] = source_list[i][4]
                temp_df['find_num'] = find_num
                if len(temp_df) > 0:
                    find_df_list.append(temp_df)
                else:
                    not_find.append(source_list[i][4])

            else:
                not_find.append(source_list[i][4])

        # 结束循环
        count = len(source_list)

    # 出现错误时，从错误处中断，再从该处开始
    except Exception as err:
        print('ERROR:%s' % err)
        print('当前进度：%s / %s' % (i + 1, len(source_list)))
        count = i
        if str(type(err)) == "<class 'UnicodeEncodeError'>":
            count += 1
            not_find.append(source_list[i][4])

    if len(find_df_list) > 0:
        all_find = pd.concat(find_df_list)
    else:
        all_find = pd.DataFrame()

    if len(not_find) > 0:
        all_not_find = pd.DataFrame(data=not_find, columns=['person_id'])
    else:
        all_not_find = pd.DataFrame()

    write2sql([['find_result', all_find], ['not_find', all_not_find]])
