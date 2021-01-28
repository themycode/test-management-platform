#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = '赖富玉'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.models import SysGroup
from backend.models import MsgPushAccount
from backend.models import MsgPushAccountGroup
from backend.serializers import MsgPushAccountSerializer




import logging

logger = logging.getLogger('mylogger')

class MsgPushAccountListAPIView(APIView):
    '''
    系统管理-系统配置-用户管理-用户列表
    '''
    # 查询列表数据
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            page_size = int(params.get('pageSize'))
            page_no = int(params.get('pageNo'))
            account = params.get('account')
            type = params.get('type')
            is_active = params.get('isActive')
            sort = params.get('sort')
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            startIndex = (page_no - 1) * page_size
            endIndex = startIndex + page_size
            filters = {'is_delete':0}
            if account:
                filters['account__startswith'] = account
            if type:
                filters['type'] = type
            if is_active != '':
                if is_active == 'true':
                    is_active = 1
                else:
                    is_active = 0
                filters['is_active'] = is_active

            rows = MsgPushAccount.objects.filter(**filters).order_by(*sort_list)[startIndex:endIndex]
            rows = MsgPushAccountSerializer(rows, many=True).data

            for row in rows:
                # 获取关联的组别
                related_group_id_list = MsgPushAccountGroup.objects.filter(account_id=row.get('id')).values_list('group_id', flat=True)
                related_groups = SysGroup.objects.filter(id__in=related_group_id_list, is_delete=0).values('id', 'name')
                row['groups'] = related_groups

            total = MsgPushAccount.objects.filter(**filters).count()

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
            MsgPushAccount.objects.filter(id__in=row_ids).update(is_delete=1)

            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



class MsgPushAccountAPIView(APIView):
    '''
    系统管理-推送账号管理，新增，修改，删除消息推送账号
    '''


    # 新增消息推送账号
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
                serializer = MsgPushAccountSerializer(data=data)
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

    # 修改消息推送账号
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['updater_id'] = request.user.id
            data['updater_name'] = request.user.name
            obj = MsgPushAccount.objects.filter(id=data.get('id')).first()
            del data['id']

            if obj:
                try:
                    serializer = MsgPushAccountSerializer(obj, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                except Exception as e:
                    result['msg'] =  '操作失败：%s' % e
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
            else:
                result['msg'] = '操作失败,账号不存在'
                result['success'] =  False
                return Response(request, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            result['data'] ={ "DataId": "2",
            "Data_ID_Id2" :"3"}
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 删除推送账号
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            obj = MsgPushAccount.objects.filter(id=data.get('id')).first()
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


class UnrelatedGroupsAPIView(APIView):
    '''
    系统管理-推送账号管理，获取单个用户未关联的组别
    '''

    # 获取未关联组别
    def get(self, request, format=None):
        result = {}
        try:
            data = request.GET
            # 获取用户已关联组别ID
            related_group_id_list = MsgPushAccountGroup.objects.filter(account_id=data.get('accountId')).values_list('group_id', flat=True)

            # 获取未关联组别
            roles = SysGroup.objects.exclude(id__in=related_group_id_list).filter(is_delete=0).values('id', 'name')
            result['data'] = roles
            result['msg'] =  '获取成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class MsgPushAccountGroupsAPIView(APIView):
    '''
    系统管理-推送账号管理，给单个推送账号关联组别
    '''
    # 关联组别
    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            account_id = data.get('account_id')
            group_id_list = data.get('group_ids')
            for group_id in group_id_list:
                obj = MsgPushAccountGroup.objects.filter(group_id=group_id, account_id=account_id)
                if not obj.exists():
                    obj = MsgPushAccountGroup(group_id=group_id, account_id=account_id)
                    obj.save()
            result['msg'] =  '关联成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



class MsgPushAccountGroupAPIView(APIView):
    '''
    系统管理-推送账号管理，删除消息推送账号关联的某个组别
    '''

    # 取消关联组别
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            account_id = data.get('account_id')
            group_id = data.get('group_id')
            obj = MsgPushAccountGroup.objects.filter(group_id=group_id, account_id=account_id)
            if obj.exists():
                obj.delete()
            result['msg'] =  '取消关联成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


