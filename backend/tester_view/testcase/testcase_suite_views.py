#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import copy
import shortuuid
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from backend.models import TestcaseSuite
from backend.models import SprintBaseCaseSuiteRelation
from backend.models import BaseTestcase
from backend.models import SprintTestcase
from backend.models import SprintTestplanTestcase
from backend.serializers import TestcaseSuiteSerializer
from backend.serializers import SprintTestcaseSerializer
from backend.serializers import BaseTestcaseSerializer
from backend.tester_view.testcase.testcase_views import TestcaseAPIUtils
from backend.tester_view.testcase.testcase_suite_utils import TestSuiteStaticUtilsClass


logger = logging.getLogger('mylogger')

class TestcaseSuitTreeAPIView(APIView):
    '''
    测试视图-测试用例管理，测试用例套件树
    '''
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            sprint_id = params.get('sprintId')
            product_id = params.get('productId')
            plan_id = params.get('planId')
            parent_id = params.get('parentId')
            recursive = int(params.get('recursive')) # 是否递归查找子测试套件
            sort = params.get('sort')
            level = params.get('level') # 套件级别
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            temp_upper_suite_id_list = [] # 临时存放用例关联套件所在的所有父级套件
            testplan_case_suite_id_list = [] # 存放计划关联用例所关联的套件自身ID
            if plan_id:
                # 获取测试计划关联用例的套件
                testplan_case_suite_id_list = list(set(SprintTestplanTestcase.objects.filter(testplan_id = plan_id).values_list('suite_id', flat=True)))
                if testplan_case_suite_id_list:
                    # 查找测试计划用例关联用例套件的父辈套件
                    upper_suite_id_list = TestcaseSuite.objects.filter(id__in=testplan_case_suite_id_list).values_list('all_upper_node_ids', flat=True)
                    upper_suite_id_list = list(set(upper_suite_id_list))

                    for item in upper_suite_id_list:
                        temp_upper_suite_id_list.extend(item.split(','))
                    temp_upper_suite_id_list = list(set(temp_upper_suite_id_list))
                    temp_upper_suite_id_list = [int(item) for item in temp_upper_suite_id_list]
                else:
                    result['msg'] =  '未获取到测试用例关联套件ID'
                    result['success'] =  True
                    result['data'] = []
                    return Response(result, status.HTTP_200_OK)

                testplan_case_suite_id_list.extend(temp_upper_suite_id_list)
                testplan_case_suite_id_list = list(set(testplan_case_suite_id_list))

                filters = {'parent_id':parent_id, 'product_id':product_id}
            else:
                filters = {'parent_id':parent_id, 'product_id':product_id, 'is_delete':0}

            if level == 'topSuite': # 加载顶级套件
                if sprint_id == '':
                    filters['sprint_id'] = -1
                else:
                    filters['sprint_id__in'] = [sprint_id, -1]

            def get_sub_suites(resource):
                '''
                获取子套件
                '''
                parent_id = resource['id']   # 获取上级套件id

                if plan_id:
                    filters = {'parent_id':parent_id, 'product_id':product_id}
                else:
                    filters = {'parent_id':parent_id, 'product_id':product_id, 'is_delete':0}
                sub_suites = TestcaseSuite.objects.filter(**filters).order_by(*sort_list)
                sub_suites = TestcaseSuiteSerializer(sub_suites, many=True).data
                resource['children'] = sub_suites
                if sub_suites: #如果存在子级套件，遍历添加子级套件
                    resource['children'] = sub_suites
                    sub_suites_copy = copy.deepcopy(sub_suites)
                    for sub_suite in sub_suites_copy:
                        if plan_id and sub_suite['id'] not in testplan_case_suite_id_list:
                            sub_suites.remove(sub_suite)
                            continue
                        get_sub_suites(sub_suite)

            # 获取指定parent_id的直接子套件
            father_suites = TestcaseSuite.objects.filter(**filters).order_by(*sort_list)
            father_suites = TestcaseSuiteSerializer(father_suites, many=True).data
            tree_nodes_list = father_suites

            if recursive: # 遍历子级套件
                for father_suite in tree_nodes_list:
                    get_sub_suites(father_suite) # 获取子级套件
            else:
                father_suites_copy = copy.deepcopy(father_suites)
                for father_suite in father_suites_copy:
                    if plan_id and father_suite['id'] not in testplan_case_suite_id_list:
                        tree_nodes_list.remove(father_suite)
                        continue
                    father_suite['children'] = []
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = tree_nodes_list
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestcaseSuitAPIView(APIView):
    '''
    测试视图-测试用例管理-测试套件树，新增测试套件
    '''

    # 新增测试套件
    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['creater_id'] = request.user.id
            data['updater_id'] = data['creater_id']
            data['is_delete'] = False
            data['name'] = '新建测试集'
            product_id = data.get('product_id')
            data['product_id'] = product_id
            sprint_id = data.get('sprint_id')
            data['sprint_id'] = sprint_id
            # 查找父级测试套件下是否已存在相同名称的测试套件
            parent_suite_id = data.get('parent_id')
            sub_suites = TestcaseSuite.objects.filter(parent_id=parent_suite_id, name=data['name'], is_delete=0)
            if sub_suites.exists():
                result['msg'] =  '新增失败：当前测试集下已存在相同名称的子测试集'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            # 创建套件
            # all_upper_node_ids = TestSuiteStaticUtilsClass.get_father_suite_ids(parent_suite_id, [parent_suite_id])
            # data['all_upper_node_ids'] = ','.join([str(item) for item in all_upper_node_ids])

            obj = TestcaseSuite.objects.filter(id=parent_suite_id).first()
            if not obj:
                result['msg'] =  '上级套件不存在'
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            all_upper_node_ids = obj.all_upper_node_ids.split(',')
            if '-1' in all_upper_node_ids:
                all_upper_node_ids.remove('-1')
            all_upper_node_ids.append(str(parent_suite_id))

            data['all_upper_node_ids'] = ','.join(all_upper_node_ids)
            suite_data = TestSuiteStaticUtilsClass.create_testcase_suite(data)

            result['msg'] =  '新增成功'
            result['success'] =  True
            data = copy.deepcopy(suite_data)
            data['editing'] = True
            data['children'] = []
            result['data'] =  data
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 修改测试套件
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['updater_id'] = request.user.id

            suite_id = data.get('suite_id')
            type = data.get('type')
            del data['suite_id']
            del data['type']

            obj = TestcaseSuite.objects.filter(id=suite_id, is_delete=0).first()
            if obj:
                try:
                    # 查找父级测试套件下是否已存在相同名称的测试套件
                    sub_suites = TestcaseSuite.objects.filter(parent_id=obj.parent_id, name=data['name'], is_delete=0).exclude(id=obj.id)
                    if sub_suites.exists():
                        result['msg'] =  '修改失败：当前测试集下已存在同名子测试集'
                        result['success'] =  False
                        return Response(result, status.HTTP_200_OK)

                    with transaction.atomic():
                        name_old = obj.name
                        serializer = TestcaseSuiteSerializer(obj, data=data, partial=True)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()

                        if type == 'sprint': # 需要修改对应基线测试套件
                            sprint_base_suite_relation = SprintBaseCaseSuiteRelation.objects.filter(sprint_case_suite_id=obj.id).first()
                            if sprint_base_suite_relation:
                                # 获取关联的基线测试套件
                                base_suite = TestcaseSuite.objects.filter(id=sprint_base_suite_relation.base_case_suite_id, is_delete=0).first()
                                if base_suite:
                                    # 判断基线套件所在上级套件下是否存在和目标名称相同的子测试集
                                    sub_suites = TestcaseSuite.objects.exclude(id=base_suite.id).filter(parent_id=base_suite.parent_id, name=data['name'], is_delete=0)
                                    if sub_suites.exists():
                                        old_base_case_suite_id = sprint_base_suite_relation.base_case_suite_id
                                        # 更新迭代测试套件和基线测试套件的关联关系
                                        base_suite_id = sub_suites.first().id
                                        sprint_base_suite_relation.base_case_suite_id = base_suite_id
                                        sprint_base_suite_relation.save()

                                        # 合并用例到名为目标名称的基线测试套件下
                                        BaseTestcase.objects.filter(suite_id=old_base_case_suite_id).update(suite_id=base_suite_id)
                                    else:
                                        serializer = TestcaseSuiteSerializer(base_suite, data=data, partial=True)
                                        serializer.is_valid(raise_exception=True)
                                        serializer.save()
                            else: # 检查被修改迭代测试套件所在上级套件关联的基线套件下是否存在同名测试集
                                sprint_base_suite_relation = SprintBaseCaseSuiteRelation.objects.filter(sprint_case_suite_id=obj.parent_id).first()
                                if sprint_base_suite_relation:
                                    # 获取关联的基线测试套件
                                    base_father_suite = TestcaseSuite.objects.filter(id=sprint_base_suite_relation.base_case_suite_id, is_delete=0).first()
                                else:
                                    # 判断被修改迭代测试套件所在上级是否是根测试套件
                                    sprint_parent_suite =  TestcaseSuite.objects.filter(id=obj.parent_id, is_delete=0).first()
                                    if sprint_parent_suite and sprint_parent_suite.parent_id == -1: # 迭代套件所在上级套件为根套件， 基线测试套件默认为根套件
                                        product_id = sprint_parent_suite.product_id
                                        base_father_suite = TestcaseSuite.objects.filter(type='base', is_delete=0, product_id=product_id, parent_id=-1, sprint_id=-1).first()
                                    else:# 迭代套件所在上级套件不存在，或者不为根套件，修改的是中间层的测试套件，但是对应的基线测试套件不存在，可能被删除了，不做同步
                                        base_father_suite = None
                                if base_father_suite:
                                    # 检查被修改迭代测试套件所在上级套件关联的基线套件下是否存在同名，但是未关联迭代的测试集
                                    sub_suite = TestcaseSuite.objects.filter(parent_id=base_father_suite.id, name=data['name'], is_delete=0).first()
                                    if sub_suite:# 存在和迭代测试套件修改后同名基线套件
                                        pass
                                    else: # 判断是否存在和迭代测试套件修改前同名基线套件
                                        sub_suite = TestcaseSuite.objects.filter(parent_id=base_father_suite.id, name=name_old, is_delete=0).first()
                                        if sub_suite:
                                            sub_suite.name = data['name']
                                            sub_suite.save()
                                        else:
                                            sub_suite = None
                                    if sub_suite: # 如果找到和测试套件修改前、修改后同名基线套件，则建立映射关系
                                        relation = SprintBaseCaseSuiteRelation.objects.filter(sprint_case_suite_id=obj.id).first()
                                        if relation:# 更新迭代测试套件和基线测试套件的关联关系
                                            relation.base_case_suite_id = sub_suite.id
                                        else: # 添加迭代测试套件和基线测试套件的关联关系
                                            relation = SprintBaseCaseSuiteRelation(base_case_suite_id=sub_suite.id, sprint_case_suite_id=obj.id)
                                        relation.save()
                except Exception as e:
                    result['msg'] =  '操作失败：%s' % e
                    result['success'] =  False
                    return Response(result, status.HTTP_400_BAD_REQUEST)
            else:
                result['msg'] = '操作失败，测试集不存在'
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

    # 删除测试套件
    def delete(self, request, format=None):
        # def delete_sub_suite(parent_id):
        #     sub_suites = TestcaseSuite.objects.filter(parent_id=parent_id, is_delete=0)
        #     if sub_suites.exists():
        #         for sub_suite in sub_suites:
        #             sub_suite.is_delete = 1
        #             sub_suite.save()
        #             # 删除关系
        #             SprintBaseCaseSuiteRelation.objects.filter(base_case_suite_id=sub_suite.id).delete()
        #
        #             delete_sub_suite(sub_suite.id)

        result = {}
        try:
            data = request.data
            suite_id = data.get('suite_id')
            type = data.get('type')
            # 是否删除对应的基线测试套件 字符串类型 1 为级联删除 否则不删除
            del_base_suites_cascade = data.get('del_base_suites_cascade')


            if type == 'base':
                case_model_table = 'BaseTestcase'
            else:
                case_model_table = 'SprintTestcase'

            # 获取子测试套件id
            query_sql = 'SELECT id FROM tb_testcase_suite AS t ' \
                        'WHERE MATCH(all_upper_node_ids) AGAINST (%s IN BOOLEAN MODE) AND is_delete=0' % suite_id

            query_result = TestcaseSuite.objects.raw(query_sql)
            suite_id_list = []
            for item in query_result:
                suite_id_list.append(int(item.id))
            suite_id_list.append(suite_id)

            if globals()[case_model_table].objects.filter(suite_id__in=suite_id_list, is_delete=0).exists():
                result['msg'] =  '删除失败，请先删除该测试集体下的所有测试用例'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            with transaction.atomic():
                TestcaseSuite.objects.filter(id__in=suite_id_list).update(is_delete = 1)
                if type == "sprint":
                    if del_base_suites_cascade == '1':
                        # 获取迭代套件对应的基线套件id
                        relation = SprintBaseCaseSuiteRelation.objects.filter(sprint_case_suite_id=suite_id)
                        if relation.exists():
                            base_suite_id = relation.first().base_case_suite_id

                            # 获取子测试套件id
                            query_sql = 'SELECT id FROM tb_testcase_suite AS t ' \
                                        'WHERE MATCH(all_upper_node_ids) AGAINST (%s IN BOOLEAN MODE) AND is_delete=0' % int(base_suite_id)
                            query_result = TestcaseSuite.objects.raw(query_sql)
                            base_suite_id_list = []
                            for item in query_result:
                                base_suite_id_list.append(int(item.id))

                            # 获取被用例引用的套件id
                            base_suite_id_list.append(base_suite_id)
                            base_cases = BaseTestcase.objects.filter(suite_id__in=base_suite_id_list, is_delete=0)
                            if base_cases.exists():
                                temp_base_suite_id_list = base_cases.values_list('suite_id', flat=True)
                                temp_base_suite_id_list.reverse()
                                suite_id_list_cannot_be_delete = set()
                                for suite_id in temp_base_suite_id_list:
                                    if suite_id not in suite_id_list_cannot_be_delete:# 如果 suite_id 存在 suite_id_list_cannot_be_delete，说明该suite的上级id也包含则里面了
                                        suite_obj = TestcaseSuite.objects.filter(id=suite_id).first()
                                        if suite_obj:
                                            temp_list = suite_obj.all_upper_node_ids.split(',')
                                            for item in temp_list:
                                                suite_id_list_cannot_be_delete.add(int(item))
                                            suite_id_list_cannot_be_delete.add(suite_id)
                                suite_id_list_can_be_delete =  set(base_suite_id_list) - suite_id_list_cannot_be_delete
                                TestcaseSuite.objects.filter(id__in=suite_id_list_can_be_delete).update(is_delete=1)
                            else:
                                TestcaseSuite.objects.filter(id__in=base_suite_id_list).update(is_delete=1)
                        else:
                            pass
                    else:
                        pass
                    SprintBaseCaseSuiteRelation.objects.filter(sprint_case_suite_id__in=suite_id_list).delete()
                else:
                    SprintBaseCaseSuiteRelation.objects.filter(base_case_suite_id__in=suite_id_list).delete()
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



class PasteTestcasesCopiedAPIView(APIView):
    '''
    测试视图-测试用例管理，黏贴拷贝的用例到目标测试套件下
    '''

    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            creater_id = request.user.id
            creater_name = request.user.name
            suite_id = data.get('suite_id')
            testcases = data.get('testcases') # 直接使用前端发来的数据，不走数据库

            target_suite = TestcaseSuite.objects.filter(id=suite_id, is_delete=0).first()
            if target_suite:
                # 遍历测试用例
                for testcase in testcases:
                    target_suite_type = target_suite.type
                    suite_type = testcase['suite_type']
                    target_suite_sprint_id = -1
                    if suite_type == 'base' and target_suite_type=='sprint':
                        testcase_serializer = 'SprintTestcaseSerializer'
                        copy_direction = 'base_to_sprint' # 拷贝方向,供复制用例步骤使用
                        target_suite_sprint_id = target_suite.sprint_id
                    elif suite_type == 'base' and target_suite_type == 'base':
                        copy_direction = 'base_to_base'
                        testcase_serializer = 'BaseTestcaseSerializer'
                    elif suite_type == 'sprint' and target_suite_type == 'sprint':
                        copy_direction = 'sprint_to_sprint'
                        target_suite_sprint_id = target_suite.sprint_id
                        testcase_serializer = 'SprintTestcaseSerializer'
                    elif suite_type == 'sprint' and target_suite_type == 'base':
                        copy_direction = 'sprint_to_base'
                        testcase_serializer = 'BaseTestcaseSerializer'
                    else:
                        result['msg'] =  '用例(guid:%s， 标题：%s)黏贴失败，类型错误：%s' % (testcase['guid'], testcase['name'], suite_type)
                        result['success'] =  False
                        return Response(result, status.HTTP_400_BAD_REQUEST)

                    new_testcase = {}
                    new_testcase['guid'] = shortuuid.uuid()
                    new_testcase['custom_no'] = None
                    new_testcase['suite_id'] = target_suite.id
                    new_testcase['sprint_id'] = target_suite_sprint_id
                    new_testcase['product_id'] = testcase['product_id']
                    new_testcase['name'] = testcase['name']
                    new_testcase['priority'] = testcase['priority']
                    new_testcase['execution_phase'] = ','.join(testcase['execution_phase'])
                    new_testcase['execution_method'] = testcase['execution_method']
                    new_testcase['executed_each_sprint'] = testcase['executed_each_sprint']
                    new_testcase['tags'] = ','.join(testcase['tags'])
                    new_testcase['desc'] = testcase['desc']
                    new_testcase['precondition'] = testcase['precondition']
                    new_testcase['steps'] = testcase['steps']
                    new_testcase['postcondition'] = testcase['postcondition']
                    new_testcase['creater_id'] = creater_id
                    new_testcase['creater_name'] = creater_name
                    new_testcase['updater_id'] = creater_id
                    new_testcase['updater_name'] = creater_name
                    new_testcase['is_delete'] = 0

                    # 创建测试用例
                    try:
                        serializer = globals()[testcase_serializer](data=new_testcase)
                        serializer.is_valid(raise_exception=True)
                        with transaction.atomic():
                            serializer.save()
                            # to_case_id = serializer.data.get('id')
                            to_case_guid = serializer.data.get('guid')
                            src_case_guid = testcase['guid']

                            # 拷贝源用例的测试附件到新建测试用例下
                            TestcaseAPIUtils.copy_case_attachments(to_case_guid, src_case_guid, copy_direction)

                            if copy_direction == 'base_to_sprint': # 更新对应的基线用例
                                # 修改基线测试用例关联的迭代测试用例guid和迭代id
                                base_case = BaseTestcase.objects.filter(guid=src_case_guid, is_delete=0).first()
                                if base_case:
                                    base_case.sprint_testcase_guid = to_case_guid
                                    base_case.sprint_id = target_suite_sprint_id
                                    base_case.save()
                                else:
                                    # 小概率事件，被复制的基线用例被删除，啥也不做，
                                    pass
                            elif copy_direction == 'sprint_to_sprint': # 同步创建基线测试用例
                                TestcaseAPIUtils.sync_sprint_case_to_base(to_case_guid, target_suite.id, new_testcase)
                    except Exception as e:
                        result['msg'] =  '用例(名称：%s)黏贴失败：%s' % (testcase['name'],e)
                        result['success'] =  False
                        return Response(result, status.HTTP_400_BAD_REQUEST)
            else:
                result['msg'] =  '黏贴失败，当前测试集不存在或者已被删除'
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)
            result['msg'] =  '黏贴成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



class PasteTestcasesCutAPIView(APIView):
    '''
    测试视图-测试用例管理，黏贴剪切的用例到目标测试套件下
    '''

    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            suite_id = data.get('suite_id')
            product_id = data.get('product_id')
            testcases = data.get('testcases') # 直接使用前端发来的数据，不走数据库

            target_suite = TestcaseSuite.objects.filter(id=suite_id, is_delete=0).first()
            if target_suite:
                # 遍历测试用例
                for testcase in testcases:
                    target_suite_type = target_suite.type
                    suite_type = testcase['suite_type']
                    if suite_type != target_suite_type: # 自动跳过和目标套件类型不一样的用例
                        continue

                    if target_suite_type == 'base':
                        testcase_mode = 'BaseTestcase'
                    elif target_suite_type == 'sprint':
                        testcase_mode = 'SprintTestcase'
                    else:# 非常小概率事件
                        result['msg'] =  '用例(guid:%s， 标题：%s)黏贴失败，类型错误：%s' % (testcase['guid'], testcase['name'], suite_type)
                        result['success'] =  False
                        return Response(result, status.HTTP_400_BAD_REQUEST)

                    # 更新测试用例
                    testcase_obj = globals()[testcase_mode].objects.filter(guid=testcase['guid'], is_delete=0).first()
                    if testcase_obj:
                        with transaction.atomic():
                            testcase_obj.suite_id = target_suite.id
                            testcase_obj.save()

                            # 如果被剪切的是迭代用例
                            if target_suite_type == 'sprint':
                                # 查找目标测试套件关联的基线测试套件
                                relation = SprintBaseCaseSuiteRelation.objects.filter(sprint_case_suite_id=target_suite.id).first()

                                base_suite = None
                                base_suite_id = None
                                if relation: # 如果存在关系，就一定存在对应套件，因为删除套件时会自动删除关系
                                    base_suite = TestcaseSuite.objects.filter(id=relation.base_case_suite_id).first()
                                else: # 判断目标测试套件是否为根套件，如果是则默认关联的基线测试套件为根套件
                                    if target_suite.parent_id == -1: # 目标测试套件为根测试套件，则默认同步创建的基线用例挂载的基线测试套件为根测试套件
                                        base_suite =  TestcaseSuite.objects.filter(type='base', is_delete=0, product_id=product_id, parent_id=-1, sprint_id=-1).first()
                                    else: # 递归创建基线对应的基线测试套件
                                        base_suite_id = TestSuiteStaticUtilsClass.sync_sprint_suite_to_base_recursive(TestcaseSuiteSerializer(target_suite).data)

                                if base_suite:
                                    base_suite_id = base_suite.id

                                if base_suite_id:
                                    # 查找迭代用例对应的基线用例,更新所在测试集
                                    base_testcase_obj = BaseTestcase.objects.filter(sprint_testcase_guid=testcase_obj.guid, is_delete=0).first()
                                    if base_testcase_obj:
                                        base_testcase_obj.suite_id = base_suite_id
                                        base_testcase_obj.save()
                                else:
                                    pass

                    else:# 用例不存在,啥也不做
                        continue
            else:
                result['msg'] =  '黏贴失败，当前测试集不存在或者已被删除'
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)
            result['msg'] =  '黏贴成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasteSuiteByStructureAPIView(APIView):
    '''黏贴按结构复制的基线测试集'''

    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            base_suite_id = data.get('base_suite_id')
            product_id = data.get('product_id')
            sprint_id = data.get('sprint_id')
            create_id = request.user.id

            try:
                TestSuiteStaticUtilsClass.copy_base_suite_to_sprint_by_structure(base_suite_id, product_id, sprint_id, create_id)
            except Exception as e:
                result['msg'] =  '黏贴失败:%s' % e
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)
            result['msg'] =  '黏贴成功,请右键目标节点刷新后查看'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasteSuiteCutAPIView(APIView):
    '''黏贴剪切的测试集'''

    @staticmethod
    def update_sub_suites(suite_id, src_upper_suite_ids_set, src_upper_suite_ids_new):
        '''更改子测试套件信息：所有上级结点id'''
        sub_suites = TestcaseSuite.objects.filter(parent_id=suite_id)
        if sub_suites.exists():
            for sub_suite in sub_suites:
                sub_suite_upper_suite_ids = sub_suite.all_upper_node_ids.replace(' ', '').split(',')
                sub_suite_upper_suite_ids_set = set([item for item in sub_suite_upper_suite_ids])
                sub_suite_upper_suite_ids_set = sub_suite_upper_suite_ids_set - src_upper_suite_ids_set
                sub_suite_upper_suite_ids = ','.join(list(sub_suite_upper_suite_ids_set)) + ',' + src_upper_suite_ids_new
                sub_suite_upper_suite_ids = sub_suite_upper_suite_ids.strip(',')
                sub_suites.update(all_upper_node_ids = sub_suite_upper_suite_ids)
                PasteSuiteCutAPIView.update_sub_suites(sub_suite.id, src_upper_suite_ids_set, src_upper_suite_ids_new)

    def post(self, request, format=None):
        '''黏贴被剪切的测试套件，注意：不支持跟套件剪切，前台做了控制，这里未做控制'''

        result = {}
        try:
            data = request.data
            src_suite_id = data.get('suite_id')
            target_suite_id = data.get('target_suite_id')
            src_suite_type = data.get('src_suite_type')
            target_suite_type = data.get('target_suite_type')
            product_id = data.get('product_id')
            update_id = request.user.id
            result['data'] = {'relatedTargetSuite':None, 'relatedSrcSuite':None}

            if src_suite_type not in ['sprint', 'base']:
                result['msg'] =  '黏贴失败：仅支持基线和迭代测试集'
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            if src_suite_id == target_suite_id:
                result['msg'] =  '黏贴失败：不能黏贴到被剪切的测试集'
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)
            if src_suite_type != target_suite_type:
                result['msg'] =  '黏贴失败：只能能黏贴到同类型的测试集'
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)
            src_suite = TestcaseSuite.objects.filter(id=src_suite_id, is_delete=0).first()
            if src_suite:
                # 查找待黏贴至目标测试套件
                target_suite = TestcaseSuite.objects.filter(id=target_suite_id, is_delete=0).first()
                if not target_suite:
                    result['msg'] =  '黏贴失败：目标测试集不存在'
                    result['success'] =  False
                    return Response(result, status.HTTP_200_OK)

                # 查找待黏贴至目标测试套件下是否已存在同名测试套件
                temp_suite = TestcaseSuite.objects.filter(parent_id=target_suite_id, name=src_suite.name, is_delete=0).first()
                if temp_suite:
                    result['msg'] =  '黏贴失败：该测试集下已存在同名测试集'
                    result['success'] =  False
                    return Response(result, status.HTTP_200_OK)

                # 记录待黏贴至目标测试套件所有上级套件id
                target_upper_suite_ids = target_suite.all_upper_node_ids.split(',')
                if '-1' in target_upper_suite_ids:
                    target_upper_suite_ids.remove('-1')

                # 记录被剪切套件所有上级套件id
                src_upper_suite_ids_old = src_suite.all_upper_node_ids.replace(' ', '').split(',')
                if '-1' in src_upper_suite_ids_old:
                    src_upper_suite_ids_old.remove('-1')
                src_upper_suite_ids_old_set = set([item for item in src_upper_suite_ids_old])

                # 获取被剪切测试套件黏贴后的所有上级套件id
                src_upper_suite_ids_new = ','.join(target_upper_suite_ids) + ',' + str(target_suite_id)
                src_upper_suite_ids_new = src_upper_suite_ids_new.strip(',')

                suite_data = {'parent_id': target_suite_id, 'update_id':update_id, 'all_upper_node_ids': src_upper_suite_ids_new }
                with transaction.atomic():
                    # 黏贴被剪切的测试套件
                    serializer = TestcaseSuiteSerializer(src_suite, data=suite_data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    # 修改被剪切测试套件的所有子测试集所有上级测试套件id
                    PasteSuiteCutAPIView.update_sub_suites(src_suite_id, src_upper_suite_ids_old_set, src_upper_suite_ids_new)
                    if src_suite_type == 'sprint': ## 移动被剪切的迭代测试套件所关联的基线测试套件
                       # 获取待黏贴至目标测试套件关联的迭代或基线测试套件
                        sprint_base_suite_relation = SprintBaseCaseSuiteRelation.objects.filter(sprint_case_suite_id=target_suite_id).first()
                        if sprint_base_suite_relation:
                            related_target_suite = TestcaseSuite.objects.filter(id=sprint_base_suite_relation.base_case_suite_id, is_delete=0).first()
                        else:# 判断待黏贴至目标测试套件关联测试套件(暂且称之为 关联目标测试套件)是否为基线根测试套件
                             if target_suite.parent_id == -1: # 目标测试套件为基线根测试套件,获取其 关联目标测试套件
                                 related_target_suite =  TestcaseSuite.objects.filter(type='base', is_delete=0, product_id=product_id, parent_id=-1, sprint_id=-1, all_upper_node_id=-1).first()
                             else:
                                 related_target_suite = None

                        if related_target_suite: # 存在 关联目标测试套件
                            result['data']['relatedTargetSuite'] = TestcaseSuiteSerializer(related_target_suite).data
                            related_target_suite_id = related_target_suite.id

                            # 判断关联目标测试套件下是否存在和被剪切测试套件同名的子测套件
                            sub_suite = TestcaseSuite.objects.filter(parent_id=related_target_suite_id, name=src_suite.name, is_delete=0).first()
                            if sub_suite:
                                raise Exception('SuiteDuplicate')
                            else:
                                # 不存在，剪切 被剪切测试套件所关联测试套件到 关联目标测试套件下
                                related_src_suite = None
                                # 获取被剪切的测试套件关联的测试套件
                                sprint_base_suite_relation = SprintBaseCaseSuiteRelation.objects.filter(sprint_case_suite_id=src_suite_id).first()
                                if sprint_base_suite_relation:
                                    related_src_suite = TestcaseSuite.objects.filter(id=sprint_base_suite_relation.base_case_suite_id, is_delete=0).first()
                                if related_src_suite:
                                    # 记录待黏贴至关联目标测试套件所有上级套件id
                                    target_upper_suite_ids = related_target_suite.all_upper_node_ids.split(',')
                                    if '-1' in target_upper_suite_ids:
                                        target_upper_suite_ids.remove('-1')

                                    # 记录被被剪切测试套件关联的测试套件的所有上级套件id
                                    src_upper_suite_ids_old = related_src_suite.all_upper_node_ids.replace(' ', '').split(',')
                                    if '-1' in src_upper_suite_ids_old:
                                        src_upper_suite_ids_old.remove('-1')
                                    src_upper_suite_ids_old_set = set([item for item in src_upper_suite_ids_old])

                                    # 获取被被剪切测试套件关联的测试套件黏贴后的所有上级套件id
                                    src_upper_suite_ids_new = ','.join(target_upper_suite_ids) + ',' + str(related_target_suite_id)
                                    src_upper_suite_ids_new = src_upper_suite_ids_new.strip(',')
                                    suite_data = {'parent_id': related_target_suite_id, 'update_id':update_id, 'all_upper_node_ids': src_upper_suite_ids_new }

                                    # 黏贴被剪切测试套件关联的基线测试套件
                                    serializer = TestcaseSuiteSerializer(related_src_suite, data=suite_data, partial=True)
                                    serializer.is_valid(raise_exception=True)
                                    serializer.save()
                                    result['data']['relatedSrcSuite'] = serializer.data

                                    # 修改被剪切测试套件关联的测试套件的所有子测试集所有上级测试套件id
                                    PasteSuiteCutAPIView.update_sub_suites(related_src_suite.id, src_upper_suite_ids_old_set, src_upper_suite_ids_new)
            else:
                result['msg'] = '黏贴失败，被剪切的测试集不存在'
                result['success'] =  False
                return Response(request, status.HTTP_404_NOT_FOUND)
            result['msg'] =  '黏贴成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            if result['msg'] == 'SuiteDuplicate':
                result['msg'] =  '黏贴失败：当前测试集关联的基线测试集下已存在同名子测试集'
                return Response(result, status.HTTP_200_OK)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
