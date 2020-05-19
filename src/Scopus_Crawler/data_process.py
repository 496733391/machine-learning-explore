#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

import pandas as pd
import pypinyin

from src.Scopus_Crawler.scopus_config import compound_surname, polyphony_surname


def data_process(input_df):
    '''

    :param input_df: dataframe,columns=['person_id', 'name', 'rankaff_name', 'rankaff_id', 'ins_en', 'aff_id']
    :return: [{'person_id':1234564, 'name':'liu bo', 'ins':['fudan university', 'xx university', 'xxx university'],
                'ins_id':[111, 222, 333], 'name_zh':'刘博'}, {...}]
    '''
    input_data = []
    for value, sub_df in input_df.groupby('person_id'):
        row_dict = {}
        row_dict['person_id'] = value
        row_dict['ins'] = list(sub_df['ins_en'])
        row_dict['ins_id'] = list(sub_df['aff_id'])

        name_zh = sub_df.iloc[0]['name']
        row_dict['name_zh'] = name_zh
        name_py = pypinyin.slug(name_zh, separator='-').replace('v', 'ü')
        name_list = name_py.split('-')
        # 如果是复姓
        if name_zh[:2] in compound_surname:
            row_dict['name'] = ''.join(name_list[0:2]).capitalize() + ' ' + ''.join(name_list[2:]).capitalize()
        # 如果是多音字姓
        elif name_zh[:1] in polyphony_surname.keys():
            row_dict['name'] = polyphony_surname[name_zh[:1]] + ' ' + ''.join(name_list[1:]).capitalize()
        # 非复姓非多音字姓
        else:
            row_dict['name'] = ''.join(name_list[0:1]).capitalize() + ' ' + ''.join(name_list[1:]).capitalize()

        input_data.append(row_dict)

    return input_data


if __name__ == '__main__':
    # 测试用，从本地excel中读数据
    input_df = pd.read_excel('C:/Users/Administrator/Desktop/test_data/test_data.xlsx')
    input_df.rename(columns={'学者代码': 'person_id',
                             '姓名': 'name',
                             '头衔当选单位': 'rankaff_name',
                             '软科代码': 'rankaff_id'}, inplace=True)

    input_data = data_process(input_df)
