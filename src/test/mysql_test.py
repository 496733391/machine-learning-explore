#! /usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd


host = 'localhost'
port = '3306'
database = 'local_test'
username = 'root'
password = 'pass1234'

db_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=UTF8MB4".\
    format(username=username, password=password, host=host, port=port, db=database)

engine = create_engine(db_url)

conn = engine.connect()
result = conn.execute("select * from con_test")
print(result.fetchone())

df = pd.read_sql('select * from con_test', engine)
df.to_sql('con_test', engine, index=False, if_exists='append')
