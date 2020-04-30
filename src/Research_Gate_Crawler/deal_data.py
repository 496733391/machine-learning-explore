#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import numpy as np

time_num = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
result = pd.read_excel('result.xlsx')
result['person_id'] = 0
for i in range(len(result)):
    result.loc[i, 'person_id'] = time_num + str(i)
    if type(result.loc[i, 'experience_list']) != np.nan:
        experience_list = result.loc[i, 'experience_list'].split(';')

print(result)
