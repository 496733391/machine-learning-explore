#! /usr/bin/python
# -*- coding: utf-8 -*-

# 数据库工具类
import math
from sqlalchemy import create_engine, types, orm, Table, MetaData
import pandas as pd


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
        self.metadata = None

        self.create_connect()

    def create_connect(self):
        db_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=UTF8MB4". \
            format(username=self.username, password=self.password, host=self.host, port=self.port, db=self.database)

        if not self.engine:
            self.engine = create_engine(db_url)
        if not self.conn:
            self.conn = self.engine.connect()

        self.metadata = MetaData(self.engine)

    def execute_sql(self, sql):
        self.conn.execute(sql)

    def single_value(self, sql):
        row = self.conn.execute(sql).fetchone()
        return row[0]

    def get_allresult(self, sql, data_type='list'):
        if data_type == 'list':
            result = self.conn.execute(sql).fetchall()
        elif data_type == 'dict':
            rows = self.conn.execute(sql).fetchall()
            result = [dict(zip(result.keys(), result)) for result in rows]
        else:
            result = pd.read_sql(sql=sql, con=self.conn)

        return result

    def insert_value(self, table_name, values):
        ins = Table(table_name, self.metadata, autoload=True)
        self.conn.execute(ins.insert(), values)

    def df_insert(self, table_name, df):
        datatype = {c: types.VARCHAR(df[c].str.len().max()) for c in df.columns[df.dtypes == 'object'].tolist()}

        df.to_sql(table_name, self.conn, index=False, if_exists='append', dtype=datatype)

    def close(self):
        self.conn.close()


class Connect:
    instance = None

    @classmethod
    def get_instance(cls, engine):
        if cls.instance:
            return cls.instance
        else:
            obj = cls(engine)
            cls.instance = obj
            return obj

    def __init__(self, engine):
        self.engine = engine
        self.session = None
        self.connect_session()

    def connect_session(self):
        try:
            self.engine.connect()
        except Exception as e:
            print(e)
            raise Exception("数据库连接失败")

        dbSession = orm.sessionmaker(bind=self.engine)
        self.session = dbSession()

    def add_all(self, records):
        '''
        指添加记录
        :param records:
        :return:
        '''

        if len(records) == 0:
            return

        post_count = 10000
        record_count = len(records)
        post = math.ceil(record_count / post_count)

        for i in range(post):
            begin_index = i * post_count
            if i + 2 <= post:
                end_index = (i + 1) * post_count
            else:
                end_index = record_count

            self.session.identity_map._dict = {}
            self.session.add_all(records[begin_index:end_index])
            self.save()

    def add(self, record):
        self.session.add(record)

    def save(self):
        try:
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()

    # 执行sql语句
    def execute_ext(self, sql):
        return self.session.execute(sql)

    # 返加是数据 []
    def execute(self, sql):
        try:
            return self.session.execute(sql).fetchall()
        except Exception:
            self.session.rollback()

    # 返回一条数据元组()
    def oneexecute(self, sql):
        try:
            return self.session.execute(sql).first()
        except Exception:
            self.session.rollback()

    def query(self, query):
        return self.session.query(query)

    def close(self):
        self.session.close()


if __name__ == '__main__':
    host = 'localhost'
    port = '3306'
    database = 'local'
    username = 'root'
    password = 'admin'

    dbUtil = DBUtil(host, port, database, username, password)
    print(dbUtil.engine)
    dbUtil.close()
