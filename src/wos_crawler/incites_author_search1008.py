#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import json

from src.Scopus_Crawler.scopus_config import headers
from src.Scopus_Crawler.data_write import write2sql
from src.wos_crawler.author_name_deal import pinyin_trans2
from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password


headers['content-type'] = 'application/json'
post_url = 'https://incites.clarivate.com/incites-app/explore/0/person/data/table/page?queryDataCollection=ESCI'

login_url = 'https://login.incites.clarivate.com/?DestApp=IC2&locale=en_US&Alias=IC2'
login_data = 'username=496733391%40qq.com&password=liang950113ZOU%21&IPStatus=IPValid'
headers_login = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                              'e/81.0.4044.138 Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded'
}

post_data = {"take": 100000, "skip": 0, "sortBy": "timesCited", "sortOrder": "desc",
             "filters": {"period": {"is": [2010, 2019]}, "personIdTypeGroup": {"is": "name"},
                         "clbrprsnIdTypeGroup": {"is": "name"}, "articletype": {"is": ["Article", "Review"]},
                         "schema": {"is": "Web of Science"}, "publisherType": {"is": "All"}, "fundingAgencyType":
                             {"is": "All"}, "personIdType": {"is": "fullName"}, "personId": {"is": []},
                         "clbrprsnIdType": {"is": "fullName"}}, "pinned": [],
             "indicators": ["key", "seqNumber", "prsnName", "rank", "affiliation", "percentCited", "wosDocuments",
                            "timesCited", "norm", "intCollaborations", "highlyCitedPapers", "hindex", "hasAffiliation"]}

dbutil = DBUtil(host, port, database, username, password)
sql = "select journalTitle from wos_journal_data where category_id in ('AA','SY','UB','UH','UK','UF'," \
      "'UR','UI','UN','UP') and flag='Q1'"
q1_df = dbutil.get_allresult(sql, 'df')
dbutil.close()
q1_df['journalTitle'] = q1_df['journalTitle'].str.upper()
q1_list = list(q1_df['journalTitle'])


def get_doc_data(input_data, author_position, period):
    if period == '近10年':
        post_data['filters']['period']['is'] = [2010, 2019]

    if period == '近5年' or period == '近5年Q1':
        post_data['filters']['period']['is'] = [2015, 2019]

    if 'authorposition' in post_data['filters']:
        post_data['filters']['authorposition']['is'] = [author_position]
        if author_position == 'First & Corresponding':
            post_data['filters']['authorposition']['is'] = ['First', 'Corresponding']
        if author_position == 'All':
            del post_data['filters']['authorposition']

    if author_position == 'First & Corresponding':
        post_data['filters']['authorposition'] = {"is": ['First', 'Corresponding']}

    a = post_data
    count = 0
    no_result = []
    while count < len(input_data):
        result_df_list = []
        try:
            session = requests.session()
            session.post(url=login_url, data=login_data, headers=headers_login, timeout=300)
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                post_data['filters']['personId']['is'] = input_data[i][2]
                author_data = session.post(url=post_url, data=json.dumps(post_data), headers=headers, timeout=300).json()
                if author_data['items']:
                    for item in author_data['items']:
                        item['doc_num'] = item['wosDocuments']['value']
                        item['highly_cited_paper'] = item['highlyCitedPapers']['value']
                        item['inter_colla'] = item['intCollaborations']['value']
                        del item['wosDocuments']
                        del item['highlyCitedPapers']
                        del item['intCollaborations']

                    data_df = pd.DataFrame(data=author_data['items'])
                    data_df['person_id'] = input_data[i][0]
                    data_df['name_zh'] = input_data[i][1]
                    result_df_list.append(data_df)

                else:
                    no_result.append([input_data[i][0], input_data[i][1], author_position, 0])

            count = len(input_data)
            session.close()

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            session.close()
            count = i

        if result_df_list:
            all_data_df = pd.concat(result_df_list)
            all_data_df['author_position'] = author_position
            all_data_df['period'] = period
            write2sql([['incites_author_data1008', all_data_df]])

    if no_result:
        no_result_df = pd.DataFrame(data=no_result, columns=['人才编号', '姓名', '作者类型', '文献数量'])
        no_result_df.to_excel('C:/Users/Administrator/Desktop/no_result1008.xlsx', index=False)


if __name__ == '__main__':
    input_data_df = pd.read_excel('C:/Users/Administrator/Desktop/物理学人才清单_20200908.xlsx', sheet_name='Sheet4')
    input_data = pinyin_trans2(input_data_df)

    period_list = ['近10年', '近5年']
    author_position_list = ['First & Corresponding']

    for ele in author_position_list:
        for period in period_list:
            get_doc_data(input_data, ele, period)

