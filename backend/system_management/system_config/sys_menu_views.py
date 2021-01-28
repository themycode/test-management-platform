#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.models import SysMenu
from backend.serializers import SysMenuSerializer

from django.db.models import Max
from django.db import transaction

import logging
logger = logging.getLogger('mylogger')

class MenuTreeAPIView(APIView):
    '''
    系统配置-菜单管理-菜单树
    '''
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            recursive = params.get('recursive') # 是否递归查找子节点
            parent_id = params.get('parentId')

            def get_sub_resource(resource):
                '''
                获取子级资源
                '''
                nonlocal tree_nodes_list
                resource_id = resource['id']   # 获取上级资源的id

                sub_sources = SysMenu.objects.filter(parent_id=resource_id, is_delete=0).order_by('order')
                sub_sources = SysMenuSerializer(sub_sources, many=True).data
                resource['children'] = sub_sources
                if sub_sources: #如果存在子级资源，遍历添加子级资源
                    for sub_source in sub_sources:
                        get_sub_resource(sub_source)

            # 获取指定parent_id的直接子资源
            father_resources = SysMenu.objects.filter(parent_id=parent_id, is_delete=0).order_by('order')
            father_resources = SysMenuSerializer(father_resources, many=True).data
            tree_nodes_list = father_resources

            if recursive: # 遍历子级资源
                for father_resource in father_resources:
                    get_sub_resource(father_resource) # 获取子级资源

            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = tree_nodes_list
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class MenuAPIView(APIView):
    '''
    系统管理-系统配置-菜单管理，新增，修改，删除菜单
    '''
    # 新增菜单
    def post(self, request, format=None):
        result = {}
        try:
            data = request.data

            data['creater_id'] = request.user.id
            data['updater_id'] = data['creater_id']
            data['is_delete'] = False

            max_order = SysMenu.objects.filter(parent_id=data.get('parent_id')).filter(is_delete=0).aggregate(Max('order'))['order__max']
            if max_order:
                data['order'] = max_order + 1
            else:
                data['order'] = 1

            try:
                serializer = SysMenuSerializer(data=data)
                serializer.is_valid(raise_exception=True)  # 验证数据是否符合要求，raise_exception=True指定不符合条件时自动抛出异常
                serializer.save()
            except Exception as e:
                result['msg'] =  '添加失败：%s' % e
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result['msg'] =  '添加成功'
            result['success'] =  True
            result['data'] =  serializer.data
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 修改菜单
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['updater_id'] = request.user.id
            sys_menu = SysMenu.objects.filter(id=data.get('id')).first()
            del data['id']
            if sys_menu:
                try:
                    serializer = SysMenuSerializer(sys_menu, data=data, partial=True)
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
                result['msg'] = '修改失败,资源不存在'
                result['success'] = False
                return Response(request, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 删除菜单
    def delete(self, request, format=None):
        result = {}
        def delete_sub_menu(parent_id):
            sys_sub_menus = SysMenu.objects.filter(parent_id=parent_id).filter(is_delete=0)
            if sys_sub_menus.exists():
                for sub_menu in sys_sub_menus:
                    sub_menu.is_delete = 1
                    delete_sub_menu(sub_menu.id)
                    sub_menu.save()

        try:
            data = request.data
            sys_menu = SysMenu.objects.filter(id=data.get('id'), is_delete=0).first()
            try:
                with transaction.atomic():
                    if sys_menu:
                        sys_menu.is_delete = 1
                        delete_sub_menu(sys_menu.id)
                        sys_menu.save()
            except Exception as e:
                 result['msg'] =  '删除失败：%s' % e
                 result['success'] =  False
                 return Response(result, status.HTTP_200_OK)

            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


