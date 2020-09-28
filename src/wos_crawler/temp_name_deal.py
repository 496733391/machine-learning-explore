#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd


def ttt():
    df = pd.read_excel('C:/Users/Administrator/Desktop/no_result0917.xlsx')
    df = df.loc[df['pinyin'].notnull()]
    result_list = []
    for i in range(len(df)):
        p_list = df.iloc[i]['pinyin'].split(' ')
        if df.iloc[i]['姓名'] == '王恩':
            name_pinyin_list = ['Wang, EN']
        elif df.iloc[i]['姓名'] in ['李理', '李力', '李丽', '李莉']:
            name_pinyin_list = ['Li li', 'Li, LI']
        elif df.iloc[i]['姓名'] == '沈卡':
            name_pinyin_list = ['Shen, KA']
        else:
            first_name = p_list[0].capitalize()
            last_name1 = '-'.join(p_list[1:]).capitalize()
            last_name2 = ''.join(p_list[1:]).capitalize()
            last_name3 = ' '.join(p_list[1:]).capitalize()
            last_name4 = '-'.join([k.capitalize() for k in p_list[1:]])
            last_name5 = ''.join([k.capitalize() for k in p_list[1:]])
            last_name6 = ' '.join([k.capitalize() for k in p_list[1:]])
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

        result_list.append([df.iloc[i]['人才编号'], df.iloc[i]['姓名'], list(set(name_pinyin_list))])

    return result_list


if __name__ == '__main__':
    ttt()

