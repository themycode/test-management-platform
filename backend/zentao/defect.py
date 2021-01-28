#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
@CreateTime: 2020/09/15 17:10
@Author : shouke
'''
import logging
from backend.database.mydb import MyDB
from backend.conf.config import ZENTAO_DEFECT_CUSTOM_FIELDS
from backend.conf.config import ZENTAO_DEFECT_CUSTOM_FIELD_MAP

logger = logging.getLogger('mylogger')

class ZentaoDefect:
    @staticmethod
    def get_all_custom_fields():
        '''获取禅道缺陷自定义字段'''

        try:
            data = [{'id':field, 'name': field} for field in ZENTAO_DEFECT_CUSTOM_FIELDS]
            return data
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def get_defects_by_project_version_ids(zentao_project_version_ids_dict, version_selected):
        '''根据项目及项目版本获取缺陷'''

        try:
            dbclient = None
            dbclient = MyDB('ZENTAODB')
            query_condition = ''

            if zentao_project_version_ids_dict['versions'] and zentao_project_version_ids_dict['projects']:
                if not version_selected: # 如果前端没有手动选取项目版本，则统计缺陷时需要统计影响版本为trunk的
                    zentao_project_version_ids_dict['versions'].append("'trunk'")

                temp = ''
                for item in zentao_project_version_ids_dict['versions']:
                    temp += 'FIND_IN_SET(%s, bug.openedBuild) OR ' %  item

                if temp:
                    query_condition += ' AND (%s)' % temp.strip().rstrip('OR')
            else:
                return []

            pj_join_extra_condition = ','.join(zentao_project_version_ids_dict['projects'])
            pj_join_extra_condition = ' AND pj.id IN (%s)' % pj_join_extra_condition

            query_fields = ''
            for key in ZENTAO_DEFECT_CUSTOM_FIELD_MAP:
                query_fields += ', bug.%s' % ZENTAO_DEFECT_CUSTOM_FIELD_MAP[key]
            # 禅道版本 9.2.1 Bug解决方案 按默认配置
            query_sql = "SELECT bug.id, " \
                        "bug.title, " \
                        "CASE WHEN (bug.status='active' AND bug.confirmed=0) THEN '新建' " \
                        "WHEN (bug.status='resolved' AND bug.resolution='fixed') THEN '已解决' " \
                        "WHEN (bug.status='active' AND bug.confirmed=1 AND bug.activatedCount=0) THEN '已受理' " \
                        "WHEN (bug.status='resolved' AND bug.resolution='postponed') THEN '延期处理' " \
                        "WHEN (bug.status='resolved' AND bug.resolution NOT IN ('postponed', 'fixed')) THEN '已拒绝' " \
                        "WHEN (bug.status='active' AND bug.activatedCount>0) THEN '重新打开' " \
                        "WHEN (bug.status='closed') THEN '已关闭' ELSE bug.status END AS status, " \
                        "bug.pri AS priority, " \
                        "bug.severity, " \
                        "bug.openedBy AS createrAccount, " \
                        "IFNULL((SELECT realname FROM zt_user WHERE zt_user.account = bug.openedBy), '') AS creater, " \
                        "DATE_FORMAT(bug.openedDate, '%%Y-%%m-%%d %%H:%%I:%%S') AS createdDate, " \
                        "bug.assignedTo AS assignedToAccount, " \
                        "IFNULL((SELECT realname FROM zt_user WHERE zt_user.account = bug.assignedTo), '') AS assignedTo, " \
                        "DATE_FORMAT(bug.assignedDate, '%%Y-%%m-%%d %%H:%%I:%%S') AS assignedDate, " \
                        "bug.resolvedBy AS resolvedByAccount, " \
                        "IFNULL((SELECT realname FROM zt_user WHERE zt_user.account = bug.resolvedBy), '') AS resolver, " \
                        "CASE bug.resolution WHEN 'fixed' THEN '已解决' WHEN 'postoned' THEN '延期处理' WHEN 'willnotfix' THEN '不予解决' WHEN 'notrepro' THEN '无法重现' " \
                        "WHEN 'external' THEN '外部原因' WHEN 'bydesign' THEN '设计如此' WHEN 'duplicate' THEN '重复Bug' WHEN 'toStory' THEN '转需求' ELSE bug.resolution END AS resolution, " \
                        "DATE_FORMAT(bug.resolvedDate, '%%Y-%%m-%%d %%H:%%I:%%S') AS resolvedDate, " \
                        "bug.closedBy AS closedByID, " \
                        "IFNULL((SELECT realname FROM zt_user WHERE zt_user.account = bug.closedBy), '') AS closedBy, " \
                        "DATE_FORMAT(bug.closedDate, '%%Y-%%m-%%d %%H:%%I:%%S') AS closedDate, " \
                        "bug.type, " \
                        "bug.confirmed, " \
                        "bug.activatedCount, " \
                        "bug.duplicateBug, " \
                        "bug.project AS projectID, " \
                        "pj.name AS projectName, " \
                        "bug.openedBuild AS 'versionIDsAffected', " \
                        "bug.product AS productID, " \
                        "pd.name AS productName %s " \
                        "FROM zt_bug AS bug " \
                        "JOIN zt_project AS pj ON bug.project = pj.id %s " \
                        "JOIN zt_product AS pd ON bug.product = pd.id " \
                        "WHERE bug.deleted = '0' %s " % (query_fields, pj_join_extra_condition, query_condition)
                        # "ORDER BY bug.severity DESC ;"  % (query_fields, query_condition)
            query_result = dbclient.select_many(query_sql, "", dictionary=True)
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
