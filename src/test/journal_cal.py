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


def rf_cal(core_journal):
    cited_data, citing_data = cite_data_deal()

    # 被学科核心期刊引用过的期刊
    cited_journal_list = list(cited_data[cited_data['cited_journal'].isin(core_journal)]['journal'])
    # 引用过学科核心期刊的期刊
    citing_journal_list = list(citing_data[citing_data['citing_journal'].isin(core_journal)]['journal'])
    related_journal_set = set(core_journal + cited_journal_list + citing_journal_list)
    print(len(related_journal_set))

    result_list = []
    for journal in related_journal_set:
        print(journal)
        rf_cited = sum(cited_data[(cited_data['journal'] == journal) &
                                  (cited_data['cited_journal'] != journal) &
                                  (cited_data['cited_journal'].isin(core_journal))]['cited_num']) / \
                   sum(cited_data[(cited_data['journal'] == journal) &
                                  (cited_data['cited_journal'] != journal)]['cited_num']) \
                   if sum(cited_data[(cited_data['journal'] == journal) &
                                     (cited_data['cited_journal'] != journal)]['cited_num']) else 0

        rf_citing = sum(citing_data[(citing_data['journal'] == journal) &
                                    (citing_data['citing_journal'] != journal) &
                                    (citing_data['citing_journal'].isin(core_journal))]['citing_num']) / \
                    sum(citing_data[(citing_data['journal'] == journal) &
                                    (citing_data['citing_journal'] != journal)]['citing_num']) \
                    if sum(citing_data[(citing_data['journal'] == journal) &
                                       (citing_data['citing_journal'] != journal)]['citing_num']) else 0
        result_list.append([journal, rf_cited, rf_citing])

    return result_list


if __name__ == '__main__':
    key_word = 'landscape design'
    core_journal = ['LANDSCAPE ECOL', 'LANDSCAPE URBAN PLAN', 'LANDSCAPE ARCHITECTURE FRONTIERS',
                    'URBAN FOR URBAN GREE', 'LANDSC ECOL ENG', 'J ENVIRON ENG LANDSC']

    result_list = rf_cal(core_journal)

    result_df = pd.DataFrame(data=result_list, columns=['期刊名称简写', 'rf_cited', 'rf_citing'])
    result_df.to_excel('rf_cite_data.xlsx', index=False)



