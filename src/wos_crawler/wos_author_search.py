#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

import requests
import re
import math
import pandas as pd

from src.Scopus_Crawler.scopus_config import proxies
from src.Scopus_Crawler.data_write import write2sql
from src.wos_crawler.author_name_deal import pinyin_trans
from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password


url = 'http://www.webofscience.com/'
post_url = 'http://apps.webofknowledge.com/UA_GeneralSearch.do'
dl_post_url = 'http://apps.webofknowledge.com/OutboundService.do?action=go&&'

headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53'
                  '7.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}

data_ini = 'fieldCount=4&action=search&product=WOS&search_mode=GeneralSearch&' \
           'SID={}' \
           '&max_field_count=25&max_field_notice=%E6%B3%A8%E6%84%8F%3A+%E6%97%A0%E6%B3%95%E6%B7%BB%' \
           'E5%8A%A0%E5%8F%A6%E4%B8%80%E5%AD%97%E6%AE%B5%E3%80%82&input_invalid_notice=%E6%A3%80%E' \
           '7%B4%A2%E9%94%99%E8%AF%AF%3A+%E8%AF%B7%E8%BE%93%E5%85%A5%E6%A3%80%E7%B4%A2%E8%AF%8D%E3%' \
           '80%82&exp_notice=%E6%A3%80%E7%B4%A2%E9%94%99%E8%AF%AF%3A+%E4%B8%93%E5%88%A9%E6%A3%80%E7%' \
           'B4%A2%E8%AF%8D%E5%8F%AF%E4%BB%A5%E5%9C%A8%E5%A4%9A%E4%B8%AA%E5%AE%B6%E6%97%8F%E4%B8%AD%E' \
           '6%89%BE%E5%88%B0+%28&input_invalid_notice_limits=+%3Cbr%2F%3E%E6%B3%A8%E6%84%8F%3A+%E6%B' \
           'B%9A%E5%8A%A8%E6%A1%86%E4%B8%AD%E6%98%BE%E7%A4%BA%E7%9A%84%E5%AD%97%E6%AE%B5%E5%BF%85%E9' \
           '%A1%BB%E8%87%B3%E5%B0%91%E4%B8%8E%E4%B8%80%E4%B8%AA%E5%85%B6%E4%BB%96%E6%A3%80%E7%B4%A2%' \
           'E5%AD%97%E6%AE%B5%E7%9B%B8%E7%BB%84%E9%85%8D%E3%80%82&' \
           'sa_params=WOS%7C%7C{}' \
           '%7Chttp%3A%2F%2Fapps.webofknowledge.com%7C%27&formUpdated=true' \
           '&value%28input1%29=2010-2019' \
           '&value%28select1%29=PY' \
           '&value%28hidInput1%29=' \
           '&value%28bool_1_2%29=AND' \
           '&value%28input2%29=Article%23%23%23+Review' \
           '&value%28select2%29=DT' \
           '&value%28hidInput2%29=' \
           '&value%28bool_2_3%29=AND' \
           '&value%28input3%29={}' \
           '&value%28select3%29=AU' \
           '&value%28hidInput3%29=' \
           '&value%28bool_3_4%29=AND' \
           '&value%28input4%29=china' \
           '&value%28select4%29=AD' \
           '&value%28hidInput4%29=' \
           '&limitStatus=expanded&ss_lemmatization=On&ss_spellchecking=Suggest&SinceLastVisit_UTC=' \
           '&SinceLastVisit_DATE=&range=CUSTOM' \
           '&period=Year+Range&startYear=2010&endYear=2019' \
           '&editions=SCI' \
           '&editions=SSCI' \
           '&editions=AHCI' \
           '&update_back2search_link_param=yes&ssStatus=display%3Anone&ss_showsuggestions=ON' \
           '&ss_numDefaultGeneralSearchFields=1&ss_query_language=&rs_sort_by=PY.D%3BLD.D%3BSO.A%3BVL.D%3BPG.A%3BAU.A'

data_dl_ini = 'selectedIds=&displayCitedRefs=true&displayTimesCited=true&displayUsageInfo=true&viewType=summary' \
              '&product=WOS' \
              '&rurl=http%253A%252F%252Fapps.webofknowledge.com%252Fsummary.do%253Fproduct%253DWOS%2526' \
              'search_mode%253DGeneralSearch%2526' \
              'qid%253D{}%2526' \
              'SID%{}' \
              '&mark_id=WOS&colName=WOS&search_mode=GeneralSearch&locale=zh_CN&view_name=WOS-summary' \
              '&sortBy=PY.D%3BLD.D%3BSO.A%3BVL.D%3BPG.A%3BAU.A&mode=OpenOutputService' \
              '&qid={}' \
              '&SID={}' \
              '&format=saveToFile&filters=HIGHLY_CITED+HOT_PAPER+OPEN_ACCESS+PMID+USAGEIND+AUTHORSIDEN' \
              'TIFIERS+ACCESSION_NUM+FUNDING+SUBJECT_CATEGORY+JCR_CATEGORY+LANG+IDS+PAGEC+SABBR+CITREF' \
              'C+ISSN+PUBINFO+KEYWORDS+CITTIMES+ADDRS+CONFERENCE_SPONSORS+DOCTYPE+CITREF+ABSTRACT+CON' \
              'FERENCE_INFO+SOURCE+TITLE+AUTHORS++&mark_to={}&mark_from={}' \
              '&queryNatural=%3Cb%3E%E5%87%BA%E7%89%88%E5%B9%B4%3A%3C%2Fb%3E+%282010-2019%29+%3Ci%3E' \
              'AND%3C%2Fi%3E+%3Cb%3E%E6%96%87%E7%8C%AE%E7%B1%BB%E5%9E%8B%3A%3C%2Fb%3E+%28Article+OR++Review%29+%3Ci%3E' \
              'AND%3C%2Fi%3E+%3Cb%3E%E4%BD%9C%E8%80%85%3A%3C%2Fb%3E+%28{}%29+%3Ci%3E' \
              'AND%3C%2Fi%3E+%3Cb%3E%E5%9C%B0%E5%9D%80%3A%3C%2Fb%3E+%28china%29' \
              '&count_new_items_marked=0&use_two_ets=false&IncitesEntitled=yes&value%28record_select_type%29=range' \
              '&markFrom={}&markTo={}' \
              '&fields_selection=HIGHLY_CITED+HOT_PAPER+OPEN_ACCESS+PMID+USAGEIND+AUTHORSIDENTIFIERS+ACCESS' \
              'ION_NUM+FUNDING+SUBJECT_CATEGORY+JCR_CATEGORY+LANG+IDS+PAGEC+SABBR+CITREFC+ISSN+PUBINFO+KEY' \
              'WORDS+CITTIMES+ADDRS+CONFERENCE_SPONSORS+DOCTYPE+CITREF+ABSTRACT+CONFERENCE_INFO+SOURCE+TITL' \
              'E+AUTHORS++&save_options=tabWinUTF8'

columns = ['PT', 'AU', 'BA', 'BE', 'GP', 'AF', 'BF', 'CA', 'TI', 'SO', 'SE', 'BS', 'LA', 'DT', 'CT',
           'CY', 'CL', 'SP', 'HO', 'DE', 'ID', 'AB', 'C1', 'RP', 'EM', 'RI', 'OI', 'FU', 'FX', 'CR',
           'NR', 'TC', 'Z9', 'U1', 'U2', 'PU', 'PI', 'PA', 'SN', 'EI', 'BN', 'J9', 'JI', 'PD', 'PY',
           'VL', 'IS', 'PN', 'SU', 'SI', 'MA', 'BP', 'EP', 'AR', 'DI', 'D2', 'EA', 'PG', 'WC', 'SC',
           'GA', 'UT', 'PM', 'OA', 'HC', 'HP', 'DA']


def wos_article(input_data):
    count = 0
    page_count = 33
    while count < len(input_data):
        articel_data_all = []
        try:
            # 建立连接session
            session = requests.session()
            connection = session.get(url, headers=headers, proxies=proxies)
            # 获取sid
            sid = re.findall(r'SID=(\w+)&', connection.url)[0]
            # 开始循环获取数据
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                print(input_data[i])

                name = input_data[i][0]
                data = data_ini.format(sid, sid, name)
                search_page = session.post(post_url, data=data, proxies=proxies, headers=headers, timeout=300)

                qid = re.findall(r'qid=([0-9]+)&', search_page.text)[0]
                search_result_num = re.findall(r'FINAL_DISPLAY_RESULTS_COUNT = ([0-9]+);', search_page.text)[0]
                print(search_result_num)
                page_num = math.ceil(int(search_result_num) / 500)

                for k in range(page_count, page_num):
                    print(f'{k}/{page_num}')
                    data_dl = data_dl_ini.format(qid, sid, qid, sid, k*500+500, k*500+1, name, k*500+1, k*500+500)
                    dl_page = session.post(dl_post_url, data=data_dl, proxies=proxies, headers=headers, timeout=300)
                    if ('PT' not in dl_page.text) and ('AU' not in dl_page.text):
                        raise Exception('error')
                    data_list = dl_page.text.strip().split('\n')
                    articel_data_temp = [j.strip().split('\t') for j in data_list[1:]]
                    df_temp = pd.DataFrame(data=articel_data_temp, columns=columns)
                    df_temp['name_zh'] = input_data[i][1]
                    articel_data_all.append(df_temp)

                page_count = 0

            # 结束循环
            count = len(input_data)
            session.close()

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            session.close()
            count = i
            page_count = k

        if articel_data_all:
            articel_data_df = pd.concat(articel_data_all)
            write2sql([['wos_article_data', articel_data_df]])


if __name__ == '__main__':
    # dbutil = DBUtil(host, port, database, username, password)
    # sql = 'select DISTINCT name_zh from wos_article_data'
    # already_df = dbutil.get_allresult(sql, 'df')
    # dbutil.close()

    df = pd.read_excel('C:/Users/Administrator/Desktop/物理学人才清单_20200908.xlsx', sheet_name='Sheet3')
    # df = df.loc[~df['姓名'].isin(list(already_df['name_zh']))]

    df = df.loc[df['姓名'] == '陈栋']

    input_data = df['姓名'].values.tolist()
    input_data = pinyin_trans(input_data)
    # input_data = input_data[:5]
    wos_article(input_data)
