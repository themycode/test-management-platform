#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.models import SysGroup
from backend.models import SysGroupRelatedGroup

from backend.serializers import SysGroupSerializer
from backend.serializers import SysGroupRelatedGroupSerializer


import logging

logger = logging.getLogger('mylogger')

class GroupListAPIView(APIView):
    '''
    系统管理-系统配置-组别管理-组别列表
    '''
    # 查询列表数据
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            page_size = int(params.get('pageSize'))
            page_no = int(params.get('pageNo'))
            name = params.get('name')
            sort = params.get('sort')
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']
            startIndex = (page_no - 1) * page_size
            endIndex = startIndex + page_size
            filters = {'is_delete':0}
            if name:
                filters['name__startswith'] = name

            rows = SysGroup.objects.filter(**filters).order_by(*sort_list)[startIndex:endIndex]
            rows = SysGroupSerializer(rows, many=True).data

            total = SysGroup.objects.filter(**filters).count()

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
            SysGroup.objects.filter(id__in=row_ids).update(is_delete=1)
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class GroupAPIView(APIView):
    '''
    系统管理-系统配置-组别管理，新增，修改，删除组别
    '''

    # 新增组别
    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['creater_id'] = request.user.id
            data['updater_id'] = data['creater_id']
            data['creater_name'] = request.user.name
            data['updater_name'] = data['creater_name']
            data['is_delete'] = False

            name = data.get('name')
            obj = SysGroup.objects.filter(name=name).first()
            if obj:
                result['msg'] =  '新增失败,已存在相同名称的组别'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            try:
                serializer = SysGroupSerializer(data=data)
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

    # 修改组别
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['updater_id'] = request.user.id
            data['updater_name'] = request.user.name
            group_id = data.get('id')
            name = data.get('name')

            obj = SysGroup.objects.exclude(id=group_id).filter(name=name).first()
            if obj:
                result['msg'] =  '新增失败,已存在相同名称的组别'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            obj = SysGroup.objects.filter(id=group_id).first()
            del data['id']
            if obj:
                try:
                    serializer = SysGroupSerializer(obj, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                except Exception as e:
                    result['msg'] =  '修改失败：%s' % e
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
            else:
                result['msg'] = '修改失败,组别不存在'
                result['success'] =  False
                return Response(request, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 删除组别
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data

            obj = SysGroup.objects.filter(id=data.get('id')).first()
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

