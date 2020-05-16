#! /usr/bin/python
# -*- coding: utf-8 -*-

# 数据库工具类
from sqlalchemy import create_engine, types
import pandas as pd
import pymysql
from DBUtils.PooledDB import PooledDB


class DBUtil:
    def __init__(self, host, port, database, username, password):
        '''

        :param host: 地址
        :param port: 端口
        :param database: 库名
        :param username: 用户名
        :param password: 密码
        '''

        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.engine = None
        self.conn = None
        self.cursor = None

        self.create_connect()

    def create_connect(self):

        db_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=UTF8MB4". \
            format(username=self.username, password=self.password, host=self.host, port=self.port, db=self.database)

        if not self.engine:
            self.engine = create_engine(db_url)

        if not self.conn:
            self.conn = pymysql.connect(
                        host=self.host,
                        port=self.port,
                        user=self.username,
                        password=self.password,
                        database=self.database,
                        charset='utf8'
                    )

    def create_cursor(self):
        self.cursor = self.conn.cursor()

    def execute_sql(self, sql):
        if not self.cursor:
            self.create_cursor()

        self.cursor.execute(sql)

    def single_value(self, sql):
        self.execute_sql(sql)
        row = self.cursor.fetchone()
        return None if not row else row[0]

    def get_allresult(self, sql, data_type='list'):

        if data_type == 'list':
            self.execute_sql(sql)
            result = self.cursor.fetchall()
        elif data_type == 'dict':
            self.execute_sql(sql)
            rows = self.cursor.fetchall()
            result = [dict(zip(result.keys(), result)) for result in rows]
        else:
            result = pd.read_sql(sql=sql, con=self.conn)

        return result

    def insert_value(self, sql, values):
        if not self.cursor:
            self.create_cursor()
        self.cursor.executemany(sql, values)

    def execute_commit(self):
        self.conn.commit()

    def df_insert(self, table_name, df):
        '''

        :param table_name: 表名称，str
        :param df: 要写入的数据，Dataframe
        :return:
        '''
        if len(df) > 0:
            datatype = {c: types.VARCHAR(df[c].str.len().max()) for c in df.columns[df.dtypes == 'object'].tolist()}
            df.to_sql(table_name, self.engine, index=False, if_exists='append', dtype=datatype)

    def close(self):
        if self.cursor:
            self.cursor.close()
        self.conn.close()
        self.engine.dispose()


if __name__ == '__main__':
    host = 'localhost'
    port = 3306
    database = 'local'
    username = 'root'
    password = 'admin'

    dbUtil = DBUtil(host, port, database, username, password)
    dbUtil.create_cursor()
    print(dbUtil.engine)
    dbUtil.close()
