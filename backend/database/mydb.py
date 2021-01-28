#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import configparser
import mysql.connector
import logging
import os

logger = logging.getLogger('mylogger')

pool_dict = {}

class MyDB:
    """动作类，获取数据库连接，配置数据库IP，端口等信息，获取数据库连接"""

    def __init__(self, db='', db_name='', db_host='', port=3306, user='', password='', pool_name='',  pool_size = 0, charset='utf8'):
        try:
            if db:
                config = configparser.ConfigParser()
                # 从配置文件中读取数据库服务器IP、域名，端口
                head, tail = os.path.split(__file__)
                conf_filepath = os.path.normpath(os.path.join(head, '../conf/database.conf'))
                config.read(conf_filepath, encoding='utf-8')
                self.host = config[db]['host']
                self.port = config[db]['port']
                self.user = config[db]['user']
                self.passwd = config[db]['passwd']
                self.db_name = config[db]['db']
                self.charset = config[db]['charset']
            else:
                self.host = db_host
                self.port = port
                self.user = user
                self.passwd = password
                self.db_name = db_name
                self.charset = charset

            self.connect_config = {'host':self.host, 'port':self.port, 'user':self.user, 'password':self.passwd, 'database':self.db_name, 'charset':self.charset}

            result = self.__connect_database()
            if not result[0]:
                raise Exception(result[1])
            logger.debug('初始化数据库连接成功(数据库：%s)' % self.db_name)
        except Exception as e:
            msg = '初始化数据连接失败(数据库：%s)：%s' % (self.db_name, e)
            logger.error(msg)
            raise Exception(msg)

    def __connect_database(self):
        try:
            self.dbconn = mysql.connector.connect(**self.connect_config)
            return [True, '']
        except Exception as e:
            self.dbconn = None
            return [False,  '%s' % e]

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def execute_create(self,query):
        try:
            logger.info('create sql：%s' % query)

            try:
                db_cursor = self.dbconn.cursor()
            except Exception as e:
                msg = '获取数据库游标失败：%s，正在尝试重新连接数据库' % e
                logger.error(msg)
                result = self.__connect_database()
                if not result[0]:
                    msg = '尝试重连数据库(%s)失败：%s' % (result[1], self.db_name)
                    logger.error(msg)
                    return [False, msg]
                db_cursor = self.dbconn.cursor()

            db_cursor.execute(query)
            db_cursor.execute('commit')
            db_cursor.close()
            return True
        except Exception as e:
            logger.error('创建数据库表操作失败：%s' % e)
            db_cursor.execute('rollback')
            db_cursor.close()
            exit(1)

    def execute_insert(self, query, data):
        try:
            query = query.replace('"', "'")
            logger.info('insert sql：%s  data：%s' % (query, data))

            try:
                db_cursor = self.dbconn.cursor()
            except Exception as e:
                msg = '获取数据库游标失败：%s，正在尝试重新连接数据库' % e
                logger.error(msg)
                result = self.__connect_database()
                if not result[0]:
                    msg = '尝试重连数据库(%s)失败：%s' % (result[1], self.db_name)
                    logger.error(msg)
                    return [False, msg]
                db_cursor = self.dbconn.cursor()
            db_cursor.execute(query, data)
            record_id = db_cursor.lastrowid
            db_cursor.execute('commit')
            db_cursor.close()
            return [True, record_id]
        except Exception as e:
            logger.error('执行数据库插入操作失败：%s' % e)
            db_cursor.execute('rollback')
            db_cursor.close()
            return [False, '%s'% e]

    def execute_update(self, query, data):
        try:
            if data:
                query = query % data
            logger.info('update sql：%s' % query)
            try:
                db_cursor = self.dbconn.cursor()
            except Exception as e:
                msg = '获取数据库游标失败：%s，正在尝试重新连接数据库' % e
                logger.error(msg)
                result = self.__connect_database()
                if not result[0]:
                    msg = '尝试重连数据库(%s)失败：%s' % (result[1], self.db_name)
                    logger.error(msg)
                    return [False, msg]
                db_cursor = self.dbconn.cursor()
            db_cursor.execute(query)
            db_cursor.execute('commit')
            db_cursor.close()
            return [True, '']
        except Exception as e:
            logger.error('执行数据库更新操作失败：%s' % e)
            db_cursor.execute('rollback')
            db_cursor.close()
            return [False, '%s'% e]

    def execute_in_batch(self, query, data):
        try:
            if data:
                query = query % data
            logger.info('execute in batch sql：%s' % query)

            try:
                db_cursor = self.dbconn.cursor()
            except Exception as e:
                msg = '获取数据库游标失败：%s，正在尝试重新连接数据库' % e
                logger.error(msg)
                result = self.__connect_database()
                if not result[0]:
                    msg = '尝试重连数据库(%s)失败：%s' % (result[1], self.db_name)
                    logger.error(msg)
                    return [False, msg]
                db_cursor = self.dbconn.cursor()

            for result in db_cursor.execute(query, multi=True):
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(
                        result.statement))
                    result.fetchall()
                else:
                    pass
                    # print("Number of rows affected by statement '{}': {}".format(
                    #     result.statement, result.rowcount))
            db_cursor.execute('commit')
            db_cursor.close()
            return [True, '']
        except Exception as e:
            logger.error('批量执行数据库操作失败：%s' % e)
            db_cursor.execute('rollback')
            db_cursor.close()
            return [False, '%s'% e]

    def call_proc(self, query, data):
        '''调用存储过程'''

        try:
            if data:
                query = query % data
            logger.info('call proc sql：%s' % query)

            try:
                db_cursor = self.dbconn.cursor()
            except Exception as e:
                msg = '获取数据库游标失败：%s，正在尝试重新连接数据库' % e
                logger.error(msg)
                result = self.__connect_database()
                if not result[0]:
                    msg = '尝试重连数据库(%s)失败：%s' % (result[1], self.db_name)
                    logger.error(msg)
                    return [False, msg]
                db_cursor = self.dbconn.cursor()

            for result in db_cursor.execute(query, multi=True):
                if result.with_rows:
                    print("Rows produced by statement '{}':".format(
                        result.statement))
                    result.fetchall()
                else:
                    pass
                    # print("Number of rows affected by statement '{}': {}".format(
                    #     result.statement, result.rowcount))
            db_cursor.execute('commit')
            db_cursor.close()
            return [True, '']
        except Exception as e:
            logger.error('执行数据库存储过程失败：%s' % e)
            db_cursor.execute('rollback')
            db_cursor.close()
            return [False, '%s'% e]

    def select_one(self, query, data="", dictionary=False):
        '''返回结果只包含一条记录'''

        try:
            logger.info('select one sql：%s  data：%s' % (query, data))
            if data:
                query = query.replace('"', "'") % data
            logger.info('执行的查询语句为：%s' % query)

            try:
                db_cursor = self.dbconn.cursor(dictionary=dictionary)
            except Exception as e:
                msg = '获取数据库游标失败：%s，正在尝试重新连接数据库' % e
                logger.error(msg)
                result = self.__connect_database()
                if not result[0]:
                    msg = '尝试重连数据库(%s)失败：%s' % (result[1], self.db_name)
                    logger.error(msg)
                    return [False, msg]
                db_cursor = self.dbconn.cursor(dictionary=dictionary)
            db_cursor.execute(query)
            query_result = db_cursor.fetchall()
            if query_result:
                query_result = query_result[0]

            if not dictionary:
                temp_list = []
                for item in query_result:
                    if type(item) == type(bytearray(b'')): # 转换字节数组为字符串
                        item = item.decode('utf-8')
                    temp_list.append(item)
                query_result = temp_list
            self.dbconn.commit()
            db_cursor.close()
            return (True, query_result)
        except Exception as e:
            logger.error('执行数据库查询操作失败：%s' % e)
            db_cursor.close()
            return [False, '%s'% e]


    def select_many(self, query, data="", dictionary=False):
        '''返回结果包含多条记录'''
        try:
            logger.info('select many sql：%s  data：%s' % (query, data))
            try:
                db_cursor = self.dbconn.cursor(dictionary=dictionary)
            except Exception as e:
                msg = '获取数据库游标失败：%s，正在尝试重新连接数据库(%s)' % (e, self.db_name)
                logger.error(msg)
                result = self.__connect_database()
                if not result[0]:
                    msg = '尝试重连数据库(%s)失败：%s' % (result[1], self.db_name)
                    logger.error(msg)
                    return [False, msg]
                db_cursor = self.dbconn.cursor(dictionary=dictionary)
            if data:
                db_cursor.execute(query, data)
            else:
                db_cursor.execute(query)
            query_result = db_cursor.fetchall()
            if not dictionary:
                final_result = []
                for record  in query_result:
                    temp_result = []
                    for item in record:
                        if type(item) == type(bytearray(b'')): # 转换字节数组为字符串类型
                            item = item.decode('utf-8')
                        temp_result.append(item)
                    final_result.append(temp_result)
                query_result = final_result
            self.dbconn.commit()
            db_cursor.close()
            return [True,query_result]
        except Exception as e:
            logger.error('执行数据库查询操作失败：%s' % e)
            db_cursor.close()
            return [False, '%s'% e]

    def close(self):
        if self.dbconn:
            self.dbconn.close
            logger.info('数据库连接已关闭')
