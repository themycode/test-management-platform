#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
@CreateTime: 2020/08/04 15:10
@Author : shouke
'''


import logging
from backend.database.mydb import MyDB

logger = logging.getLogger('mylogger')

class ZentaoProject():

    @staticmethod
    def get_all_projects():
        '''获取所有满足条件的项目'''

        try:
            dbclient = None
            dbclient = MyDB('ZENTAODB')
            query_sql = "SELECT cast(id AS CHAR ) AS 'id', name AS 'name' " \
                        "FROM zt_project ORDER BY `order` DESC ;"
            query_result = dbclient.select_many(query_sql, "", dictionary=True)
            if query_result[0]:
                all_projects = query_result[1]
            else:
                raise Exception('查询禅道项目失败：%s' % query_result[1] )
            return all_projects
        except Exception as e:
            raise Exception(e)
        finally:
            if dbclient:
                dbclient.close()

    @staticmethod
    def get_project_versions_by_project(project_id):
        '''根据项目id获取项目版本'''

        try:
            dbclient = None
            dbclient = MyDB('ZENTAODB')

            query_sql = "SELECT cast(id AS CHAR ) AS 'id', name,  'zentao' AS 'platform' " \
                        "FROM zt_build WHERE project = %s AND deleted='0' ORDER BY id DESC;" % project_id

            query_result = dbclient.select_many(query_sql, "", dictionary=True)
            if query_result[0]:
                all_project_versions = query_result[1]
            else:
                raise Exception('根据项目id查询禅道项目版本失败：%s' % query_result[1] )
            return all_project_versions
        except Exception as e:
            raise Exception(e)
        finally:
            if dbclient:
                dbclient.close()