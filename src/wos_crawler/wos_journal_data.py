#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import requests
from selenium import webdriver
import pandas as pd
import json

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

base_url = 'https://jcr.clarivate.com/AllCategoriesJson.action?_dc=1597229885149&jcrYear=2019' \
           '&edition=SSCI' \
           '&subjectCategoryScheme=WoS&page=1&start=0&limit=25'

journal_data_url = 'https://jcr.clarivate.com/JournalHomeGridJson.action?_dc=1597233012104&jcrYear=2019' \
                   '&edition={}' \
                   '&categoryIds={}' \
                   '&subjectCategoryScheme=WoS&jifQuartile=&impactFactorRangeFrom=&impactFactorRangeTo=&averageJifP' \
                   'ercentileRangeFrom=&averageJifPercentileRangeTo=&OAFlag=N&page=1&start=0&limit=10000' \
                   '&sort=%5B%7B%22property%22%3A%22journalImpactFactor%22%2C%22direction%22%3A%22DESC%22%7D%5D'

post_url = 'https://incites.clarivate.com/incites-app/explore/0/organization/data/table/page'

login_url = 'https://login.incites.clarivate.com/?DestApp=IC2&locale=en_US&Alias=IC2'
login_data = 'username=496733391%40qq.com&password=liang950113ZOU%21&IPStatus=IPValid'
headers_login = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                              'e/81.0.4044.138 Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded'
}


post_data = {"take": 100000, "skip": 0, "sortBy": "timesCited", "sortOrder": "desc",
             "indicators": ["key", "seqNumber", "orgName", "rank", "wosDocuments", "norm", "timesCited",
                            "percentCited", "hasProfile", "jifdocsq1"],
             "filters": {"orgtype": {"is": ["Academic"]}, "location": {"is": ["CHINA MAINLAND"]},
                         "personIdTypeGroup": {"is": "name"}, "personIdType": {"is": "fullName"},
                         "schema": {"is": "China SCADC Subject 97 Narrow"}, "sbjname": {"is": ["ACOUSTICS"]},
                         "publisherType": {"is": "All"}, "articletype": {"is": ["Article"]},
                         "period": {"is": [2015, 2015]}}, "pinned": []}


# session = requests.session()
# session.post(url=login_url, data=login_data, headers=headers_login, timeout=300)
# url = 'https://incites.clarivate.com/incites-app/explore/0/filter/categories?schema=China+SCADC+Subject+97+Narrow'
#
# subject_list = session.get(url, headers=headers).json()


def get_doc_data(input_data):
    headers['content-type'] = 'application/json'
    count = 0
    while count < len(input_data):
        result_df_list = []
        try:
            session = requests.session()
            session.post(url=login_url, data=login_data, headers=headers_login, timeout=300)
            for i in range(count, len(input_data)):
                print('当前进度：%s / %s' % (i + 1, len(input_data)))
                for year in range(2015, 2020):
                    post_data['filters']['sbjname']['is'] = input_data[i]
                    post_data['filters']['period']['is'] = [year, year]
                    doc_data = session.post(url=post_url, data=json.dumps(post_data), headers=headers, timeout=300).json()
                    if doc_data['items']:
                        for item in doc_data['items']:
                            item['doc_num'] = item['jifdocsq1']['value']
                            del item['jifdocsq1']
                            del item['wosDocuments']

                        data_df = pd.DataFrame(data=doc_data['items'])
                        data_df['year'] = year
                        data_df['category_id'] = input_data[i][:4]
                        data_df['category_name'] = input_data[i][5:]
                        result_df_list.append(data_df)

            count = len(input_data)
            session.close()

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            session.close()
            count = i

        if result_df_list:
            all_data_df = pd.concat(result_df_list)
            write2sql([['wos_doc_data_copy', all_data_df]])


if __name__ == '__main__':
    input_data = ['0101 Philosophy', '0201 Theoretical Economics', '0202 Applied Economics', '0301 Law', '0302 Political Science', '0303 Sociology', '0304 Ethnology', '0401 Education', '0402 Psychology', '0403 Physical Education and Sport Science', '0502 Foreign Language and Literature', '0503 Journalism and Communication', '0601 Archaeology', '0602 History of China', '0603 World History', '0701 Mathematics', '0702 Physics', '0703 Chemistry', '0704 Astronomy', '0705 Geography', '0706 Atmospheric Science', '0707 Marine Science', '0708 Geophysics', '0709 Geology', '0710 Biology', '0711 Systems Science', '0712 History of Science and Technology', '0713 Ecology', '0714 Statistics', '0801 Mechanics', '0802 Mechanical Engineering', '0803 Optical Engineering', '0804 Instrumentation Science and Technology', '0805 Materials Science and Engineering', '0806 Metallurgical Engineering', '0807 Power Engineering and Engineering Thermophysics', '0808 Electrical Engineering', '0809 Electronic Science and Technology', '0810 Information and Communication Engineering', '0811 Control Science and Engineering', '0812 Computer Science and Technology', '0813 Architecture', '0814 Civil Engineering', '0815 Hydraulic Engineering', '0816 Surveying and Mapping', '0817 Chemical Engineering and Technology', '0818 Geological Resources and Geological Engineering', '0819 Mining Engineering', '0820 Oil and Natural Gas Engineering', '0821 Textile Science and Engineering', '0822 Light Industry Technology and Engineering', '0823 Transportation Engineering', '0824 Naval Architecture and Ocean Engineering', '0825 Aerospace Science and Technology', '0826 Armament Science and Technology', '0827 Nuclear Science and Technology', '0828 Agricultural Engineering', '0829 Forestry Engineering', '0830 Environmental Science and Engineering', '0831 Biomedical Engineering', '0832 Food Science and Engineering', '0833 Urban and Rural Planning', '0834 Landscape Architecture', '0835 Software Engineering', '0836 Biotechnology and Bioengineering', '0837 Safety Science and Engineering', '0839 Cyberspace Security', '0901 Crop Science', '0902 Horticulture', '0903 Agricultural Resource and Environment Sciences', '0904 Plant Protection', '0905 Animal Science', '0906 Veterinary Medicine', '0907 Forestry', '0908 Fisheries', '0909 Grassland Science', '1001 Basic Medicine', '1002 Clinical Medicine', '1003 Stomatology', '1004 Public Health and Preventive Medicine', '1005 Chinese Medicine', '1007 Pharmaceutical Science', '1008 Chinese Materia Medica', '1009 Special Medicine', '1010 Medical Technology', '1011 Nursing', '1201 Management Science and Engineering', '1202 Business Administration', '1203 Economics and Management of Agriculture and Forestry', '1204 Public Administration', '1205 Library and Information Science & Archive Management', '1301 Art Theory', '1302 Music and Dance', '1303 Drama Film and Television', '1304 Fine Art', '1305 Design', '1401 Cross-field']
    get_doc_data(input_data)

