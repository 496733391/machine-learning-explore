#! /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd

from src.config.DBUtil import DBUtil
from src.Scopus_Crawler.scopus_config import host, port, database, username, password


dbutil = DBUtil(host, port, database, username, password)
