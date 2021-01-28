#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
@CreateTime: 2020/08/04 9:38
@Author : shouke
'''

import logging
from backend.database.mydb import MyDB

logger = logging.getLogger('mylogger')

class JiraProject():

    @staticmethod
    def get_all_projects():
        '''获取所有满足条件的项目'''

        try:
            jira_dbclient = None
            jira_dbclient = MyDB('JIRA')

            # query_sql = "SELECT cast(ID AS CHAR ) AS 'id', pname AS 'name' " \
            #             "FROM project;"
            query_sql = "SELECT cast(ID AS CHAR ) AS 'id', pname AS 'name' " \
                        "FROM project WHERE PROJECTTYPE = 'software' ORDER BY ID DESC;"

            query_result = jira_dbclient.select_many(query_sql, "", dictionary=True)
            if query_result[0]:
                all_projects = query_result[1]
            else:
                raise Exception('查询jira项目失败：%s' % query_result[1] )
            return all_projects
        except Exception as e:
            raise Exception(e)
        finally:
            if jira_dbclient:
                jira_dbclient.close()


    @staticmethod
    def get_project_versions_by_project(project_id):
        '''根据项目id获取项目版本'''

        try:
            jira_dbclient = None
            jira_dbclient = MyDB('JIRA')

            query_sql = "SELECT cast(ID AS CHAR ) AS 'id', vname AS 'name', 'jira' AS 'platform'" \
                        "FROM projectversion WHERE PROJECT = %s ORDER BY SEQUENCE DESC;" % project_id

            query_result = jira_dbclient.select_many(query_sql, "", dictionary=True)
            if query_result[0]:
                all_project_versions = query_result[1]
            else:
                raise Exception('根据项目id查询jira项目版本失败：%s' % query_result[1] )
            return all_project_versions
        except Exception as e:
            raise Exception(e)
        finally:
            if jira_dbclient:
                jira_dbclient.close()