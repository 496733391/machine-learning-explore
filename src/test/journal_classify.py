#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from itertools import product
import json


def reduce_mem_usage(df):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    end_mem = df.memory_usage().sum() / 1024**2
    print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    return df


def cite_data_deal():
    cited_data = pd.read_csv('C:/Users/Administrator/Desktop/jcr_data/Cited Journal Data.txt', header=None,
                             names=['source', 'data_type', 'journal', 'id', 'impact_factor', 'cited_journal', 'cited_num'])

    citing_data = pd.read_csv('C:/Users/Administrator/Desktop/jcr_data/Citing Journal Data.txt', header=None,
                              names=['source', 'data_type', 'journal', 'id', 'impact_factor', 'citing_journal', 'citing_num'], encoding='latin-1')

    cited_data = cited_data.loc[~cited_data['id'].isin([1, 2]), ['journal', 'impact_factor', 'cited_journal', 'cited_num']]
    citing_data = citing_data.loc[~citing_data['id'].isin([1, 2]), ['journal', 'impact_factor', 'citing_journal', 'citing_num']]

    cited_data = reduce_mem_usage(cited_data)
    citing_data = reduce_mem_usage(citing_data)

    return cited_data, citing_data


def key_word_selected():
    journal_data = pd.read_excel('C:/Users/Administrator/Desktop/jcr_data/journal_data.xlsx')
    subject_data = pd.read_excel('C:/Users/Administrator/Desktop/jcr_data/subject_data.xlsx')
    subject_data = subject_data.loc[:, ['WOS学科英文名', '2018软科学科英文名']]
    subject_data.drop_duplicates(subset=['WOS学科英文名'], inplace=True, ignore_index=True)
    subject_data['2018软科学科英文名'] = subject_data['2018软科学科英文名']

    key_word = ['Key word 1', 'Key word 2', 'Key word 3', 'Key word 4']
    research_area = ['Research area 1', 'Research area 2', 'Research area 3',
                     'Research area 4', 'Research area 5', 'Research area 6']

    df_list = []
    for tup in product(key_word, research_area):
        columns_lis = list(tup)
        df = journal_data.loc[journal_data[columns_lis[0]].notnull() & journal_data[columns_lis[1]].notnull(), columns_lis]
        df.rename(columns={columns_lis[0]: 'key_word', columns_lis[1]: 'research_area'}, inplace=True)
        df_list.append(df)

    key_area = pd.concat(df_list)
    group_df = key_area.groupby(by=['key_word', 'research_area']).size().reset_index(name='count')
    group_df.sort_values(by=['research_area', 'count'], ascending=[1, 0], inplace=True, ignore_index=True)

    ranking_subject_set = set(subject_data['2018软科学科英文名'])

    subject_kw_dict = {}
    for ranking_subject in ranking_subject_set:
        one_subject_key_word = group_df.loc[group_df['research_area'] == ranking_subject, 'key_word'].values.tolist()
        matched_key_word = []
        disturb_key_word = []
        for kw in one_subject_key_word:
            temp_df = journal_data.loc[(journal_data['Key word 2'].isnull()) &
                                       (journal_data['Key word 1'] == kw) &
                                       (journal_data['Research area 2'].isnull())]
            if len(temp_df) > 0:
                if len(temp_df.loc[temp_df['Research area 1'] == ranking_subject]) / len(temp_df) >= 0.8:
                    matched_key_word.append(kw)
                else:
                    disturb_key_word.append(kw)
            else:
                temp_df = journal_data.loc[((journal_data['Key word 1'] == kw) |
                                            (journal_data['Key word 2'] == kw) |
                                            (journal_data['Key word 3'] == kw) |
                                            (journal_data['Key word 4'] == kw)) &
                                           (journal_data['Research area 2'].isnull())]

                if len(temp_df) > 0:
                    if len(temp_df.loc[temp_df['Research area 1'] == ranking_subject]) / len(temp_df) >= 0.8:
                        matched_key_word.append(kw)
                    else:
                        disturb_key_word.append(kw)
                else:
                    disturb_key_word.append(kw)

        subject_kw_dict[ranking_subject] = [matched_key_word, disturb_key_word]

    subject_kw_json = json.dumps(subject_kw_dict, indent=4)
    with open('subject_kw.json', 'w') as js:
        js.write(subject_kw_json)


def core_journal_selected():
    journal_data = pd.read_excel('C:/Users/Administrator/Desktop/jcr_data/journal_data.xlsx')
    with open('subject_kw.json', 'r') as skw:
        subject_kw_dict = json.load(skw)

    subject_core_journal_dict = {}
    for key, value in subject_kw_dict.items():
        subject_journal = journal_data.loc[((journal_data['Key word 1'].isin(value[0])) |
                                            (journal_data['Key word 2'].isin(value[0])) |
                                            (journal_data['Key word 3'].isin(value[0])) |
                                            (journal_data['Key word 4'].isin(value[0]))) &
                                           (~journal_data['Key word 1'].isin(value[1])) &
                                           (~journal_data['Key word 2'].isin(value[1])) &
                                           (~journal_data['Key word 3'].isin(value[1])) &
                                           (~journal_data['Key word 4'].isin(value[1])) &
                                           ((journal_data['Research area 1'] == key) |
                                            (journal_data['Research area 2'] == key) |
                                            (journal_data['Research area 3'] == key) |
                                            (journal_data['Research area 4'] == key) |
                                            (journal_data['Research area 5'] == key) |
                                            (journal_data['Research area 6'] == key))]
        subject_core_journal_dict[key] = list(subject_journal['Abb'])

    subject_core_journal_json = json.dumps(subject_core_journal_dict, indent=4)
    with open('subject_core_journal.json', 'w') as js:
        js.write(subject_core_journal_json)


cited_data, citing_data = cite_data_deal()
with open('subject_core_journal.json', 'r') as js:
    subject_core_journal_dict = json.load(js)

result_list = []
physics_dict = {'Physics': subject_core_journal_dict['Physics']}
for key, value in physics_dict.items():
    print(key)
    # 被学科核心期刊引用过的期刊
    cited_journal_list = list(cited_data[cited_data['cited_journal'].isin(value)]['journal'])
    # 引用过学科核心期刊的期刊
    citing_journal_list = list(citing_data[citing_data['citing_journal'].isin(value)]['journal'])
    related_journal_set = set(value + cited_journal_list + citing_journal_list)
    print(len(related_journal_set))
    for journal in related_journal_set:
        rf_cited = sum(cited_data[(cited_data['journal'] == journal) &
                                  (cited_data['cited_journal'] != journal) &
                                  (cited_data['cited_journal'].isin(value))]['cited_num']) / \
                   sum(cited_data[(cited_data['journal'] == journal) &
                                  (cited_data['cited_journal'] != journal)]['cited_num']) \
                   if sum(cited_data[(cited_data['journal'] == journal) &
                                     (cited_data['cited_journal'] != journal)]['cited_num']) else 0

        rf_citing = sum(citing_data[(citing_data['journal'] == journal) &
                                    (citing_data['citing_journal'] != journal) &
                                    (citing_data['citing_journal'].isin(value))]['citing_num']) / \
                    sum(citing_data[(citing_data['journal'] == journal) &
                                    (citing_data['citing_journal'] != journal)]['citing_num']) \
                    if sum(citing_data[(citing_data['journal'] == journal) &
                                       (citing_data['citing_journal'] != journal)]['citing_num']) else 0

        result_list.append([journal, key, rf_cited, rf_citing])

result_df = pd.DataFrame(data=result_list, columns=['journal_name', 'subject', 'rf_cited', 'rf_citing'])
result_df.to_excel('C:/Users/Administrator/Desktop/jcr_data/rf_cite_data.xlsx', index=False)


# if __name__ == '__main__':
#     core_journal_selected()
