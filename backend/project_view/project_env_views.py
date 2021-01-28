#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import json
import logging

from collections import OrderedDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from backend.models import ProjectEnv
from backend.serializers import ProjectEnvSerializer

logger = logging.getLogger('mylogger')

class ProjectEnvListView(APIView):
    '''
    项目视图-API项目管理-配置-环境配置
    '''

    # 查询列表数据
    def get(self, request, format=None):
        result = {}
        data = request.GET
        project_id = data.get('projectId')
        try:
            rows = ProjectEnv.objects.filter(project_id=project_id, is_delete=0).order_by('-id').values('id', 'project_id', 'env_name', 'addr', 'headers', 'cookies', 'is_default')
            for item in rows:
                item['headers'] = json.loads(item.get('headers'), object_pairs_hook=OrderedDict)
                item['cookies'] = json.loads(item.get('cookies'), object_pairs_hook=OrderedDict)
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = rows
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProjectEnvView(APIView):
    '''
    项目视图-API项目管理-配置-环境配置，新增，修改，删除项目环境
    '''

    # 新增项目环境
    def post(self, request, format=None):
        result = {}

        try:
            data = request.data
            env_name = data.get('env_name')
            project_id = data.get('project_id')
            data['creater_id'] = request.user.id
            data['updater_id'] = data['creater_id']
            data['creater'] = request.user.name
            data['updater'] = data['creater']
            data['is_delete'] = False
            is_default = data.get('is_default')
            data['headers'] = json.dumps(data.get('headers'))
            data['cookies'] = json.dumps(data.get('cookies'))

            if ProjectEnv.objects.filter(project_id=project_id, env_name=env_name, is_delete=0).exists():
                result['msg'] =  '保存失败，已存在同名环境'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            try:
                with transaction.atomic():
                    if is_default:
                        ProjectEnv.objects.filter(project_id=project_id, is_default=True).update(is_default=False)

                    serializer = ProjectEnvSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            except Exception as e:
                result['msg'] =  '保存失败：%s' % e
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

            result['msg'] =  '保存成功'
            result['success'] =  True
            temp_data = serializer.data
            headers = json.loads(temp_data.get('headers'), object_pairs_hook=OrderedDict)
            cookies = json.loads(temp_data.get('cookies'), object_pairs_hook=OrderedDict)
            temp_data = {'id':temp_data.get('id'), 'project_id':temp_data.get('project_id'), 'env_name':temp_data.get('env_name'),
                         'addr':temp_data.get('addr'), 'headers':headers,  'cookies':cookies, 'is_default':temp_data.get('is_default')}
            result['data'] =  temp_data
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 修改项目环境
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['updater_id'] = request.user.id
            data['updater'] = request.user.name
            data['headers'] = json.dumps(data.get('headers'))
            data['cookies'] = json.dumps(data.get('cookies'))
            env_name = data.get('env_name')
            project_id = data.get('project_id')
            env_id = data.get('env_id')
            is_default = data.get('is_default')

            data.pop('project_id')
            data.pop('env_id')

            if ProjectEnv.objects.filter(env_name=env_name, project_id=project_id, is_delete=0).exclude(id=env_id).exists():
                result['msg'] =  '保存失败，已存在同名环境'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)
            obj = ProjectEnv.objects.filter(id=env_id, is_delete=0).first()
            if obj:
                try:
                    with transaction.atomic():
                        if is_default:
                            ProjectEnv.objects.filter(project_id=project_id, is_default=True).update(is_default=False)
                            serializer = ProjectEnvSerializer(obj, data=data, partial=True)
                            serializer.is_valid(raise_exception=True)
                            serializer.save()
                except Exception as e:
                    result['msg'] =  '保存失败：%s!' % e
                    result['success'] =  False
                    return Response(result, status.HTTP_400_BAD_REQUEST)
            else:
                result['msg'] = '保存失败,项目环境不存在'
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result['msg'] =  '保存成功'
            result['success'] =  True
            temp_data = {}
            data_keys = list(data.keys())
            data_keys.append('update_time')
            for key in data_keys:
                temp_data[key] = serializer.data.get(key)
            temp_data['headers'] = json.loads(temp_data.get('headers'), object_pairs_hook=OrderedDict)
            temp_data['cookies'] = json.loads(temp_data.get('cookies'), object_pairs_hook=OrderedDict)
            result['data'] =  temp_data
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


    # 删除项目环境
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            ProjectEnv.objects.filter(id=data.get('env_id')).update(is_delete = 1)
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
