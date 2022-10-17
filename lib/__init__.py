#!/usr/bin/env python
# coding:utf-8

from config.__init__ import read_conf
from peewee import OperationalError, MySQLDatabase
from peewee import __exception_wrapper__
from .mysql import ReConnectMysqlDatabase


class RetryOperationalError(object):
    def execute_sql(self, sql, params=None, commit=True):
        try:
            cursor = super(RetryOperationalError, self).execute_sql(
                sql, params, commit)
        except OperationalError:
            if not self.is_closed():
                self.close()
            with __exception_wrapper__:
                cursor = self.cursor()
                cursor.execute(sql, params or ())
                if commit and not self.in_transaction():
                    self.commit()
        return cursor


class RetryMySQLDatabase(RetryOperationalError, MySQLDatabase):
    pass

database = 'biddata'
_mdb = RetryMySQLDatabase(database=database, **read_conf(conf_type='mysql')[database])

#
# _mdb=ReConnectMysqlDatabase(database, **mysql_config["user_r"])


#
# from peewee import SqliteDatabase
# _mdb = SqliteDatabase("changshangtong.db")
