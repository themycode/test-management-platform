#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.utils import timezone
# from django.utils.translation import ugettext_lazy as _

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from django.core.cache import cache
from django.contrib.auth import logout
from django.conf import settings
from django.db.models import Q
from datetime import timedelta

from .models import User
from .models import SysUserGroup
from .models import SysGroup
from .models import SysUserRole
from .models import SysRole
from .models import SysRoleMenu
from .models import SysMenu
from .models import RefreshToken


import logging
logger = logging.getLogger('mylogger')


class CustomAuthToken(ObtainAuthToken):
    authentication_classes = []
    def post(self, request, *args, **kwargs):

        data = request.data
        refresh_token_key = data.get('refreshToken')

        refres_token = RefreshToken.objects.filter(key=refresh_token_key).first()
        if refres_token is None:
            return Response({
                'success':False,
                'msg':'RefreshTokenNotExists'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 如果refresh token过期则删除
        if timezone.now() > (refres_token.created + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_TIME)):
            refres_token.delete()
            return Response({
                'success':False,
                'msg':'RefreshTokenExpired'
            }, status=status.HTTP_401_UNAUTHORIZED)

        user_id = refres_token.user_id
        user = User.objects.filter(id=user_id).first()
        if user is None:
            return Response({
                'success':False,
                'msg':'刷新token失败，用户不存在'
            }, status=status.HTTP_400_BAD_REQUEST)
        elif user.is_active==1 and user.is_delete==0:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'msg':'获取token成功',
                'success': True
            }, status.HTTP_200_OK)
        elif user.is_active == 0:
            return Response({
                'success':False,
                'msg':'刷新token失败，用户已被禁用'
            }, status=status.HTTP_400_BAD_REQUEST)
        elif user.is_delete == 1:
            return Response({
                'success':False,
                'msg':'刷新token失败，用户已被删除'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    '''
    登录系统
    '''
    permission_classes = []
    authentication_classes = []

    # 获取用户已关联组别信息
    def get_user_related_groups(self, user_id, is_superuser):
        try:
            if not is_superuser:
                # 获取用户已关联组别ID
                related_group_id_list = SysUserGroup.objects.filter(user_id=user_id).values_list('group_id', flat=True)

                # 获取关联组别
                return SysGroup.objects.filter(id__in=related_group_id_list, is_delete=0).values('id', 'name')
            else: # 如果未超级用户，返回所有未删除的组
                return SysGroup.objects.filter(is_delete=0).values('id', 'name')
        except Exception as e:
            logger.error('获取用户关联组别信息出错：%s' % e)
            return []

    # 登录api
    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            account = data.get('account')

            user = User.objects.filter(Q(username=account) | Q(mobile=account) | Q(email=account) | Q(job_number=account)).filter(is_delete=0, is_active=1).first()
            if not user:
                result['msg'] =  '登录失败,用户不存在或者已被禁用'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)
            else:
                account = user.username

            password = data.get('password')
            captcha = data.get('captcha') # 图片验证码 # 暂时不做验证
            user = authenticate(request, username=account,password=password, is_delete=0) # 验证用户名和密码，返回用户对象
            if user is not None:
                login(request, user)   # 用户登陆
                # 更新Token
                try:
                    # 如果已经存在则删除
                    token = Token.objects.get(user=user)
                    token.delete()
                except Token.DoesNotExist as e:
                    pass

                refresh_token = RefreshToken.objects.filter(user_id=user.id).first()
                if refresh_token:
                    refresh_token.delete()

                token = Token.objects.create(user=user)

                refresh_token_key = str(token.user_id) + token.key
                refresh_token = RefreshToken(key=refresh_token_key, created=token.created, user_id=token.user_id)
                refresh_token.save()

                result['msg'] =  '登录成功'
                result['success'] =  True
                result['data'] =  {}
                # 获取用户关联的组别
                result['data']['userGroups'] = self.get_user_related_groups(user.id, user.is_superuser)
                # 获取用户权限标识
                try:
                    result['data']['perms'] = UserPermsView.get_user_perms(user.id, user.is_superuser)
                except Exception as e:
                    result['data']['perms'] = []
                    result['msg'] = '登录成功，但获取权限标识失败'
                result['data']['username'] = user.username
                result['data']['name'] = user.name
                result['data']['userId'] = user.id
                result['data']['token'] = token.key
                result['data']['refreshToken'] = refresh_token_key
                result['data']['isSuperuser'] = user.is_superuser
                # result['data']['userInfo'] = UserSerializer(user).data
                return Response(result, status.HTTP_200_OK)
            else:
                user = User.objects.filter(username=account).first()
                if user:
                    if not user.is_active:
                        result['msg'] =  '登录失败,用户已被禁用'
                        result['success'] =  False
                        return Response(result, status.HTTP_200_OK)
                    elif user.is_delete:
                        result['msg'] =  '登录失败,用户已删除'
                        result['success'] =  False
                        return Response(result, status.HTTP_200_OK)

                result['msg'] =  '登录失败,用户名或密码错误'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    '''
    退出系统
    '''

    def post(self, request, format=None):
        try:
            result = {}

            LogoutView.logout_user(request)
            result['msg'] = '退出成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def logout_user(request):
        user_id = request.user.id

        logout(request) # 删除会话

        # 删除Token
        token = Token.objects.filter(user_id=user_id).first()
        if token:
            cache.delete(token.key)
            token.delete()

        refresh_token = RefreshToken.objects.filter(user_id=user_id).first()
        if refresh_token:
            refresh_token.delete()


class UserPermsView(APIView):
    '''
    获取用户权限标识
   '''

    @staticmethod
    def get_user_perms(user_id, is_superuser):
        '''
        获取用户权限标识信息
        '''

        try:
            if is_superuser: # 如果为超级用户，获取全部标识
                # 通过角色ID获取用户已关联菜单ID
                perms = SysMenu.objects.filter(is_delete=0).values_list('perms', flat=True)
            else:
                # 获取用户已关联角色ID
                related_role_id_list = SysUserRole.objects.filter(user_id=user_id).values_list('role_id', flat=True)

                # 过滤已经删除，禁用的角色ID
                related_role_id_list = SysRole.objects.filter(id__in=related_role_id_list, is_delete=0, is_active=1).values_list('id', flat=True)

                # 通过角色ID获取用户已关联菜单ID
                related_menu_id_list = SysRoleMenu.objects.filter(role_id__in=related_role_id_list).values_list('menu_id', flat=True)

                related_menu_id_list = list(set(related_menu_id_list)) # 去重

                # 获取菜单权限标识
                perms = SysMenu.objects.filter(id__in=related_menu_id_list, is_delete=0).values_list('perms', flat=True)
            perms = list(set(perms))
            perms = [perm for perm in perms if perm]
            return perms
        except Exception as e:
            raise Exception('%s' % e)


    def get(self, request):
        try:
            result = {}
            user_id = request.user.id
            is_superuser = request.user.is_superuser

            result['data'] = UserPermsView.get_user_perms(user_id, is_superuser)
            result['msg'] = '获取用户权限标识成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '获取用户权限标识失败：%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



