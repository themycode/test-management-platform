#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import json
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backend.models import Project
from backend.models import ProjectAssociated
from backend.models import ProjectVersion
from backend.serializers import ProjectSerializer

from backend.jira.project import JiraProject
from backend.jira.issue import JiraIssue

from backend.zentao.project import ZentaoProject
from backend.zentao.defect import ZentaoDefect


from backend.conf.config import SYS_CUSTOM_FIELDS

logger = logging.getLogger('mylogger')

class ProjectListAPIView(APIView):
    '''
    项目视图-项目管理-项目列表
    '''

    # 查询列表数据
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            page_size = int(params.get('pageSize'))
            page_no = int(params.get('pageNo'))
            name = params.get('name')
            project_status = params.get('status')
            sort = params.get('sort')

            order_by = 'id desc'
            if sort:
                order_by = sort
            #     sort_list = sort.split(',')
            # else:
            #     sort_list = ['-id']

            startIndex = (page_no - 1) * page_size
            # endIndex = startIndex + page_size

            # filters = {'is_delete':0}
            where = ['tb_project.is_delete = 0']
            if name:
                # filters['name__startswith'] = name
                where.append('locate("%s", name) ' % name)

            if project_status:
                # filters['status'] = project_status
                where.append("status='%s'" % project_status)

            where = ' AND '.join(where)
            where = 'WHERE ' + where
            sql = 'SELECT tb_project.id, COUNT(1) AS count FROM tb_project LEFT JOIN tb_project_associated ON tb_project.id=tb_project_associated.project_id ' \
                  '%s ' % where
            query_rows = Project.objects.raw(sql)
            total = query_rows[0].__dict__.get('count') if query_rows else 0

            sql =  "SELECT tb_project.id, name, status, begin_time, end_time, product_id, `desc`, tb_project.creater_id, tb_project.creater_name, " \
                   "DATE_FORMAT(tb_project.create_time, '%%Y-%%m-%%d %%H:%%I:%%S') AS create_time, " \
                   "tb_project.updater_id, tb_project.updater_name, DATE_FORMAT(tb_project.update_time, '%%Y-%%m-%%d %%H:%%I:%%S') AS update_time, "\
                   "IFNULL(platform_project_name, '') AS platform_project_name, IFNULL(platform_project_id, '') AS platform_project_id, IFNULL(platform, '') AS platform, " \
                   "IFNULL(defect_issue_type_id, '') AS defect_issue_type_id, IFNULL(defect_status_map, '') AS defect_status_map, IFNULL(defect_severity_map, '') AS defect_severity_map, " \
                   "IF(ISNULL(custom_field_map) OR custom_field_map='', '{}', custom_field_map) AS custom_field_map " \
                   "FROM tb_project LEFT JOIN tb_project_associated ON tb_project.id=tb_project_associated.project_id "
            sql +=  "%s ORDER BY %s LIMIT %s,%s " % (where, order_by, startIndex, page_size) # 上述sql包含 {} 占位符，所以采用sql +=的方式
            query_rows = Project.objects.raw(sql)
            rows = []
            for item in query_rows:
                item.__dict__.pop('_state')
                rows.append(item.__dict__)

            # rows = projects.order_by(*sort_list)[startIndex:endIndex]
            # rows = ProjectSerializer(rows, many=True).data
            # total = Project.objects.filter(**filters).count()

            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = {}
            result['data']['rows'] = rows
            result['data']['total'] = total
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 批量删除列表数据
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            row_ids = data.get('row_ids')
            if ProjectVersion.objects.filter(project_id__in=row_ids,is_delete=0).exists():
                result['msg'] =  '删除失败，请先删除关联的项目版本'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            Project.objects.filter(id__in=row_ids).update(is_delete=1)
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectsDetailsAPIView(APIView):
    '''
    按指定字段批量获取项目详细信息
    '''

    # 查询详情
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            fields = params.get('fields')
            sort = params.get('sort')
            exclusive_filters = params.get('exclusion')
            if fields:
                fields = fields.split(',')
            else:
                fields = ['id', 'name']
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            filters = {'is_delete':0}
            if exclusive_filters:
                exclusive_filters = json.loads(exclusive_filters)
                rows = Project.objects.filter(**filters).exclude(**exclusive_filters).order_by(*sort_list).values(*fields)
            else:
                rows = Project.objects.filter(**filters).order_by(*sort_list).values(*fields)
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = rows
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectAPIView(APIView):
    '''
    项目视图-项目管理，新增，修改，删除项目
    '''

    # 新增项目
    def post(self, request, format=None):
        result = {}

        try:
            data = request.data
            project_name = data.get('name')
            data['creater_id'] = request.user.id
            data['updater_id'] = data['creater_id']
            data['creater_name'] = request.user.name
            data['updater_name'] = data['creater_name']
            data['is_delete'] = False

            if Project.objects.filter(name=project_name, is_delete=0).exists():
                result['msg'] =  '新增失败，项目已存在'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            try:
                serializer = ProjectSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except Exception as e:
                result['msg'] =  '新增失败：%s' % e
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

            result['msg'] =  '新增成功'
            result['success'] =  True
            result['data'] =  serializer.data
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 修改项目
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['updater_id'] = request.user.id
            data['updater_name'] = request.user.name
            project_name = data.get('name')
            project_id = data.get('id')
            data.pop('id')

            if Project.objects.exclude(id=project_id).filter(name=project_name, is_delete=0).exists():
                result['msg'] =  '修改失败，项目名称已存在'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            if ProjectVersion.objects.filter(project_id=project_id, is_delete=0).exists():
                result['msg'] =  '该项目已存在关联项目版本，不允许修改'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            obj = Project.objects.filter(id=project_id).first()

            if obj:
                try:
                    serializer = ProjectSerializer(obj, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                except Exception as e:
                    result['msg'] =  '操作失败：%s!' % e
                    result['success'] =  False
                    return Response(result, status.HTTP_400_BAD_REQUEST)
            else:
                result['msg'] = '操作失败,项目不存在'
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result['msg'] =  '操作成功'
            result['success'] =  True
            temp_data = {}
            data_keys = list(data.keys())
            data_keys.append('update_time')
            for key in data_keys:
                temp_data[key] = serializer.data.get(key)
            result['data'] =  temp_data
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 删除项目
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            project_id = data.get('id')

            if ProjectVersion.objects.filter(project_id=project_id,is_delete=0).exists():
                result['msg'] =  '删除失败，请先删除关联的项目版本'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            Project.objects.filter(id=data.get('project_id')).update(is_delete = 1)
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectSystemFieldsAPIVIEW(APIView):
    '''获取项目系统字段信息'''

    def get(self, request, format=None):
        try:
            result = {}
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = SYS_CUSTOM_FIELDS
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            logger.error('%s' % e)
            result['msg'] =  '获取系统自定义字段出错：%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

class  PlatformProjectsAPIView(APIView):
    '''获取某个平台关联的项目信息'''

    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            platform = params.get('platform').lower()
            projects = []
            if platform == 'jira':
                projects = JiraProject.get_all_projects()
            elif platform == 'zentao':# 禅道
                projects = ZentaoProject.get_all_projects()
            elif platform == 'tapd':
                pass
            else:
                result['msg'] =  '不支持的平台类型：%s' % platform
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = projects
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            logger.error('%s' % e)
            result['msg'] =  '获取平台关联的项目信息出错：%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class JiraIssueTypeAPIView(APIView):
    '''获取jira系统问题类型'''

    def get(self, request, format=None):
        result = {}
        try:
            issue_types = JiraIssue.get_all_issue_types()
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = issue_types
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            logger.error('%s' % e)
            result['msg'] =  '获取jira平台问题类型出错：%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class JiraIssueCustomFieldAPIView(APIView):
    '''获取jira问题自定义字段列表'''

    def get(self, request, format=None):
        result = {}
        try:
            custom_fields = JiraIssue.get_all_custom_fields()
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = custom_fields
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            logger.error('%s' % e)
            result['msg'] =  '获取jira平台问题自定义字段出错：%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

class ZentaoDefectCustomFieldAPIView(APIView):
    '''获取禅道缺陷自定义字段列表'''

    def get(self, request, format=None):
        result = {}
        try:
            custom_fields = ZentaoDefect.get_all_custom_fields()
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = custom_fields
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            logger.error('%s' % e)
            result['msg'] =  '获取禅道平台缺陷自定义字段出错：%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

class PlatformProjectAssociationAPIView(APIView):
    '''平台项目关联关系管理'''

    # 新增\修改
    def post(self, request, format=None):
        result = {}

        try:
            data = request.data
            data['creater_id'] = request.user.id
            data['creater_name'] = request.user.name
            data['updater_id'] = data['creater_id']
            data['updater_name'] = data['creater_name']
            defect_issue_type_id = data.get('defect_issue_type_id')
            data['defect_issue_type_id'] =  defect_issue_type_id

            defect_status_map = data.get('defect_status_map')
            defect_status_map = defect_status_map.strip() if defect_status_map else ''
            data['defect_status_map'] = defect_status_map

            defect_severity_map = data.get('defect_severity_map')
            defect_severity_map = defect_severity_map.strip() if defect_severity_map else ''
            data['defect_severity_map'] = defect_status_map

            custom_field_map = json.dumps(data.get('custom_field_map'))


            data['custom_field_map'] = custom_field_map

            platform_project_name = data.get('platform_project_name')
            platform_project_id = data.get('platform_project_id')

            platform = data.get('platform')

            project_id = data.get('project_id')

            obj = ProjectAssociated.objects.filter(project_id=project_id).first()

            if obj:
                obj.platform_project_name = platform_project_name
                obj.platform_project_id = platform_project_id
                obj.platform = platform
                obj.defect_issue_type_id =defect_issue_type_id
                obj.defect_status_map = defect_status_map
                obj.defect_severity_map = defect_severity_map
                obj.custom_field_map = custom_field_map
                obj.updater_id = request.user.id
                obj.updater_name = request.user.name
                obj.save()
            else:
                ProjectAssociated(**data).save()
            result['msg'] =  '关联成功'
            result['success'] =  True
            result['data'] =  {'platformProjectName': platform_project_name, 'platformProjectId':platform_project_id,
                               'platform':platform, 'defectIssueTypeId': defect_issue_type_id,
                               # 'defectSourceField': defect_source_field, 'defectSeverityField': defect_severity_field,
                               'defectStatusMap': defect_status_map, 'defectSeverityMap': defect_severity_map, 'customFieldMap': custom_field_map }
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


    # 删除
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            project_id = data.get('project_id')

            ProjectAssociated.objects.filter(project_id=project_id).delete()
            result['msg'] =  '保存成功'
            result['success'] =  True
            result['data'] =  {'platformProjectName':'', 'platformProjectId':'', 'platform':''}
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

