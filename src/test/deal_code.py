#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd

data_all = pd.DataFrame(data=[], columns=[])
for i in range(75):
    data = pd.read_table('savedrecs (%s).txt' % i, sep='\t{1}', usecols=['TI', 'RP', 'C1', 'UT'], engine='python')
    data_all = data_all.append(data, ignore_index=True)

data1 = data_all.loc[:, ['TI', 'C1', 'UT']]
data2 = data_all.loc[:, ['TI', 'RP', 'UT']]

data1.dropna(inplace=True)
data2.dropna(inplace=True)
data1.reset_index(drop=True, inplace=True)
data2.reset_index(drop=True, inplace=True)

result1 = pd.DataFrame(data=None, columns=None)
for i in range(len(data1)):
    temp_df = pd.DataFrame(data=data1.loc[i, 'C1'].split(';'), columns=['AD'])
    temp_df['TI'] = data1.loc[i, 'TI']
    temp_df['UT'] = data1.loc[i, 'UT']
    temp_df['AD_ORDER'] = temp_df.index
    result1 = result1.append(temp_df, ignore_index=True)

result1['AD_TYPE'] = 'C1'

result2 = pd.DataFrame(data=None, columns=None)
for i in range(len(data2)):
    temp_df = pd.DataFrame(data=data2.loc[i, 'RP'].split(';'), columns=['AD'])
    temp_df['TI'] = data2.loc[i, 'TI']
    temp_df['UT'] = data2.loc[i, 'UT']
    temp_df['AD_ORDER'] = temp_df.index
    result2 = result2.append(temp_df, ignore_index=True)

result2['AD_TYPE'] = 'RP'

result = result1.append(result2, ignore_index=True)
result = result[['UT', 'TI', 'AD_TYPE', 'AD_ORDER', 'AD']]
result.to_csv('result.txt', index=0)