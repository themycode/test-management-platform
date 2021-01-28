#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backend.models import Env
from backend.serializers import EnvSerializer

import logging

logger = logging.getLogger('mylogger')

class EnvListAPIView(APIView):
    '''
    系统管理-环境管理-环境列表
    '''

    # 查询列表数据
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            page_size = int(params.get('pageSize'))
            page_no = int(params.get('pageNo'))
            sort = params.get('sort')
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            startIndex = (page_no - 1) * page_size
            endIndex = startIndex + page_size
            filters = {'is_delete':0}
            rows = Env.objects.filter(**filters).order_by(*sort_list)[startIndex:endIndex]
            rows = EnvSerializer(rows, many=True).data
            total = Env.objects.filter(**filters).count()

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
            Env.objects.filter(id__in=row_ids).update(is_delete=1)
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class EnvDetailsAPIView(APIView):
    '''
    批量获取环境详情信息
    '''
    # 查询列表数据
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
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

            filters = {'is_delete':0}
            rows = Env.objects.filter(**filters).order_by(*sort_list).values(*fields)
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = rows
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

class EnvAPIView(APIView):
    '''
    系统管理-环境管理，新增，修改，删除环境
    '''

    # 新增环境
    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['creater_id'] = request.user.id
            data['updater_id'] = data['creater_id']
            data['creater_name'] = request.user.name
            data['updater_name'] = data['creater_name']
            data['is_delete'] = False

            try:
                serializer = EnvSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except Exception as e:
                result['msg'] =  '新增失败：%s' % e
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result['msg'] =  '新增成功'
            result['success'] =  True
            result['data'] =  serializer.data
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 修改环境
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['updater_id'] = request.user.id
            data['updater_name'] = request.user.name

            obj = Env.objects.filter(id=data.get('id')).first()
            del data['id']
            if obj:
                try:
                    serializer = EnvSerializer(obj, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                except Exception as e:
                    result['msg'] =  '操作失败：%s' % e
                    result['success'] =  False
                    return Response(result, status.HTTP_400_BAD_REQUEST)
            else:
                result['msg'] = '操作失败,环境不存在'
                result['success'] =  False
                return Response(request, status.HTTP_404_NOT_FOUND)

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

    # 逐个删除环境
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data

            obj = Env.objects.filter(id=data.get('id')).first()
            if obj:
                obj.is_delete = 1
                obj.save()
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


