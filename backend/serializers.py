#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from rest_framework import serializers

# 系统管理
from backend.models import User
from backend.models import SysMenu
from backend.models import SysRole
from backend.models import SysGroup
from backend.models import SysGroupRelatedGroup
from backend.models import SysUserAccount
from backend.models import Env
from backend.models import TestPhase
from backend.models import MsgPushAccount


# 产品视图
from backend.models import Product
from backend.models import Sprint

# 项目视图
from backend.models import Project
from backend.models import ProjectVersion
from backend.models import APIProjectGroup
from backend.models import APIProject
from backend.models import ProjectEnv

# 开发视图
from backend.models import APIGroup
from backend.models import ProjectAPI

# 测试视图-测试用例
from backend.models import TestcaseSuite
from backend.models import SprintTestcase
from backend.models import BaseTestcase
from backend.models import TestcaseAttachment

# 测试视图-测试计划管理
from backend.models import SprintTestplan
from backend.models import SprintTestplanTestcase
from backend.models import SprintTestplanTestcaseAttachment

# 测试视图-测试报告管理-迭代测试报告
from backend.models import SprintTestReport
# from backend.models import SprintTestReportTestPlan

# 度量 - 线上度量统计



from backend.models import TpadDefect

class UserSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(source='date_joined', format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    last_login_time = serializers.DateTimeField(source='last_login', format='%Y-%m-%d %H:%M:%S', required=False)
    account = serializers.CharField(source='username')

    class Meta:
        model = User
        exclude = ['username', 'last_login', 'first_name', 'last_name', 'user_permissions', 'groups', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}, 'is_delete':{'write_only':True},'is_staff':{'write_only':True}}
        read_only_fields = ['update_time', 'create_time', 'last_login_time']


class SysMenuSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = SysMenu
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time']

class SysRoleSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = SysRole
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time']


class SysGroupSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = SysGroup
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time']

class SysGroupRelatedGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysGroupRelatedGroup
        fields = '__all__'


class SysUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysUserAccount
        fields = '__all__'


class TestPhaseSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = TestPhase
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time']

class EnvSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Env
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time']

class MsgPushAccountSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = MsgPushAccount
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time']


class ProductSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time']



class SprintSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Sprint
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time']


class ProjectSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time']


class ProjectVersionSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    product = serializers.CharField(required=False)
    sprint = serializers.CharField(required=False)

    class Meta:
        model = ProjectVersion
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time', 'product', 'sprint']


class APIProjectGroupSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = APIProjectGroup
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time']

class APIGroupSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = APIGroup
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time']


class APIProjectSerializer(serializers.ModelSerializer):
    is_in_favorites = serializers.IntegerField(required=False)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = APIProject
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time', 'is_in_favorites']


class ProjectEnvSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    label = serializers.CharField(required=False)

    class Meta:
        model = ProjectEnv
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time']

class ProjectAPISerializer(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()   # 接口分类
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    def get_group_name(self, obj):
        group = APIGroup.objects.filter(id=obj.group_id).first()
        if group:
            return group.name
        else:
            return '--'

    class Meta:
        model = ProjectAPI
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time']


class TestcaseSuiteSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    editing = serializers.BooleanField(default=False, read_only=True)  # 返回是否正在编辑标识，方便前端处理

    class Meta:
        model = TestcaseSuite
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time', 'editing']

class SprintTestcaseSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = SprintTestcase
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time','suite_path', 'suite_type']

class BaseTestcaseSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = BaseTestcase
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}
        read_only_fields = ['create_time', 'update_time', 'suite_path', 'suite_type']


class TestcaseAttachmentSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    class Meta:
        model = TestcaseAttachment
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}, 'case_guid': {'write_only': True}, 'creater_id': {'write_only': True}, 'create_time': {'write_only': True}}
        read_only_fields = ['case_id', 'case_type', 'priority']

class SprintTestplanSerializer(serializers.ModelSerializer):
    begin_time = serializers.DateField(format='%Y-%m-%d', required=False)
    end_time = serializers.DateField(format='%Y-%m-%d', required=False)
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)
    finish_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',allow_null=True, required=False)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = SprintTestplan
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}}

class SprintTestplanTestcaseSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = SprintTestplanTestcase
        fields = '__all__'
        read_only_fields = ['fail_num',  'is_delete', 'children', 'suite_type', 'case_ids']

class TestplanTestcaseAttachmentSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    class Meta:
        model = SprintTestplanTestcaseAttachment
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True}, 'case_guid': {'write_only': True}, 'creater_id': {'write_only': True}, 'create_time': {'write_only': True}}
        read_only_fields = ['case_id', 'case_type', 'priority']

class SprintTestReportSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = SprintTestReport
        fields = '__all__'


# class SprintTestReportTestPlanSerializer(serializers.ModelSerializer):
#     start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)
#     finish_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)
#
#     class Meta:
#         model = SprintTestReportTestPlan
#         fields = '__all__'

class TpadDefectSerializer(serializers.ModelSerializer):
    # created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # resolved = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # closed = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # in_progress_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # verify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # reject_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # modified = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # begin = serializers.DateField(format='%Y-%m-%d', required=False)
    # due = serializers.DateField(format='%Y-%m-%d', required=False)
    # deadline = serializers.DateField(format='%Y-%m-%d', required=False)

    class Meta:
        model = TpadDefect
        fields = '__all__'


