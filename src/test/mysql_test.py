#! /usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, types, Table, MetaData
import pandas as pd


host = 'localhost'
port = '3306'
database = 'local'
username = 'root'
password = 'admin'

db_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=UTF8MB4".\
    format(username=username, password=password, host=host, port=port, db=database)

engine = create_engine(db_url)

conn = engine.connect()
dd = conn.begin()
result = conn.execute("select * from con_test")

metadata = MetaData(engine)
ins = Table('con_test', metadata, autoload=True)
print(ins.insert())
conn.execute(ins.insert(), [{'test1': 1, 'test2': 1}, {'test1': 1, 'test2': 1}])

print(result.fetchone(), '\n', result.fetchall())
print(conn.execute('select test1 from con_test limit 1 ').fetchone())
conn.execute('update con_test set test1="2"')

df = pd.read_sql('select * from con_test', conn)

datatype = {c: types.VARCHAR(df[c].str.len().max()) for c in df.columns[df.dtypes == 'object'].tolist()}

df.to_sql('con_test', conn, index=False, if_exists='append', dtype=datatype)

conn.close()
