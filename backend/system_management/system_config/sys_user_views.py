#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backend.models import User
from backend.models import SysRole
from backend.models import SysUserRole
from backend.models import SysGroup
from backend.models import SysUserGroup
from backend.models import SysUserAccount
from backend.models import SysMenu
from backend.models import SysRoleMenu

from backend.serializers import UserSerializer
from backend.serializers import SysGroupSerializer
from backend.serializers import SysUserAccountSerializer

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate



import logging

logger = logging.getLogger('mylogger')

class UserListAPIView(APIView):
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
            name = params.get('name')
            is_active = params.get('isActive')
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
            if account:
                filters['username__startswith'] = account
            if is_active != '':
                if is_active == 'true':
                    is_active = 1
                else:
                    is_active = 0
                filters['is_active'] = is_active

            rows = User.objects.filter(**filters).order_by(*sort_list)[startIndex:endIndex]
            rows = UserSerializer(rows, many=True).data

            for row in rows:
                # 获取关联的角色
                related_role_id_list = SysUserRole.objects.filter(user_id=row.get('id')).values_list('role_id', flat=True)
                related_roles = SysRole.objects.filter(id__in=related_role_id_list, is_active=1, is_delete=0).values('id', 'name')
                row['roles'] = related_roles

                # 获取关联的组别
                related_group_id_list = SysUserGroup.objects.filter(user_id=row.get('id')).values_list('group_id', flat=True)
                related_groups = SysGroup.objects.filter(id__in=related_group_id_list, is_delete=0).values('id', 'name')
                row['groups'] = related_groups

            total = User.objects.filter(**filters).count()

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
            rows = User.objects.filter(id__in=row_ids)
            for row in rows:
                if request.user.id == row.id: # 不能删除自身账号
                    continue
                row.is_delete = 1
                row.save()
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserAPIView(APIView):
    '''
    系统管理-系统配置-用户管理，新增，修改，删除用户
    '''

    # 新增用户
    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            account = data.get('account')
            email = data.get('email')
            mobile = data.get('mobile')
            job_number = data.get('job_number')

            data['creater_id'] = request.user.id
            data['updater_id'] = data['creater_id']
            data['is_delete'] = False
            data['password'] = make_password('123456')

            users = User.objects.filter(username=account, is_delete=0)
            if users.exists():
                result['msg'] =  '新增失败：用户帐号已存在'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)
            elif User.objects.filter(email=email, is_delete=0).exists():
                result['msg'] =  '新增失败：邮箱已存在'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)
            elif User.objects.filter(mobile=mobile, is_delete=0).exists():
                result['msg'] =  '新增失败：手机号已存在'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)
            elif User.objects.filter(job_number=job_number, is_delete=0).exists():
                result['msg'] =  '新增失败：工号已存在'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            try:
                serializer = UserSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except Exception as e:
                result['msg'] =  '新增失败：%s' % e
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result_data = serializer.data
            result_data['roles'] = []
            result_data['groups'] = []
            result['msg'] =  '新增成功'
            result['success'] =  True
            result['data'] =  result_data
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 修改用户
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            user_id = data.get('id')
            if request.user.id == user_id and  'is_active' in data.keys() and not data.get('is_active'):
                result['msg'] = '操作失败,不能禁用自身账号'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            data['updater_id'] = request.user.id

            obj = User.objects.filter(id=user_id).first()
            del data['id']
            if obj:
                account = data.get('account')
                email = data.get('email')
                mobile = data.get('mobile')
                job_number = data.get('job_number')

                users = User.objects.exclude(id=obj.id).filter(username=account, is_delete=0)
                if users.exists():
                    result['msg'] =  '修改失败：用户名已存在'
                    result['success'] =  False
                    return Response(result, status.HTTP_200_OK)
                elif User.objects.exclude(id=obj.id).filter(email=email, is_delete=0).exists():
                    result['msg'] =  '修改失败：邮箱已存在'
                    result['success'] =  False
                    return Response(result, status.HTTP_200_OK)
                elif User.objects.exclude(id=obj.id).filter(mobile=mobile, is_delete=0).exists():
                    result['msg'] =  '修改失败：手机号已存在'
                    result['success'] =  False
                    return Response(result, status.HTTP_200_OK)
                elif User.objects.exclude(id=obj.id).filter(job_number=job_number, is_delete=0).exists():
                    result['msg'] =  '修改失败：工号已存在'
                    result['success'] =  False
                    return Response(result, status.HTTP_200_OK)
                try:
                    serializer = UserSerializer(obj, data=data, partial=True)
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
                result['msg'] = '修改失败,用户不存在'
                result['success'] =  False
                return Response(request, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 删除用户
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            if request.user.id == data.get('id'):
                result['msg'] = '操作失败,不能删除自身账号'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            obj = User.objects.filter(id=data.get('id')).first()
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

    # 获取用户
    def get(self, request):
        result = {}
        try:
            data = request.GET
            obj = User.objects.filter(id=data.get('user_id')).first()
            if obj:
                result['data'] = UserSerializer(obj).data
            else:
                result['data'] = {}

            result['msg'] =  '获取成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '获取指定用户信息失败：%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserPersonalInfo(APIView):
    ''' 获取用户个人信息 '''

    def get(self, request, format=None):
        result = {}
        try:
            user = request.user
            if user.id:
                result['data'] = UserSerializer(user).data
            else:
                result['data'] = {}

            result['msg'] =  '获取成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '用户当前用户信息失败：%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

class UnrelatedRolesAPIView(APIView):
    '''
    系统管理-系统配置-用户管理，获取单个用户关联的角色
    '''

    # 获取未关联角色
    def get(self, request, format=None):
        result = {}
        try:
            data = request.GET
            # 获取用户已关联角色ID
            related_role_id_list = SysUserRole.objects.filter(user_id=data.get('userId')).values_list('role_id', flat=True)

            # 获取未关联角色
            roles = SysRole.objects.exclude(id__in=related_role_id_list).filter(is_delete=0, is_active=1).order_by('-id').values('id', 'name')
            result['data'] = roles
            result['msg'] =  '获取成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserRolesAPIView(APIView):
    '''
    系统管理-系统配置-用户管理，给单个用户关联角色
    '''
    # 分配角色
    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            user_id = data.get('user_id')
            role_id_list = data.get('role_ids')
            for role_id in role_id_list:
                obj = SysUserRole.objects.filter(role_id=role_id, user_id=user_id)
                if not obj.exists():
                    obj = SysUserRole(role_id=role_id, user_id=user_id)
                    obj.save()
            result['msg'] =  '分配成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserRoleAPIView(APIView):
    '''
    系统管理-系统配置-用户管理，删除用户关联的单个角色
    '''

    # 取消关联角色
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            user_id = data.get('user_id')
            role_id = data.get('role_id')
            obj = SysUserRole.objects.filter(role_id=role_id, user_id=user_id)
            if obj.exists():
                obj.delete()
            result['msg'] =  '取消关联成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



class UnrelatedGroupsAPIView(APIView):
    '''
    系统管理-系统配置-用户管理，获取单个用户未关联的组别
    '''

    # 获取未关联组别
    def get(self, request, format=None):
        result = {}
        try:
            data = request.GET
            # 获取用户已关联组别ID
            related_group_id_list = SysUserGroup.objects.filter(user_id=data.get('userId')).values_list('group_id', flat=True)

            # 获取未关联组别
            result['data'] = SysGroup.objects.exclude(id__in=related_group_id_list).filter(is_delete=0).order_by('-id').values('id', 'name')
            result['msg'] =  '获取成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserGroupsAPIView(APIView):
    '''
    系统管理-系统配置-用户管理，给单个用户关联组别
    '''

    # 关联组别
    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            user_id = data.get('user_id')
            group_id_list = data.get('group_ids')
            for group_id in group_id_list:
                obj = SysUserGroup.objects.filter(group_id=group_id, user_id=user_id)
                if not obj.exists():
                    obj = SysUserGroup(group_id=group_id, user_id=user_id)
                    obj.save()
            result['msg'] =  '关联成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserGroupsDetailsAPIView(APIView):
    '''
    获取用户关联的组别详细信息（按字段获取）
    '''

    @staticmethod
    def get_user_groups_details(user, params):
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

        if not user.is_superuser:
            # 获取用户已关联组别ID
            related_group_id_list = SysUserGroup.objects.filter(user_id=user.id).values_list('group_id', flat=True)
            # 获取关联组别
            groups = SysGroup.objects.filter(id__in=related_group_id_list, is_delete=0).order_by(*sort_list).values(*fields)
        else: # 如果未超级用户，返回所有未删除的组
            groups = SysGroup.objects.filter(**filters).order_by(*sort_list).values(*fields)
        return groups

    def get(self, request, format=None):
        ''' 获取用户关联的组别信息（按字段获取） '''
        result = {}
        try:
            params = request.GET
            user_id = request.user.id

            user_obj = User.objects.filter(id=user_id, is_delete=0, is_active=1).first()

            if not user_obj:
                result['msg'] =  '获取用户关联的组别失败:用户不存在或者已被禁用'
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)
            groups = UserGroupsDetailsAPIView.get_user_groups_details(user_obj, params)

            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = groups
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserGroupAPIView(APIView):
    '''
    系统管理-系统配置-用户管理，删除用户关联的单个组别
    '''

    # 取消关联组别
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            user_id = data.get('user_id')
            group_id = data.get('group_id')
            obj = SysUserGroup.objects.filter(group_id=group_id, user_id=user_id)
            if obj.exists():
                obj.delete()
            result['msg'] =  '取消关联成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



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

            startIndex = (page_no - 1) * page_size
            endIndex = startIndex + page_size
            filters = {'is_delete':0}
            if name:
                filters['name__startswith'] = name

            rows = SysGroup.objects.filter(**filters).order_by('-id')[startIndex:endIndex]
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
            rows = SysGroup.objects.filter(id__in=row_ids)
            for row in rows:
                if request.user.id == row.id: # 不能删除自身账号
                    continue
                row.is_delete = 1
                row.save()
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class RelatedAccountListAPIView(APIView):
    '''
    系统管理-系统配置-用户管理，用户关联账户列表
    '''

    # 查询列表数据
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            user_id = params.get('userId')

            rows = SysUserAccount.objects.filter(user_id=user_id)
            rows = SysUserAccountSerializer(rows, many=True).data

            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = rows
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class RelatedAccountAPIView(APIView):
    # 新增关联账号
    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            user_id = data.get('user_id')
            platform = data.get('platform')
            obj = SysUserAccount.objects.filter(user_id=user_id, platform=platform).first()
            if obj:
                result['msg'] =  '新增失败，每个平台只能关联一个账号'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            try:
                serializer = SysUserAccountSerializer(data=data)
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

    # 修改关联账号
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data_keys = list(data.keys())
            data_keys.remove('account_id')
            data_keys.remove('user_id')

            user_id = data.get('user_id')
            platform = data.get('platform')
            obj = SysUserAccount.objects.exclude(id=data.get('account_id')).filter(user_id=user_id, platform=platform).first()
            if obj:
                result['msg'] =  '修改失败，所选平台已存在关联账号'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            obj = SysUserAccount.objects.filter(id=data.get('account_id')).first()
            if obj:
                try:
                    serializer = SysUserAccountSerializer(obj, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                except Exception as e:
                    result['msg'] =  '操作失败：%s' % e
                    result['success'] =  False
                    return Response(result, status.HTTP_400_BAD_REQUEST)

                result['msg'] =  '操作成功'
                result['success'] =  True

                temp_data = {}
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
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 删除关联账号
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data

            obj = SysUserAccount.objects.filter(id=data.get('account_id')).first()
            if obj:
                obj.delete()
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserMenusAPIView(APIView):
    permission_classes = []
    # authentication_classes = [SessionAuthentication]

    @staticmethod
    def get_sub_menu(menu, filters, excludes, root_menu_id, root_menu_url):
        ''' 获取子菜单 '''

        father_menu_id = menu['id']
        filters['parent_id'] = father_menu_id
        sub_menus = SysMenu.objects.filter(**filters).exclude(**excludes).order_by('order').values()
        menu['children'] = sub_menus

        for sub_menu in sub_menus:
            sub_menu['is_top_nav'] = False
            sub_menu['top_nav_id'] = root_menu_id
            sub_menu['top_nav_url'] = root_menu_url
            sub_menu['create_time'] = sub_menu['create_time'].strftime('%Y-%m-%d %H:%M:%S')
            sub_menu['update_time'] = sub_menu['update_time'].strftime('%Y-%m-%d %H:%M:%S')
            UserMenusAPIView.get_sub_menu(sub_menu, filters, excludes, root_menu_id, root_menu_url)


    def get(self, request, format=None):
        '''获取用户关联的菜单资源'''

        result = {}
        try:
            user_id = request.user.id

            # 如果用户已登陆
            if user_id:
                # 判断是否超级管理员，如果是超级管理员不做角色判断
                is_superuser = request.user.is_superuser

                if is_superuser: # 超级管理员
                    # 用户未登陆，获取“未登录是否展示”为1，并且“是否在前端展示”为0的,未删除菜单
                    filters = {'is_delete':0, 'parent_id':1}
                    excludes = {'type':'按钮'}
                    father_menus = SysMenu.objects.filter(**filters).exclude(**excludes).order_by('order').values()
                else: # 否则普通管理员
                    # 获取用户已关联角色ID
                    related_role_id_list = SysUserRole.objects.filter(user_id=user_id).values_list('role_id', flat=True)

                    # 过滤已经删除、禁用的角色ID
                    related_role_id_list = SysRole.objects.filter(id__in=related_role_id_list, is_delete=0, is_active=1).values_list('id', flat=True)

                    # 通过角色ID获取用户已关联菜单ID
                    related_menu_id_list = SysRoleMenu.objects.filter(role_id__in=related_role_id_list).values_list('menu_id', flat=True)

                    related_menu_id_list = list(set(related_menu_id_list))

                    filters = {'is_delete':0, 'show':1, 'parent_id':1, 'id__in':related_menu_id_list}
                    excludes = {'type':'按钮'}
                    father_menus = SysMenu.objects.filter(**filters).exclude(**excludes).order_by('order').values()
            else: # 用户未登陆，获取“未登录是否展示”为1，并且“是否在前端展示”为0的,未删除菜单
                filters = {'is_delete':0, 'show_without_auth':1, 'show':1, 'parent_id':1}
                excludes = {'type':'按钮'}
                father_menus = SysMenu.objects.filter(**filters).exclude(**excludes).order_by('order').values()

            for father_menu in father_menus:
                father_menu['create_time'] = father_menu['create_time'].strftime('%Y-%m-%d %H:%M:%S')
                father_menu['update_time'] = father_menu['update_time'].strftime('%Y-%m-%d %H:%M:%S')
                father_menu['is_top_nav'] = True # 用于标记是否是顶级菜单
                father_menu['top_nav_id'] = father_menu['id']
                father_menu['top_nav_url'] = father_menu['url']
                UserMenusAPIView.get_sub_menu(father_menu, filters, excludes, father_menu['id'], father_menu['url'])

            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = father_menus
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserPasswdAPIView(APIView):
    '''
    顶部导航-用户-修改密码
    '''

    # 修改用户密码
    def put(self, request, format=None):
        result = {}
        try:
            data = request.data
            old_passwd = data.get('old_passwd')
            new_passwd = data.get('new_passwd')
            confirm_passwd = data.get('confirm_passwd')

            user_id = request.user.id
            user = User.objects.filter(id=user_id,is_delete=0).first()
            if user:
                if not user.is_active:
                    result['msg'] =  '修改失败：当前用户已被禁用'
                    result['success'] =  False
                    return Response(result, status.HTTP_200_OK)
                else:
                    user = authenticate(request, username=user.username, password=old_passwd)
                    if user:
                        if new_passwd == confirm_passwd:
                            user.password = make_password(new_passwd)
                            user.save()
                        else:
                            result['msg'] =  '修改失败：两次密码修改不一致'
                            result['success'] =  False
                            return Response(result, status.HTTP_200_OK)

                        result['msg'] =  '修改成功'
                        result['success'] =  True
                        return Response(result, status.HTTP_200_OK)
                    else:
                        result['msg'] =  '修改失败：原密码输入错误'
                        result['success'] =  False
                        return Response(result, status.HTTP_200_OK)
            else:
                result['msg'] = '修改失败,用户不存在或者已被删除'
                result['success'] =  False
                return Response(request, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 重置用户密码
    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            user_id = data.get('user_id')
            user = User.objects.filter(id=user_id).first()
            if user:
                user.password = make_password('123456')
                user.save()

                result['msg'] =  '重置成功'
                result['success'] =  True
                return Response(result, status.HTTP_200_OK)
            else:
                result['msg'] =  '修改失败：用户不存在'
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UsersDetailsAPIView(APIView):
    '''
    批量获取用户指定字段信息
    '''
    # 查询详情
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

            filters = {'is_delete':0, 'is_active':1}
            rows = User.objects.filter(**filters).order_by(*sort_list).values(*fields)
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = rows
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)