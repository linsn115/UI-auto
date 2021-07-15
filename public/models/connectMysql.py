from public.page_obj.base import con

import pandas as pd
from sqlalchemy import create_engine

# 初始化数据库连接
# 按实际情况依次填写MySQL的用户名、密码、IP地址、端口、数据库名
user = con.get("Mysql", "USER")
password = con.get("Mysql", "PASSWORD")
ip = con.get("Mysql", "IP")
port = con.get("Mysql", "PORT")
db_name = con.get("Mysql", "DB_NAME")
engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, ip, port, db_name))


def get_sql_query(sql):
    """
    返回sql查询结果
    :param sql:
    :return:
    """
    return pd.read_sql(sql, engine)


def select_sql_by_parameter(column1, table, column2, value):
    """
    单表查询：根据一个字段查询
    :param column1:字段1
    :param table:表
    :param column2:字段2
    :param value:字段值
    :return: 返回查询结果
    """
    return pd.read_sql("SELECT {} FROM {} WHERE {} = '{}'".format(column1, table, column2, value), engine)
