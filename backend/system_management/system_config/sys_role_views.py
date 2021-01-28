#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.models import SysRole
from backend.models import SysRoleMenu
from backend.serializers import SysRoleSerializer
from django.db import transaction
# from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
# from rest_framework.renderers import JSONRenderer

import logging

logger = logging.getLogger('mylogger')

class RoleListAPIView(APIView):
    '''
    系统管理-系统配置-角色管理-角色列表
    '''
    # 查询列表数据
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            page_size = int(params.get('pageSize'))
            page_no = int(params.get('pageNo'))
            is_active = params.get('isActive')
            name = params.get('name')
            sort = params.get('sort')
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            startIndex = (page_no - 1) * page_size
            endIndex = startIndex + page_size
            filters = {'is_delete':0}
            if is_active != '':
                if is_active == 'true':
                    is_active = 1
                else:
                    is_active = 0
                filters['is_active'] = is_active
            if name:
                filters['name__startswith'] = name

            rows = SysRole.objects.filter(**filters).order_by(*sort_list)[startIndex:endIndex]
            rows = SysRoleSerializer(rows, many=True).data

            total = SysRole.objects.filter(**filters).count()

            # rows = SysRole.objects.filter(**filters)
            # rows = SysRoleSerializer(rows, many=True).data
            # total = len(rows)
            #
            # paginator = Paginator(rows, page_size) # 设置每页展示的数据
            # try:
            #     page = paginator.page(page_no)
            # except PageNotAnInteger as e: # 如果请求的页面编号不存在，返回第一页数据
            #     logger.warn('%s' % e)
            #     page = paginator.page(1)
            # except EmptyPage as e: # 如果请求页面，超出页面范围，返回最后一页数据
            #     logger.warn('%s' % e)
            #     page = paginator.page(paginator.num_pages)
            # rows = page.object_list

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
            SysRole.objects.filter(id__in=row_ids).update(is_delete=1)
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class RoleAPIView(APIView):
    '''
    系统管理-系统配置-角色管理，新增，修改，删除角色
    '''

    # 新增角色
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
                serializer = SysRoleSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # 往测试集表新增记录
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

    # 修改角色
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['updater_id'] = request.user.id
            data['updater_name'] = request.user.name

            obj = SysRole.objects.filter(id=data.get('id')).first()
            del data['id']
            if obj:
                try:
                    serializer = SysRoleSerializer(obj, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                except Exception as e:
                    result['msg'] =  '操作失败：%s' % e
                    result['success'] =  False
                    return Response(result, status.HTTP_400_BAD_REQUEST)

                result['msg'] =  '操作成功'
                result['success'] =  True

                temp_data = {}
                # data_keys用于存放要返回的被修改项名称
                data_keys = list(data.keys())
                data_keys.append('update_time')
                for key in data_keys:
                    temp_data[key] = serializer.data.get(key)
                result['data'] =  temp_data
                return Response(result, status.HTTP_200_OK)
            else:
                result['msg'] = '操作失败,角色不存在'
                result['success'] = False
                return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 删除角色
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            obj = SysRole.objects.filter(id=data.get('id')).first()
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


class RelatedMenusAPIView(APIView):
    '''
    系统管理-系统配置-角色管理，获取关联菜单、关联/取消关联菜单
    '''

    # 获取关联菜单
    def get(self, request, format=None):
        result = {}
        try:
            data = request.GET
            menu_id_list = SysRoleMenu.objects.filter(role_id=data.get('roleId')).values_list('menu_id', flat=True)

            result['data'] = menu_id_list
            result['msg'] =  '获取成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



    # 关联/取消关联菜单
    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            role_id = data.get('role_id')
            related_menu_id_list = data.get('related_menus')
            try:
                with transaction.atomic():
                    related_menu_id_set = set(SysRoleMenu.objects.filter(role_id=role_id).values_list('menu_id', flat=True)) # 获取旧的关联菜单的ID
                    menus_for_binding = set(related_menu_id_list) - related_menu_id_set # 待关联的菜单
                    menus_for_unbinding = related_menu_id_set - set(related_menu_id_list) # 待取消关联的菜单

                    # 取消关联菜单
                    SysRoleMenu.objects.filter(menu_id__in=menus_for_unbinding, role_id=role_id).delete()

                     # 关联菜单
                    for menu_id in menus_for_binding:
                        obj = SysRoleMenu.objects.filter(role_id=role_id, menu_id=menu_id)
                        if not obj.exists():
                            obj = SysRoleMenu(role_id=role_id, menu_id=menu_id)
                            obj.save()
            except Exception as e:
                result['msg'] =  '绑定失败：%s' % e
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


            result['msg'] =  '绑定成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


