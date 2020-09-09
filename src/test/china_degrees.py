#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import re

from src.Scopus_Crawler.scopus_config import headers

url1 = 'http://www.chinadegrees.cn/webrms/Services/xkpm.jsp?xkdm='

key_list = ['01,02,03,04,05,06', '07', '08', '09', '10', '12']

for key in key_list:
    url = url1 + key
    page = requests.get('http://www.chinadegrees.cn/', headers=headers)
    print(1)


