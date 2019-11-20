#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import sys
import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt

from copy import deepcopy
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../../")
print(BASE_DIR)
sys.path.insert(0, BASE_DIR)


seed = 201910
# 读取数据
if pd.__version__ >= '0.25.1':
    error_data5 = pd.read_excel(BASE_DIR + '\data/5_9error.xlsx', sheet_name='19_5')
    error_data6 = pd.read_excel(BASE_DIR + '\data/5_9error.xlsx', sheet_name='19_6')
    error_data7 = pd.read_excel(BASE_DIR + '\data/5_9error.xlsx', sheet_name='19_7')
    error_data8 = pd.read_excel(BASE_DIR + '\data/5_9error.xlsx', sheet_name='19_8')
    error_data9 = pd.read_excel(BASE_DIR + '\data/5_9error.xlsx', sheet_name='19_9')

    predict_data = pd.read_excel(BASE_DIR + '\data/10_predict.xlsx', sheet_name='Sheet1')

    part_data = pd.read_excel(BASE_DIR + '\data/month_data.xlsx', sheet_name='Sheet2')
else:
    error_data5 = pd.read_excel(BASE_DIR + '\data/5_9error.xlsx', sheetname='19_5')
    error_data6 = pd.read_excel(BASE_DIR + '\data/5_9error.xlsx', sheetname='19_6')
    error_data7 = pd.read_excel(BASE_DIR + '\data/5_9error.xlsx', sheetname='19_7')
    error_data8 = pd.read_excel(BASE_DIR + '\data/5_9error.xlsx', sheetname='19_8')
    error_data9 = pd.read_excel(BASE_DIR + '\data/5_9error.xlsx', sheetname='19_9')

    predict_data = pd.read_excel(BASE_DIR + '\data/10_predict.xlsx', sheetname='Sheet1')

    part_data = pd.read_excel(BASE_DIR + '\data/month_data.xlsx', sheetname='Sheet2')


# 数据处理
error_data = pd.concat([error_data5, error_data6, error_data7, error_data8, error_data9]).reset_index(drop=True)
error_data['error_real'] = (error_data['origin_predict'] - error_data['actual']) / error_data['actual']
error_data.drop(columns='error', inplace=True)
error_data.rename(columns={'error_real': 'error'}, inplace=True)
error_data.loc[(error_data['actual'] == 0) & (error_data['origin_predict'] == 0), 'error'] = 0
error_data.loc[(error_data['actual'] == 0) & (error_data['origin_predict'] != 0), 'error'] = 1


# 去除预测数据中part_name不存在于训练集中的数据
for i in set(predict_data['part_name']):
    if i not in set(error_data['part_name']):
        predict_data = predict_data[predict_data['part_name'] != i]
predict_data.reset_index(inplace=True, drop=True)

# 根据实际销量数字量级分为10类
split_df = error_data.loc[:, ['part_name', 'actual']]
num_list = split_df.groupby('part_name')['actual'].mean()
num_split = pd.qcut(num_list, 10, labels=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
num_split_df = num_split.to_frame()
num_split_df.reset_index(inplace=True)
num_split_df.rename(columns={'actual': 'sold_num_type'}, inplace=True)
num_split_df['sold_num_type'] = pd.to_numeric(num_split_df['sold_num_type'])
part_data = pd.merge(part_data, num_split_df, on='part_name')

error_data_temp = error_data.drop('actual', axis=1)

all_data = pd.merge(error_data_temp, part_data, on='part_name', how='left')
predict_data10 = pd.merge(predict_data, part_data, on='part_name', how='left')

all_data['month'] = all_data.apply(lambda x: x.date.month, axis=1)
predict_data10['month'] = 10

drop_columns = [
                'date',
                'predict',
                'part_nm_chn',
                'is_new',
                'SC',
                'DC',
                # 'part_class_name',
                # 'part_type',
                # 'acc',
                # 'vehicle',
                # 'part_flow_abc',
                # 'part_price_abc',
                # 'supplier_type',
                # 'order_frequency',
                # 'delivery_frequency'
                ]
all_data.drop(drop_columns, axis=1, inplace=True)
predict_data10.drop(drop_columns, axis=1, inplace=True)

part_df = part_data.loc[:, ['part_name']]
part_dict = part_df.to_dict()['part_name']
part_df['part_no'] = part_df.index
part_dict_f = part_df.set_index(['part_name'])['part_no'].to_dict()

all_data['part_name'].replace(part_dict_f, inplace=True)
predict_data10['part_name'].replace(part_dict_f, inplace=True)

# 特征工程
# 独热编码
one_hot_feature = [
                   'part_class_name',
                   'part_type',
                   'acc',
                   'vehicle',
                   'part_flow_abc',
                   'part_price_abc',
                   'supplier_type',
                   'order_frequency',
                   'delivery_frequency'
                   ]

all_data_ready = deepcopy(all_data)
predict_data_ready = deepcopy(predict_data10)
for col in one_hot_feature:
    all_data_ready = all_data_ready.join(pd.get_dummies(all_data_ready[[col]]))
    predict_data_ready = predict_data_ready.join(pd.get_dummies(predict_data_ready[[col]]))

all_data_ready.drop(columns=one_hot_feature, inplace=True)
predict_data_ready.drop(columns=one_hot_feature + ['actual'], inplace=True)

month_list = [5, 6, 7, 8, 9]
month_get_list1 = list(combinations(month_list, 1))
month_get_list2 = list(combinations(month_list, 2))

feature_list = list(predict_data_ready.columns)
pred_dfs1 = pd.DataFrame()
err_all = 0
# for com in month_get_list2:
for com in month_get_list1:
    train_data = all_data_ready[~all_data_ready['month'].isin(com)].reset_index(drop=True)
    test_data = all_data_ready[all_data_ready['month'].isin(com)].reset_index(drop=True)

    train_x = train_data.loc[:, feature_list]
    train_y = train_data.loc[:, ['error']]
    test_x = test_data.loc[:, feature_list]
    test_y = test_data.loc[:, ['error']]

    dtrain = xgb.DMatrix(train_x, train_y)
    dtest = xgb.DMatrix(test_x, test_y)
    params = {
                'eta': 0.01,
                'max_depth': 3,
                'min_child_weight': 3,
                'gamma': 0.1,
                'subsample': .8,
                'colsample_bytree': .7,
                'reg_alpha': 1,
                # 'objective': 'reg:squarederror'
            }
    watchlist = [(dtrain, 'train'), (dtest, 'test')]
    xgb_model = xgb.train(params=params, dtrain=dtrain, num_boost_round=1000, early_stopping_rounds=100,
                          evals=watchlist)

    # fig, ax = plt.subplots(figsize=(18, 18))

    # xgb.plot_importance(xgb_model, ax=ax)
    # plt.show()

    test_pred_df = pd.concat([test_y, pd.DataFrame(xgb_model.predict(dtest), columns=['error_pred'])], axis=1)
    test_pred_df['err_err'] = np.abs(test_pred_df['error'] - test_pred_df['error_pred'])
    err_all += test_pred_df['err_err'].mean()
    # test_pred_df['error_q'] = 0
    # test_pred_df['error_pred_q'] = 0
    # test_pred_df.loc[test_pred_df['error'] >= 0, 'error_q'] = 1
    # test_pred_df.loc[test_pred_df['error_pred'] >= 0, 'error_pred_q'] = 1
    # test_pred_df['q_error'] = np.abs(test_pred_df['error_q'] - test_pred_df['error_pred_q'])
err_mean = float(err_all / 9)
print(err_mean)
