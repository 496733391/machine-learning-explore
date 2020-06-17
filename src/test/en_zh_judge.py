#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from pypinyin import slug, pinyin, Style
import re

# 多音字姓氏
polyphony_surname = {'曾': 'zeng', '单': 'shan', '呙': 'guo', '吕': 'lü', '柏': 'bai', '查': 'zha',
                     '仇': 'qiu', '都': 'du', '郝': 'hao', '解': 'xie', '乐': 'le', '缪': 'miao',
                     '覃': 'qin', '翟': 'zhai'}

# 中文姓
with open('C:/Users/Administrator/Desktop/中文姓氏.txt', 'r', encoding='utf8') as fl:
    surname_str = fl.read()

surname_list = surname_str.replace(', ', ',').split(',')
# 中文姓氏转拼音
# surname_py_list = [slug(i, separator='').replace('v', 'ü') for i in surname_list]
surname_py_list = [polyphony_surname[i] if i in polyphony_surname.keys() else slug(i, separator='').replace('v', 'ü') for i in surname_list]
surname_py_list.append('lv')

surname_py_list.remove('de')
surname_py_list.remove('a')

print(surname_py_list)

source_data = pd.read_excel('C:/Users/Administrator/Desktop/编委是否为华人判断.xlsx')
source_data.drop(columns=['是否为华人'], inplace=True)
source_data.dropna(inplace=True)
source_data['姓名'] = source_data['姓名'].astype('str')

name_list = list(source_data['姓名'])

# 先不区分大小写，筛选出错误的
error_list = []

for name in name_list:
    # 将姓名拆分为list
    one_name_list = re.split(r'\s+', name)
    # 是否存在姓氏拼音
    if len(set(one_name_list).intersection(set(surname_py_list))) >= 1:
        error_list.append(name)

ch = []
not_ch = []

for name in name_list:
    # 将姓名拆分为list
    one_name_list = re.split(r'\s+', name.lower())
    # 是否存在姓氏拼音
    if len(set(one_name_list).intersection(set(surname_py_list))) >= 1:
        ch.append(name)
    else:
        not_ch.append(name)

ch_df = pd.DataFrame(data=ch, columns=['姓名'])
ch_df['是否为华人'] = 1
not_ch_df = pd.DataFrame(data=not_ch, columns=['姓名'])
not_ch_df['是否为华人'] = 0

result = ch_df.append(not_ch_df, ignore_index=True)

result.to_excel('C:/Users/Administrator/Desktop/编委是否为华人判断结果.xlsx', encoding='utf8', index=False)

