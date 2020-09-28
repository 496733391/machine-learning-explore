#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from pypinyin import slug, pinyin, Style
from itertools import product

from src.Scopus_Crawler.scopus_config import compound_surname, polyphony_surname
from src.wos_crawler.temp_name_deal import ttt

polyphony_surname['吕'] = 'Lv'


def pinyin_trans(input_data):
    result = []
    for name_zh in input_data:
        # 如果是复姓
        if name_zh[:2] in compound_surname:
            k = 2
            first_name = slug(name_zh[:2], separator='')

        # 如果是多音字姓
        elif name_zh[:1] in polyphony_surname.keys():
            k = 1
            first_name = polyphony_surname[name_zh[:1]]
        # 非复姓非多音字姓
        else:
            k = 1
            first_name = slug(name_zh[:1], separator='')

        last_name1 = slug(name_zh[k:], separator=' ')
        last_name2 = slug(name_zh[k:], separator='')
        last_name3 = slug(name_zh[k:], separator=' ', style=Style.FIRST_LETTER)
        last_name4 = slug(name_zh[k:], separator='', style=Style.FIRST_LETTER)
        name_py = first_name + ' ' + last_name1 + ' or ' + first_name + ' ' + last_name2 + ' or ' + last_name2 + ' ' + \
                  first_name + ' or ' + first_name + ' ' + last_name3 + ' or ' + first_name + ' ' + last_name4
        result.append([name_py, name_zh])

    return result


def pinyin_trans2(input_data):
    df = pd.read_excel('C:/Users/Administrator/Desktop/no_result0917.xlsx')
    df['人才编号'] = df['人才编号'].astype('str')
    df = df.loc[df['pinyin'].notnull()]
    input_data['人才编号'] = input_data['人才编号'].astype('str')
    input_data = input_data.loc[~input_data['人才编号'].isin(list(df['人才编号']))]
    input_data.reset_index(drop=True, inplace=True)
    result = []
    for i in range(len(input_data)):
        name_zh = input_data.loc[i, '姓名']
        # 如果是复姓
        if name_zh[:2] in compound_surname:
            k = 2
            first_name = slug(name_zh[:2], separator='').capitalize()
        # 如果是多音字姓
        elif name_zh[:1] in polyphony_surname.keys():
            k = 1
            first_name = polyphony_surname[name_zh[:1]]
        # 非复姓非多音字姓
        else:
            k = 1
            first_name = slug(name_zh[:1], separator='').capitalize()

        last_name1 = slug(name_zh[k:], separator='-').capitalize()
        last_name2 = slug(name_zh[k:], separator='').capitalize()
        last_name3 = slug(name_zh[k:], separator=' ').capitalize()
        last_name_pinyin_list = [k[0].capitalize() for k in pinyin(name_zh[k:], style=Style.NORMAL)]
        last_name4 = ' '.join(last_name_pinyin_list)
        last_name5 = '-'.join(last_name_pinyin_list)
        last_name6 = ''.join(last_name_pinyin_list)
        if '长' in name_zh:
            last_name1 = last_name1.replace('zhang', 'chang').replace('Zhang', 'Chang')
            last_name2 = last_name2.replace('zhang', 'chang').replace('Zhang', 'Chang')
            last_name3 = last_name3.replace('zhang', 'chang').replace('Zhang', 'Chang')
            last_name4 = last_name4.replace('zhang', 'chang').replace('Zhang', 'Chang')
            last_name5 = last_name5.replace('zhang', 'chang').replace('Zhang', 'Chang')
            last_name6 = last_name6.replace('zhang', 'chang').replace('Zhang', 'Chang')
        name_pinyin_list = [first_name + ' ' + last_name1,
                            first_name + ' ' + last_name2,
                            first_name + ' ' + last_name3,
                            first_name + ' ' + last_name4,
                            first_name + ' ' + last_name5,
                            first_name + ' ' + last_name6,
                            first_name + ', ' + last_name1,
                            first_name + ', ' + last_name2,
                            first_name + ', ' + last_name3,
                            first_name + ', ' + last_name4,
                            first_name + ', ' + last_name5,
                            first_name + ', ' + last_name6,
                            last_name1 + ' ' + first_name,
                            last_name2 + ' ' + first_name,
                            last_name3 + ' ' + first_name,
                            last_name4 + ' ' + first_name,
                            last_name5 + ' ' + first_name,
                            last_name6 + ' ' + first_name,
                            last_name1 + ', ' + first_name,
                            last_name2 + ', ' + first_name,
                            last_name3 + ', ' + first_name,
                            last_name4 + ', ' + first_name,
                            last_name5 + ', ' + first_name,
                            last_name6 + ', ' + first_name]

        result.append([input_data.loc[i, '人才编号'], input_data.loc[i, '姓名'], list(set(name_pinyin_list))])

    another_data = ttt()
    result.extend(another_data)

    return result


if __name__ == '__main__':
    df = pd.read_excel('C:/Users/Administrator/Desktop/物理学人才清单_20200908.xlsx', sheet_name='Sheet4')
    pinyin_trans2(df)
