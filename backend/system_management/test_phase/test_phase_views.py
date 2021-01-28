#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = '赖富玉'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from backend.models import TestPhase
from backend.serializers import TestPhaseSerializer

import logging

logger = logging.getLogger('mylogger')

class TestPhaseListAPIView(APIView):
    '''
    系统管理-测试阶段管理-测试阶段列表
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
                sort_list = ['order','id']

            startIndex = (page_no - 1) * page_size
            endIndex = startIndex + page_size
            filters = {'is_delete':0}
            rows = TestPhase.objects.filter(**filters).order_by(*sort_list)[startIndex:endIndex]
            rows = TestPhaseSerializer(rows, many=True).data
            total = TestPhase.objects.filter(**filters).count()

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
            TestPhase.objects.filter(id__in=row_ids).update(is_delete=1)
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestPhaseDetailsAPIView(APIView):
    '''
    批量获取用例执行阶段详情信息
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
                sort_list = ['order', 'id']

            filters = {'is_delete':0}
            rows = TestPhase.objects.filter(**filters).order_by(*sort_list).values(*fields)
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = rows
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

class TestPhaseAPIView(APIView):
    '''
    系统管理-测试阶段管理，新增，修改，删除测试阶段
    '''

    # 新增
    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['creater_id'] = request.user.id
            data['updater_id'] = data['creater_id']
            data['creater_name'] = request.user.name
            data['updater_name'] = data['creater_name']
            code = data.get('code')
            name = data.get('name')
            data['is_delete'] = False

            if TestPhase.objects.filter(code=code, is_delete=0).exists():
                result['msg'] =  '新增失败，编码(%s)已存在' % code
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)
            if TestPhase.objects.filter(name=name, is_delete=0).exists():
                result['msg'] =  '新增失败，阶段名称(%s)已存在' % name
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)
            try:
               with transaction.atomic():
                   if data.get('default'):
                       TestPhase.objects.filter(default=True).update(default=False)
                   serializer = TestPhaseSerializer(data=data)
                   serializer.is_valid(raise_exception=True)
                   serializer.save()
            except Exception as e:
                result['msg'] =  '新增失败：%s' % e
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result['msg'] =  '新增成功'
            result['success'] =  True
            # result['data'] =  serializer.data
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 修改
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['updater_id'] = request.user.id
            data['updater_name'] = request.user.name
            code = data.get('code')
            name = data.get('name')
            id = data.get('id')
            del data['id']

            if TestPhase.objects.filter(code=code, is_delete=0).exclude(id=id).exists():
                result['msg'] =  '新增失败，编码(%s)已存在' % code
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            if TestPhase.objects.filter(name=name, is_delete=0).exclude(id=id).exists():
                result['msg'] =  '新增失败，阶段名称(%s)已存在' % name
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)
            obj = TestPhase.objects.filter(id=id).first()
            if obj:
                try:
                    with transaction.atomic():
                        if data.get('default'):
                            TestPhase.objects.filter(default=True).exclude(id=id).update(default=False)
                        serializer = TestPhaseSerializer(obj, data=data, partial=True)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                except Exception as e:
                    result['msg'] =  '操作失败：%s' % e
                    result['success'] =  False
                    return Response(result, status.HTTP_400_BAD_REQUEST)
            else:
                result['msg'] = '操作失败,测试阶段不存在'
                result['success'] =  False
                return Response(request, status.HTTP_404_NOT_FOUND)

            result['msg'] =  '操作成功'
            result['success'] =  True

            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 逐个删除
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data

            obj = TestPhase.objects.filter(id=data.get('id')).first()
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


