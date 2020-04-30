#! /usr/bin/python
# -*- coding: utf-8 -*-

# 数据库工具类

from sqlalchemy import create_engine


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
        self.create_cursor()

    def create_connect(self):
        db_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=UTF8MB4". \
            format(username=self.username, password=self.password, host=self.host, port=self.port, db=self.database)

        if not self.engine:
            self.engine = create_engine(db_url)
        if not self.conn:
            self.conn = self.engine.raw_connection()

    def create_cursor(self):
        if not self.cursor:
            self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    host = 'localhost'
    port = '3306'
    database = 'local'
    username = 'root'
    password = 'admin'

    dbUtil = DBUtil(host, port, database, username, password)
    print(dbUtil.engine)
    dbUtil.close()
    print(1)
