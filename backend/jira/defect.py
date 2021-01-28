#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
@CreateTime: 2020/08/10 14:43
@Author : shouke
'''


import logging
from backend.conf.config import JIRA_ISSUE_TYPE_NAME
from backend.database.mydb import MyDB

logger = logging.getLogger('mylogger')

class JiraDefect:

    @staticmethod
    def get_defects_by_version_ids(version_id_list, issue_type_id):
        '''根据项目版本获取缺陷'''

        try:
            dbclient = None
            dbclient = MyDB('JIRA')
            version_filter = ''
            if version_id_list:
                version_filter =  'AND nodeassociation.SINK_NODE_ID in (%s)'  % ','.join(version_id_list)

            if issue_type_id:
                issue_type_filter = ' AND issuetype.ID=%s ' % issue_type_id
            else:
                issue_type_filter = " AND issuetype.pname = '%s' " %  JIRA_ISSUE_TYPE_NAME

            query_sql = "SELECT jiraissue.ID AS id," \
                        "jiraissue.issuenum AS issuenum, " \
                        "jiraissue.SUMMARY AS title, " \
                        "IFNULL(issuestatus.pname, '新建') AS 'status', " \
                        "jiraissue.PRIORITY AS priority, " \
                        "user_creater.display_name AS creater, "\
                        "user_creater.lower_user_name AS createrAccount, "\
                        "DATE_FORMAT(jiraissue.created, '%%Y-%%m-%%d %%H:%%I:%%S') AS createdDate, " \
                        "user_assignee.display_name AS assignedTo, "\
                        "user_assignee.lower_user_name AS assignedToAccount," \
                        "IFNULL(resolution.pname, '待处理') AS resolution, " \
                        "DATE_FORMAT(jiraissue.RESOLUTIONDATE, '%%Y-%%m-%%d %%H:%%I:%%S') AS resolvedDate, " \
                        "jiraissue.PROJECT AS projectID, " \
                        "project.pname AS projectName, " \
                        "IFNULL(GROUP_CONCAT(nodeassociation.SINK_NODE_ID), '') AS 'versionIDsAffected', " \
                        "jiraissue.TIMESPENT AS timespent, " \
                        "issuetype.pname AS issuetypeName " \
                        "FROM jiraissue " \
                        "JOIN issuetype ON issuetype.ID = jiraissue.issuetype %s" \
                        "JOIN issuestatus ON issuestatus.ID = jiraissue.issuestatus " \
                        "JOIN project ON project.ID = jiraissue.PROJECT " \
                        "JOIN nodeassociation ON nodeassociation.SOURCE_NODE_ID = jiraissue.ID AND nodeassociation.ASSOCIATION_TYPE='IssueVersion' %s " \
                        "JOIN app_user AS creater ON creater.user_key = jiraissue.CREATOR " \
                        "JOIN app_user AS assignee ON assignee.user_key = jiraissue.ASSIGNEE " \
                        "JOIN cwd_user AS user_creater ON user_creater.lower_user_name = creater.lower_user_name " \
                        "JOIN cwd_user AS user_assignee ON user_assignee.lower_user_name = assignee.lower_user_name " \
                        "LEFT JOIN resolution ON resolution.ID = jiraissue.RESOLUTION " \
                        "GROUP BY jiraissue.ID;" % (issue_type_filter, version_filter)
            query_result = dbclient.select_many(query_sql, "", dictionary=True)
            logger.info(query_sql)
            if query_result[0]:
                 defects = query_result[1]
            else:
                 raise Exception('查询禅道项目缺陷失败：%s' % query_result[1] )
            return defects
        except Exception as e:
            raise Exception(e)
        finally:
            if dbclient:
                dbclient.close()

    @staticmethod
    def get_defect_custom_field_info(defect_id):
        ''' 根据缺陷id获取缺陷自定义字段信息 '''

        try:
            dbclient = None
            dbclient = MyDB('JIRA')

            query_sql = "SELECT DISTINCT customfieldvalue.ISSUE, customfield.ID AS custom_field, " \
                        "IF(" \
                        "customfieldvalue.STRINGVALUE IS NOT NULL, " \
                        "IF(LOCATE('JIRAUSER', customfieldvalue.STRINGVALUE), IFNULL(concat(cwd_user.display_name, '__', cwd_user.lower_user_name), ''), IFNULL(GROUP_CONCAT(customfieldoption.customvalue ORDER BY STRINGVALUE ASC), customfieldvalue.STRINGVALUE)), " \
                        "IFNULL(customfieldvalue.NUMBERVALUE, customfieldvalue.TEXTVALUE)) AS cfvalue, " \
                        "customfield.cfname " \
                        "FROM customfieldvalue " \
                        "JOIN customfield  ON customfieldvalue.CUSTOMFIELD = customfield.ID " \
                        "LEFT JOIN customfieldoption ON customfieldvalue.STRINGVALUE = customfieldoption.ID " \
                        "LEFT JOIN app_user ON customfieldvalue.STRINGVALUE = app_user.user_key " \
                        "LEFT JOIN cwd_user ON app_user.lower_user_name = cwd_user.lower_user_name " \
                        "WHERE ISSUE = %s " \
                        "GROUP BY customfield.ID;" % defect_id
            query_result = dbclient.select_many(query_sql, "", dictionary=True)
            logger.info(query_sql)
            if query_result[0]:
                 rows = query_result[1]
            else:
                 raise Exception('查询jira项目缺陷失败：%s' % query_result[1] )
            return rows
        except Exception as e:
            raise Exception(e)
        finally:
            if dbclient:
                dbclient.close()

