#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd

data_all = pd.read_table('savedrecs.txt', sep='\t{1}', usecols=['TI', 'DI'], engine='python')

data_all.to_excel('webofs.xlsx', index=False)
