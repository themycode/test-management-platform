#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
@CreateTime: 2020/09/15 17:10
@Author : shouke
'''
import logging
from backend.database.mydb import MyDB

logger = logging.getLogger('mylogger')

class ZentaoUser:
    @staticmethod
    def get_all_users():
        '''根据项目及项目版本获取缺陷'''

        try:
            dbclient = None
            dbclient = MyDB('ZENTAODB')
            query_sql = "SELECT id, account, realname FROM zt_user WHERE deleted = '0'"
            query_result = dbclient.select_many(query_sql, "", dictionary=True)
            if query_result[0]:
                 users = query_result[1]
            else:
                 raise Exception('查询禅道用户失败失败：%s' % query_result[1] )
            return users
        except Exception as e:
            raise Exception(e)
        finally:
            if dbclient:
                dbclient.close()
