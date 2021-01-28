#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
@CreateTime: 2020/08/14 1:20
@Author : shouke
'''

import logging
from backend.database.mydb import MyDB

logger = logging.getLogger('mylogger')

class JiraIssue():

    @staticmethod
    def get_all_issue_types():
        '''获取所有满足条件的问题类型'''

        try:
            jira_dbclient = None
            jira_dbclient = MyDB('JIRA')
            query_sql = "SELECT cast(ID AS CHAR ) AS 'id', pname AS 'name' " \
                    "FROM issuetype ORDER BY ID DESC;"
            query_result = jira_dbclient.select_many(query_sql, "", dictionary=True)
            if query_result[0]:
                all_issue_types = query_result[1]
            else:
                raise Exception('查询jira项目失败：%s' % query_result[1] )
            return all_issue_types
        except Exception as e:
            raise Exception(e)
        finally:
            if jira_dbclient:
                jira_dbclient.close()


    @staticmethod
    def get_all_custom_fields():
        '''获取jira问题自定义字段'''

        try:
            jira_dbclient = None
            jira_dbclient = MyDB('JIRA')

            query_sql = "SELECT cast(ID AS CHAR ) AS 'id', cfname AS 'name' " \
                        "FROM customfield ORDER BY ID DESC;"
            query_result = jira_dbclient.select_many(query_sql, "", dictionary=True)
            if query_result[0]:
                all_custom_fields = query_result[1]
            else:
                raise Exception('查询jira项目失败：%s' % query_result[1] )
            return all_custom_fields
        except Exception as e:
            raise Exception(e)
        finally:
            if jira_dbclient:
                jira_dbclient.close()