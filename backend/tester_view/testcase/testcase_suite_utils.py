#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from backend.models import TestcaseSuite
from backend.models import SprintBaseCaseSuiteRelation
from backend.serializers import TestcaseSuiteSerializer
from django.db import transaction

import copy
import logging

logger = logging.getLogger('mylogger')

class TestSuiteStaticUtilsClass:
    @staticmethod
    def get_suite_path(suite_id, suite_path=""):
        '''获取套件路径'''
        obj = TestcaseSuite.objects.filter(id=suite_id).values('parent_id', 'name').first()
        if obj:
            suite_path = obj.get('name')
            parent_id = obj.get('parent_id')
            if parent_id != -1: # 存在上级测试套件
                suite_path = TestSuiteStaticUtilsClass.get_suite_path(parent_id, suite_path) + '/' + suite_path
        return suite_path

    @staticmethod
    def get_sub_suite_ids(suite_id, sub_suite_id_list=[]):
        '''获取子套件id'''
        sub_suites = TestcaseSuite.objects.filter(parent_id=suite_id, is_delete=0)
        if sub_suites.exists():
            for sub_suite in sub_suites:
                sub_suite_id_list.append(sub_suite.id)
                TestSuiteStaticUtilsClass.get_sub_suite_ids(sub_suite.id, sub_suite_id_list)
        return sub_suite_id_list

    @staticmethod
    def get_father_suite_ids(suite_id, suite_id_list=[]):
        '''获取所有上级套件id'''
        obj = TestcaseSuite.objects.filter(id=suite_id).values('parent_id', 'id').first()
        if obj:
            parent_id = obj.get('parent_id')
            if parent_id != -1: # 存在上级测试套件
                suite_id_list.append(parent_id)
                TestSuiteStaticUtilsClass.get_father_suite_ids(parent_id, suite_id_list)
        return suite_id_list




    @staticmethod
    def sync_sprint_suite_to_base_recursive(sprint_suite_data):
        '''
        递归同步迭代测试套件到基线测试套件
        '''

        ######## 获取当前测试套件及其父套件 ########
        sprint_suite_data_list = [] # 存放迭代测试套件及其祖先测试套件相关数据
        sprint_suite_data_list.append(sprint_suite_data)

        sprint_father_suite = TestcaseSuite.objects.filter(id=sprint_suite_data.get('parent_id')).first()
        while sprint_father_suite.parent_id != -1: # 根套件除外
            sprint_suite_data_list.append(TestcaseSuiteSerializer(sprint_father_suite).data)
            sprint_father_suite =  TestcaseSuite.objects.filter(id=sprint_father_suite.parent_id).first()

        ######## 创建基线测试套件 ########
        # 获取基线测试套件根套件
        base_father_suite = TestcaseSuite.objects.filter(type='base', is_delete=0, parent_id=-1, sprint_id=-1, product_id=sprint_suite_data.get('product_id')).first()

        base_suite_parent_id = None
        if base_father_suite:
            base_suite_parent_id = base_father_suite.id
            sprint_suite_list_len = len(sprint_suite_data_list)
            for i in range(0, sprint_suite_list_len):
                index = sprint_suite_list_len - i - 1

                sprint_suite_data = sprint_suite_data_list[index]
                base_suite_data = {'name':sprint_suite_data['name'], 'type':'base',
                                   'sprint_id':-1, 'product_id':sprint_suite_data['product_id'], 'parent_id':base_suite_parent_id,
                                   'creater_id':sprint_suite_data['creater_id'], 'updater_id':sprint_suite_data['updater_id'], 'is_delete':0}
                base_suite_parent_id = TestSuiteStaticUtilsClass.sync_sprint_suite_to_base_suite(sprint_suite_data['id'], base_suite_data)
        else:
            logger.warn('找不到基线测试集，同步递归创建基线测试套件失败')
        return base_suite_parent_id # 返回获取的最后层级套件的套件ID，即最新创建的基线套件id或者是基线根套件id

    @staticmethod
    def sync_sprint_suite_to_base_suite(sprint_suite_id, base_suite_data):
        '''同步迭代测试套件到基线测试套件'''

        # 判断上级基线套件下是否存在相同名称的测试套件
        sub_suite = TestcaseSuite.objects.filter(parent_id=base_suite_data['parent_id'], name=base_suite_data['name'], is_delete=0).first()
        if not sub_suite:# 不存在同名称的测试套件则新增，否则不新增
            all_upper_node_ids = TestSuiteStaticUtilsClass.get_father_suite_ids(base_suite_data['parent_id'], [base_suite_data['parent_id']])
            base_suite_data['all_upper_node_ids'] = ','.join([str(item) for item in all_upper_node_ids])
            base_suite_serializer = TestcaseSuiteSerializer(data=base_suite_data)
            base_suite_serializer.is_valid(raise_exception=True)
            base_suite_serializer.save()
            base_suite_id = base_suite_serializer.data.get('id')
        else:
            base_suite_id = sub_suite.id

        relation = SprintBaseCaseSuiteRelation.objects.filter(sprint_case_suite_id=sprint_suite_id).first()
        if relation:# 更新迭代测试套件和基线测试套件的关联关系
            relation.base_case_suite_id = base_suite_id
        else: # 添加迭代测试套件和基线测试套件的关联关系
            relation = SprintBaseCaseSuiteRelation(base_case_suite_id=base_suite_id, sprint_case_suite_id=sprint_suite_id)
        relation.save()
        return base_suite_id

    @staticmethod
    def create_testcase_suite(suite_data):
        ''' 创建测试用例套件 '''
        try:
            with transaction.atomic():
                serializer = TestcaseSuiteSerializer(data=suite_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                sprint_suite_id = serializer.data.get('id')

                if suite_data.get('type') == 'sprint':# 新增迭代测试套件 -> 需要新增迭代测试套件对应的基线测试套件
                    # 查找基线测试套件的上级套件id
                    sprint_base_suite_relation = SprintBaseCaseSuiteRelation.objects.filter(sprint_case_suite_id=suite_data.get('parent_id')).first()
                    if sprint_base_suite_relation:
                        # 获取基线测试套件的上级套件对象
                        base_father_suite = TestcaseSuite.objects.filter(id=sprint_base_suite_relation.base_case_suite_id, is_delete=0).first()
                        if base_father_suite: # 存在对应的基线上级套件对象
                            base_suite_data = copy.deepcopy(suite_data)
                            base_suite_data['type'] = 'base'
                            base_suite_data['parent_id'] = base_father_suite.id
                            base_suite_data['sprint_id'] = -1
                            all_upper_node_ids = TestSuiteStaticUtilsClass.get_father_suite_ids(base_suite_data['parent_id'], [base_suite_data['parent_id']])
                            base_suite_data['all_upper_node_ids'] = ','.join([str(item) for item in all_upper_node_ids])
                            TestSuiteStaticUtilsClass.sync_sprint_suite_to_base_suite(sprint_suite_id, base_suite_data)
                        else: # 不存在对应的上级套件对象，可能被软删除、物理删除
                            TestSuiteStaticUtilsClass.sync_sprint_suite_to_base_recursive(serializer.data)
                    else:
                        TestSuiteStaticUtilsClass.sync_sprint_suite_to_base_recursive(serializer.data)
        except Exception as e:
            raise Exception('%s' % e)
        return serializer.data


    @staticmethod
    def copy_base_suite_to_sprint_by_structure(base_suite_id, product_id, sprint_id, creater_id):
        '''
        向上拷贝基线套件到指定迭代
        '''

        sprint_root_suite = TestcaseSuite.objects.filter(type='sprint', parent_id=-1, sprint_id=sprint_id, product_id=product_id, is_delete=0).first()
        all_base_node_id_list = TestSuiteStaticUtilsClass.get_father_suite_ids(base_suite_id, [base_suite_id]) # all_base_node_id_list 为有序列表，按索引顺序从前往后，分别是当前基线套件id，上级套件id，。。。，根套件id
        if sprint_root_suite:
            sprint_suite_id = sprint_root_suite.id
            suite_num_need_to_copy = len(all_base_node_id_list) - 1
            all_upper_node_ids = str(sprint_suite_id)

            for i in range(0, suite_num_need_to_copy):
                base_suite_id = all_base_node_id_list[suite_num_need_to_copy-i-1]
                base_suite = TestcaseSuite.objects.filter(id=base_suite_id, is_delete=0).first()
                if base_suite:
                    sprint_suite_obj = TestcaseSuite.objects.filter(name=base_suite.name, parent_id=sprint_suite_id, is_delete=0).first()
                    if sprint_suite_obj:
                        sprint_suite_id = sprint_suite_obj.id
                    else:
                        new_sprint_suite = {'name': base_suite.name,
                                            'type': 'sprint',
                                            'parent_id': sprint_suite_id,
                                            'sprint_id': sprint_id,
                                            'product_id':product_id,
                                            'creater_id': creater_id,
                                            'updater_id':creater_id,
                                            'is_delete':0,
                                            'all_upper_node_ids':all_upper_node_ids
                                            }

                        suite_serializer = TestcaseSuiteSerializer(data=new_sprint_suite)
                        suite_serializer.is_valid(raise_exception=True)
                        suite_serializer.save()
                        sprint_suite_id = suite_serializer.data.get('id')

                         # 添加基线套件和迭代测试套件的绑定关系
                        relation = SprintBaseCaseSuiteRelation(base_case_suite_id=base_suite.id, sprint_case_suite_id=sprint_suite_id)
                        relation.save()

                    all_upper_node_ids = str(sprint_suite_id) +  "," + all_upper_node_ids
        else:# 迭代根测试套件不存在
            raise Exception("迭代根测试集不存在")

    @staticmethod
    def get_root_suite_info_by_name_for_product(root_suite_name, product_id):
        '''根据根套件名称查询套件信息'''

        # 查找迭代根测试套件是否存在和 root_suite_name 同名的测试套件
        sprint_root_suite = TestcaseSuite.objects.filter(name=root_suite_name, type='sprint', parent_id=-1, is_delete=0, all_upper_node_ids=-1, product_id=product_id).first()
        if sprint_root_suite:
            parent_suite_id = sprint_root_suite.id
            parent_suite_type = sprint_root_suite.type
            parent_suite_sprint_id = sprint_root_suite.sprint_id
            parent_suite_product_id = sprint_root_suite.product_id
            root_suite_info = {'type': parent_suite_type , 'id':parent_suite_id, 'sprint_id':parent_suite_sprint_id, 'product_id':parent_suite_product_id}
        else:
            # 查找基线根测试套件是否存在和 root_suite_name 同名的测试套件
            base_root_suite = TestcaseSuite.objects.filter(name=root_suite_name, type='base', parent_id=-1, is_delete=0, sprint_id=-1, all_upper_node_ids=-1,  product_id=product_id).first()
            if base_root_suite:
                parent_suite_id = base_root_suite.id
                parent_suite_type = base_root_suite.type
                parent_suite_sprint_id = base_root_suite.sprint_id
                parent_suite_product_id = base_root_suite.product_id
                root_suite_info = {'type': parent_suite_type , 'id':parent_suite_id, 'sprint_id':parent_suite_sprint_id, 'product_id':parent_suite_product_id}
            else:
                return {'success':False, 'reason':'用例所在根套件"%s"不存在' % root_suite_name}
        return {'success':True, 'root_suite_info':root_suite_info}

    @staticmethod
    def create_testsuite(suite_info):
        '''创建测试套件'''

        # 查找父级测试套件下是否已存在相同名称的测试套件
        parent_suite_id = suite_info['parent_id']
        sub_suite = TestcaseSuite.objects.filter(parent_id=parent_suite_id, name=suite_info['name'], is_delete=0).first()
        if sub_suite: # 已存在,更新
            serializer = TestcaseSuiteSerializer(sub_suite, data=suite_info)
            serializer.is_valid(raise_exception=True)
        else: # 不存在，新建
            all_upper_node_ids = TestSuiteStaticUtilsClass.get_father_suite_ids(parent_suite_id, [parent_suite_id])
            suite_info['all_upper_node_ids'] = ','.join([str(item) for item in all_upper_node_ids])
            serializer = TestcaseSuiteSerializer(data=suite_info)
            serializer.is_valid(raise_exception=True)
        serializer.save()
        suite_id = serializer.data.get('id')
        return suite_id


    @staticmethod
    def create_sub_testsuite_by_path(case_path, type, root_suite_id, sprint_id, product_id, creater_id):
        # 遍历用例路径中的每个测试套件，并检查套件是否存在，如果不存在，则创建测试套件
        all_upper_node_ids = [] # 存放待创建测试套件所有父辈套件id
        suite_name_list = case_path.split('/')
        parent_suite_id = root_suite_id
        for suite_name in suite_name_list[1:]:
            all_upper_node_ids.append(parent_suite_id)
            suite_info = {'name': suite_name, 'type': type, 'parent_id':parent_suite_id, 'sprint_id':sprint_id, 'product_id':product_id,
                          'creater_id':creater_id, 'updater_id':creater_id, 'is_delete':0, 'all_upper_node_ids':','.join([str(item) for item in all_upper_node_ids])}

            try:
                with transaction.atomic():
                    if type == 'sprint':# 新增迭代测试套件 -> 需要新增迭代测试套件对应的基线测试套件
                        base_suite_data = copy.deepcopy(suite_info)
                        base_suite_data['type'] = 'base'
                        base_suite_data['sprint_id'] = -1

                        # 获取基线待新增测试套件所在的父级套件
                        relation = SprintBaseCaseSuiteRelation.objects.filter(sprint_case_suite_id=parent_suite_id).first()
                        if relation:
                            base_father_suite = TestcaseSuite.objects.filter(id=relation.base_case_suite_id, is_delete=0).first()
                        else:
                            sprint_father_suite = TestcaseSuite.objects.filter(id=parent_suite_id).first()
                            if sprint_father_suite.parent_id == -1:
                                base_father_suite = TestcaseSuite.objects.filter(type='base', is_delete=0, product_id=product_id, parent_id=-1, sprint_id=-1).first()
                            else: # 找不到迭代套件关联的基线套件（创建迭代测试套件会自动新增和基线套件的关联关系，删除套件时会自动删除关系，所以，找不到关系的情况下，如果迭代套件为非根套件，
                                #那一定是极端事件，非正常操作，设置对应的基线套件为None,即不创建对应套件）
                                base_father_suite = None
                        parent_suite_id = TestSuiteStaticUtilsClass.create_testsuite(suite_info)
                        if base_father_suite:
                            base_suite_data['parent_id'] = base_father_suite.id
                            temp_all_upper_node_ids = TestSuiteStaticUtilsClass.get_father_suite_ids(base_father_suite.id, [base_father_suite.id])
                            temp_all_upper_node_ids = ','.join([str(item) for item in temp_all_upper_node_ids])
                            base_suite_data['all_upper_node_ids'] = temp_all_upper_node_ids
                            base_suite_id = TestSuiteStaticUtilsClass.create_testsuite(base_suite_data)

                            # 更新迭代套件和基线套件的映射关系
                            sprint_base_suite_relation = SprintBaseCaseSuiteRelation.objects.filter(sprint_case_suite_id=parent_suite_id).first()
                            if sprint_base_suite_relation:
                                sprint_base_suite_relation.base_case_suite_id = base_suite_id
                                sprint_base_suite_relation.save()
                            else:
                                SprintBaseCaseSuiteRelation(sprint_case_suite_id=parent_suite_id, base_case_suite_id=base_suite_id).save()
                    elif type == 'base':
                        parent_suite_id = TestSuiteStaticUtilsClass.create_testsuite(suite_info)
            except Exception as e:
                fail_desc = '创建测试套件(%s)失败：%s' % (suite_name, e)
                return {'success':False, 'reason':fail_desc}
        return {'success':True, 'tail_suite_id':parent_suite_id }  # tail_suite_id 最后层级测试套件id