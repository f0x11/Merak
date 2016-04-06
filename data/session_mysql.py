#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
import random
import socket
from sqlalchemy import create_engine, MetaData, Column, DateTime
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import etc

machine_name = socket.gethostname()
machine_no = etc.machine_no_dict[machine_name]
def id_generator():
    """
    snowflake算法 64位
    1: 41: 12: 10x
    1 位保留
    41位是ms时间戳
    12位是机器号
    10位是序号
    :return:
    """
    t = time.time()
    m = machine_no
    i = random.randint(0, 1024)
    l = (int(t * 1000) << 22) | (m << 12) | i
    return l

# session
engine = create_engine(
    'mysql://' + etc.mysql_user + ':' + etc.mysql_passwd + '@' + etc.mysql_host + ':' + str(
        etc.mysql_port) + '/' + etc.mysql_dbname + '?charset=utf8mb4',
    encoding="utf-8", pool_size=100, pool_recycle=3600,
    echo=False)

Session = sessionmaker()
Session.configure(bind=engine)


class SessionCM(object):
    def __enter__(self):
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is not None:
            self.session.rollback()
        self.session.close()

base_metadata = MetaData()


# BaseTable
class _Base(object):
    id = Column('id', BIGINT(unsigned=True),
                primary_key=True, default=id_generator)
    created_time = Column("created_time", DateTime, default=datetime.now())

DeclarativeBase = declarative_base(metadata=base_metadata, cls=_Base)


if __name__ == '__main__':
    pass
