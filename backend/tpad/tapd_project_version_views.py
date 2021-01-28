#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = '赖富玉'

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backend.models import Sprint
from backend.serializers import SprintSerializer

from backend.tpad.tpadTool import TpadProjectTool

import logging
import json

logger = logging.getLogger('mylogger')


class TapdProjectVersionAPIView(APIView):
    '''
    系统管理-迭代管理，新增、修改TPAD项目版本
    '''

    # 创建TPAD项目版本
    def post(self, request, format=None):
        result = {}

        try:
            data = request.data

            sprint_id = data.get('sprint_id')
            # project_id = data.get('project_id')
            project_id = settings.TPAD_PROJECT_ID
            name = data.get('name')
            creater = request.user.name
            description = data.get('description')
            logger.info( data.get('publish_date'))

            obj = Sprint.objects.filter(id=sprint_id).first()
            if not obj:
                result['success'] = False
                result['msg'] = '创建TPAD项目版本失败：当前迭代不存在'
                return Response(result, status.HTTP_400_BAD_REQUEST)

            version_data = 'workspace_id=%s&name=%s&creator=%s&description=%s' % (project_id, name, creater, description)
            request_result = TpadProjectTool.create_or_update_project_version(version_data)
            if request_result[0]:
                response_body = request_result[1]
                response_body= json.loads(response_body)
                info = response_body.get('info')
                if info == 'success':
                    # 创建项目成功
                    tpad_project_version_id = response_body.get('data').get('Version').get('id') or 0
                    data = {'updater_id':request.user.id, 'updater_name':creater, 'publish_date': data.get('publish_date'), 'tpad_project_version_id':tpad_project_version_id}
                    serializer = SprintSerializer(obj, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                else:
                    result['success'] = False
                    result['msg'] = '创建TPAD项目版本失败：%s，请前往tpad检查是否已存在对应名称的版本' % info
                    return Response(result, status.HTTP_200_OK)
            else:
                result['success'] = False
                result['msg'] = '创建TPAD项目版本失败：%s' % request_result[1]
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

            result['msg'] =  '创建成功'
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

    # 修改tpad项目版本
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            project_version_id = data.get('version_id')
            name = data.get('name')
            modifier = request.user.name
            description = data.get('description')
            # project_id = data.get('project_id')
            project_id = settings.TPAD_PROJECT_ID
            version_data = "name=%s&id=%s&workspace_id=%s&modifier=%s&description=%s"  % (name, project_version_id, project_id, modifier, description)
            request_result = TpadProjectTool.create_or_update_project_version(version_data)
            if request_result[0]:
                response_body = request_result[1]
                response_body= json.loads(response_body)
                info = response_body.get('info')
                if info != 'success':
                    result['success'] = False
                    result['msg'] = '修改TPAD项目版本失败：%s' % info
                    return Response(result, status.HTTP_200_OK)
                else:
                    sprint = Sprint.objects.filter(id=data.get('sprint_id')).first()
                    data = {'updater_id':request.user.id, 'updater_name':modifier, 'publish_date': data.get('publish_date')}
                    serializer = SprintSerializer(sprint, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

            else:
                result['success'] = False
                result['msg'] = '修改TPAD项目版本失败：%s' % request_result[1]
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

            temp_data = {}
            data_keys = list(data.keys())
            data_keys.append('update_time')

            for key in data_keys:
                temp_data[key] = serializer.data.get(key)
            result['data'] =  temp_data
            result['msg'] =  '修改TPAD项目版本成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


