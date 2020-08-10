#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import re
import time
import js2py

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from src.Scopus_Crawler.scopus_config import headers

js_str = requests.get(url='http://www.gx211.com/collegemanage/class.js', headers=headers, timeout=30)

context = js2py.EvalJs()
context.execute(js_str.text)
maxclass = eval('{}'.format(context.maxclass))
minclass = eval('{}'.format(context.minclass))

maxclass_df = pd.DataFrame(data=maxclass, columns=['专业大类', '专业大类名称'])
minclass_df = pd.DataFrame(data=minclass, columns=['tid', '专业小类', '专业小类名称'])

maxclass_df['专业大类'] = pd.to_numeric(maxclass_df['专业大类'])
minclass_df['专业小类'] = pd.to_numeric(minclass_df['专业小类'])
subject_df = pd.read_excel('C:/Users/Administrator/Desktop/0716subject.xlsx')
subject_df = pd.merge(subject_df, maxclass_df, on='专业大类', how='left')
subject_df = pd.merge(subject_df, minclass_df, on='专业小类', how='left')

school_df = pd.read_excel('C:/Users/Administrator/Desktop/0716school.xlsx')

subject_df = pd.merge(subject_df, school_df, on='id', how='left')
subject_df.to_excel('C:/Users/Administrator/Desktop/0716all.xlsx', index=False)
