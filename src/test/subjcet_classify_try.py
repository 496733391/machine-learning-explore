#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pandas as pd

proxies = {
            "http": "http://202.120.43.93:8059"
}

# headers
headers = {
            'Accept': 'application/json'
}

apikey_list = ['2e63a421d8a260ed9b4f2403f0f6d5db', '20ca1709b7822de4cf70fb2e31e2ac0a',
               '4907f2ddcf925c9f7216aea58e164571', 'e5f9556e1909cc04391a81799355b1b4',
               'd8517c2e251906b5e3ae833e6b619e30']

base_url = 'https://api.elsevier.com/content/search/scopus?' \
           'query=AU-ID({})' \
           '&apiKey=4907f2ddcf925c9f7216aea58e164571' \
           '&start={}' \
           '&count=25&view=complete'

base_url2 = 'https://api.elsevier.com/content/search/scopus?' \
            'query=AU-ID({})' \
            '&apiKey=4907f2ddcf925c9f7216aea58e164571' \
            '&start={}' \
            '&count=25'


def get_co_author(input_data):
    k = 1
    find_list = []
    while k < 1:
        to_find_set = set(input_data).difference(set(find_list))
        k += 1
        for author_id in to_find_set:
            find_list.append(author_id)
            for j in range(1000):
                url = base_url.format(author_id, str(j*25))
                author_article_info = requests.get(url=url, proxies=proxies, headers=headers).json()
                if 'service-error' in author_article_info:
                    break

                if 'entry' not in author_article_info['search-results']:
                    break

                if 'error' in author_article_info['search-results']['entry'][0]:
                    break

                for article_dict in author_article_info['search-results']['entry']:
                    author_id_list = [i['authid'] for i in article_dict['author']]
                    if len(author_id_list) < 10:
                        input_data += author_id_list
    return set(input_data)


def get_publication(input_author_id):
    result_list = []
    count = 0
    while count < len(input_author_id):
        try:
            for i in range(count, len(input_author_id)):
                print('当前进度：%s / %s' % (i + 1, len(input_author_id)))
                author_id = input_author_id[i]
                for j in range(1000):
                    url = base_url2.format(author_id, str(j * 25))
                    author_article_info = requests.get(url=url, proxies=proxies, headers=headers).json()
                    if 'service-error' in author_article_info:
                        break

                    if 'entry' not in author_article_info['search-results']:
                        break

                    if 'error' in author_article_info['search-results']['entry'][0]:
                        break

                    for article_dict in author_article_info['search-results']['entry']:
                        scopus_article_id = article_dict['dc:identifier'][10:]
                        publication = article_dict.get('prism:publicationName', '')
                        result_list.append([author_id, scopus_article_id, publication])

            count = len(input_author_id)

        # 出现错误时，从错误处中断，再从该处开始
        except Exception as err:
            print('ERROR:%s' % err)
            count = i

    result_df = pd.DataFrame(data=result_list, columns=['author_id', 'scopus_article_id', 'publication'])
    result_df.to_excel('C:/Users/Administrator/Desktop/系统科学期刊统计.xlsx', index=False)


if __name__ == '__main__':
    input_data = ['56984215000',
'55966759800',
'26039230700',
'14059260100',
'55794370100',
'55723019300',
'7003734499',
'11139324700',
'57201570977',
'55733323100',
'18439000200',
'16687313600',
'26024156500',
'7401629977',
'56979720300',
'35077414600',
'56489059800',
'35195159100',
'56196546400',
'55763794609']
    input_author_id = list(get_co_author(input_data))
    get_publication(input_author_id)
