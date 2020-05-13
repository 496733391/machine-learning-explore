#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

base_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
sys.path.insert(0, base_dir)

from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password


def write2sql(rows):
    '''

    :param rows: [[表名， df名称], [...]]
    :return:
    '''
    dbutil = DBUtil(host, port, database, username, password)
    for row in rows:
        dbutil.df_insert(row[0], row[1])

    dbutil.close()


def write2text(row):
    if len(row) > 0:
        with open('not_found.txt', 'a', encoding='utf-8') as f:
            f.writelines(row)
