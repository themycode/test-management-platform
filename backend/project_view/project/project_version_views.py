#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import logging
from datetime import date, datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from backend.models import Project
from backend.models import ProjectVersion
from backend.models import ProjectAssociated
from backend.models import ProjectVersionAssociated
from backend.serializers import ProjectVersionSerializer

from backend.jira.project import JiraProject
from backend.zentao.project import ZentaoProject

logger = logging.getLogger('mylogger')

class ProjectVersionListAPIView(APIView):
    '''
    项目视图-版本管理
    '''

    # 查询列表数据
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            page_size = int(params.get('pageSize'))
            page_no = int(params.get('pageNo'))
            name = params.get('name')
            project_id = params.get('projectId')
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
            where = ['tb_project_version.is_delete = 0']
            if name:
                where.append('locate("%s", name) ' % name)
                # filters['name__startswith'] = name
            if project_id:
                where.append('project_id = %s' % int(project_id))
            where = ' AND '.join(where)
            where = 'WHERE ' + where
                # filters['project_id'] = int(project_id)
            sql = 'SELECT tb_project_version.id, COUNT(1) AS count FROM tb_project_version JOIN tb_sprint ON tb_sprint.id = tb_project_version.sprint_id ' \
                  'LEFT JOIN tb_project_version_associated ' \
                  'ON tb_project_version.id=tb_project_version_associated.project_version_id ' \
                  '%s' % where
            query_rows = ProjectVersion.objects.raw(sql)
            total = query_rows[0].__dict__.get('count') if query_rows else 0

            sql =  "SELECT tb_project_version.*, tb_sprint.name AS sprint, IFNULL(platform_project_version_name, '') AS platform_project_version_name, " \
                   "IFNULL(platform_project_version_id, '') AS platform_project_version_id, IFNULL(platform, '') AS platform " \
                   "FROM tb_project_version JOIN tb_sprint ON tb_sprint.id = tb_project_version.sprint_id " \
                   "LEFT JOIN tb_project_version_associated " \
                   "ON tb_project_version.id=tb_project_version_associated.project_version_id " \
                   "%s ORDER BY %s " \
                   "LIMIT %s,%s " % (where, order_by, startIndex, page_size)
            query_rows = ProjectVersion.objects.raw(sql)
            rows = []
            for item in query_rows:
                item.__dict__.pop('_state')
                item.__dict__['create_time'] = item.__dict__['create_time'].strftime('%Y-%m-%d %H:%M:%S')
                item.__dict__['update_time'] = item.__dict__['update_time'].strftime('%Y-%m-%d %H:%M:%S')
                rows.append(item.__dict__)

            # rows = ProjectVersion.objects.filter(**filters).extra(
            #     select={'sprint':'SELECT tb_sprint.name FROM tb_sprint WHERE tb_sprint.id = tb_project_version.sprint_id'}
            # ).order_by(*sort_list)[startIndex:endIndex]
            # rows = ProjectVersionSerializer(rows, many=True).data
            # total = ProjectVersion.objects.filter(**filters).count()

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
            with transaction.atomic():
                ProjectVersion.objects.filter(id__in=row_ids).update(is_delete=1)
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectVersionAPIView(APIView):
    '''
    项目视图-版本管理，新增，修改，删除版本
    '''

    # 新增版本
    def post(self, request, format=None):
        result = {}

        try:
            data = request.data
            project_id = data.get('project_id')
            version_name = data.get('name')
            data['creater_id'] = request.user.id
            data['updater_id'] = data['creater_id']
            data['creater_name'] = request.user.name
            data['updater_name'] = data['creater_name']
            data['zt_project_version_id'] = -1
            data['is_delete'] = False

            # 查询项目关联的禅道项目id和产品id
            project = Project.objects.filter(id=project_id, is_delete=0).first()
            if not project:
                result['msg'] =  '新增失败，所属项目不存在'
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)
            data['product_id'] = project.product_id

            if ProjectVersion.objects.filter(name=version_name, project_id=project_id, is_delete=0).exists():
                result['msg'] =  '新增失败，版本已存在'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            try:
                with transaction.atomic():
                    serializer = ProjectVersionSerializer(data=data)
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


    # 修改版本
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['updater_id'] = request.user.id
            data['updater_name'] = request.user.name
            project_version_name = data.get('name')
            project_version_id = data.get('id')

            if ProjectVersion.objects.exclude(id=project_version_id).filter(name=project_version_name, is_delete=0).exists():
                result['msg'] =  '修改失败，版本名称已存在'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            obj = ProjectVersion.objects.filter(id=project_version_id).first()
            del data['id']
            if obj:
                try:
                    serializer = ProjectVersionSerializer(obj, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                except Exception as e:
                    result['msg'] =  '修改失败：%s!' % e
                    result['success'] =  False
                    return Response(result, status.HTTP_400_BAD_REQUEST)
            else:
                result['msg'] = '修改失败,当前版本不存在'
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result['msg'] =  '修改成功'
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


    # 删除版本
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            project_version_id = data.get('id')

            with transaction.atomic():
                ProjectVersion.objects.filter(id=project_version_id).update(is_delete=True)
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class VersionsDetailsForProjectAPIView(APIView):
    '''按指定字段获取某个项目关联的项目版本信息'''

    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            project_id = params.get('projectId')
            fields = params.get('fields')
            sort = params.get('sort')
            if fields:
                fields = fields.split(',')
            else:
                fields = ['id', 'name']

            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            filters = {'is_delete':0, 'project_id': project_id}
            projects = ProjectVersion.objects.filter(**filters).order_by(*sort_list).values(*fields)

            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = projects
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            logger.error('%s' % e)
            result['msg'] =  '获取产品关联的项目信息出错：%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



class PlatformProjectVersionsAPIView(APIView):
    '''获取某个平台项目关联的项目版本信息'''

    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            project_id = params.get('projectId').lower()

            # 查找关联的项目
            project_associated = ProjectAssociated.objects.filter(project_id=project_id).first()
            if not project_associated:
                result['msg'] =  '未找到关联项目，请先为当前项目先配置关联项目'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            platform = project_associated.platform.lower()
            project_id_associated = project_associated.platform_project_id

            project_versions = []
            if platform == 'jira':
                project_versions = JiraProject.get_project_versions_by_project(project_id_associated)
            elif platform == 'zentao':# 禅道
                project_versions = ZentaoProject.get_project_versions_by_project(project_id_associated)
            elif platform == 'tapd':
                pass
            else:
                result['msg'] =  '不支持关联项目所属的平台类型：%s' % platform
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = project_versions
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            logger.error('%s' % e)
            result['msg'] =  '获取项目关联的项目版本列表出错：%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectVersionAssociationAPIView(APIView):
    '''平台项目版本关联关系管理'''

    # 新增、修改
    def post(self, request, format=None):
        result = {}

        try:
            data = request.data
            data['creater_id'] = request.user.id
            data['creater_name'] = request.user.name
            data['updater_id'] = data['creater_id']
            data['updater_name'] = data['creater_name']

            project_version_id = data.get('project_version_id')

            obj = ProjectVersionAssociated.objects.filter(project_version_id=project_version_id).first()
            if obj:
                obj.platform_project_version_name = data.get('platform_project_version_name')
                obj.platform_project_version_id = data.get('platform_project_version_id')
                obj.platform = data.get('platform')
                obj.updater_id = request.user.id
                obj.updater_name = request.user.name
                obj.save()
            else:
                ProjectVersionAssociated(**data).save()
            result['msg'] =  '关联成功'
            result['success'] =  True
            result['data'] =  {'platformProjectVersionName':data.get('platform_project_version_name'), 'platformProjectVersionId':data.get('platform_project_version_id'), 'platform':data.get('platform')}
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
            project_version_id = data.get('project_version_id')

            ProjectVersionAssociated.objects.filter(project_version_id=project_version_id).delete()
            result['msg'] =  '解除关联成功'
            result['success'] =  True
            result['data'] =  {'platformProjectVersionName':'', 'platformProjectVersionId':'', 'platform':''}
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


