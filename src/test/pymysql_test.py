#! /usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import pandas as pd
from sqlalchemy import types, create_engine

host = 'localhost'
port = 3306
database = 'local'
username = 'root'
password = 'admin'

db_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=UTF8MB4".\
    format(username=username, password=password, host=host, port=port, db=database)

engine = create_engine(db_url)

conn = pymysql.connect(
    host=host,
    port=port,
    user=username,
    password=password,
    database=database,
    charset='utf8'
)

cursor = conn.cursor()

cursor.execute("select * from con_test")
result = cursor.fetchall()
print(result)

df = pd.read_sql('select * from con_test', conn)

datatype = {c: types.VARCHAR(df[c].str.len().max()) for c in df.columns[df.dtypes == 'object'].tolist()}

df.to_sql('con_test', engine, index=False, if_exists='append', dtype=datatype)

conn.close()
