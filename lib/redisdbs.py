#!/usr/bin/env python
# coding:utf-8

import logging
import time
import traceback
import redis
from config.__init__ import read_conf

logger = logging.getLogger(__name__)
redis_config = read_conf(conf_type='redis')


# ----------------------------------------------------------------------
def getRedisConn():
    """
    conn
    :param:
    :return:
    """
    return setRedisConn(redis_config["host"], redis_config["port"], redis_config["db"], redis_config["retry"])


def setRedisConn(host="127.0.0.1", port=6379, db=1, retry=3, timeout=10):
    """
    :链接redis
    @host:主机
    @port:端口
    @timeout:超时秒数
    @db:database
    @retry:重试次数
    """
    logger.info("-->begin:getRedisConn,host[%s],port[%d],database[%d],timeout[%d]" % (host, port, db, timeout))

    r = None
    i = 0

    while i < retry:
        try:
            pool = redis.ConnectionPool(host=host, port=port, db=db, decode_responses=True)
            r = redis.Redis(connection_pool=pool, decode_responses=True)
            if not r:
                logger.info("the [%d] times connect redis db failed，retry" % i)
            else:
                break
        except:
            logger.error(traceback.format_exc())
            time.sleep(1)
        i += 1
    return r


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisClient(object):

    def __init__(self, HOST=redis_config['host'], PORT=redis_config['port'], DB=redis_config['db']):
        self.pool = redis.ConnectionPool(host=HOST, port=PORT, db=DB, decode_responses=True)

    @property
    def conn(self):
        if not hasattr(self, '_conn'):
            self.getConnection()
        return self._conn

    def getConnection(self):
        self._conn = redis.Redis(connection_pool=self.pool)
