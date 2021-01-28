#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backend.models import SprintTestplan
from backend.models import SprintTestplanTestcase
from backend.models import TestcaseSuite

from backend.models import SprintTestplanTestcaseAttachment

from backend.serializers import SprintTestplanTestcaseSerializer

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from collections import OrderedDict

import shortuuid
import os
import logging

logger = logging.getLogger('mylogger')

class TestplanTestcaseListAPIView(APIView):
    '''
    测试视图-测试计划管理-测试详情，测试用例，查询测试用例表数据
    '''

    def get_suite_path(self, suite_id, suite_path=""):
        '''获取套件路径'''
        obj = TestcaseSuite.objects.filter(id=suite_id).values('parent_id', 'name').first()
        if obj:
            suite_path = obj.get('name')
            parent_id = obj.get('parent_id')
            if parent_id != -1: # 存在上级测试套件
                suite_path = self.get_suite_path(parent_id, suite_path) + '/' + suite_path
        return suite_path

    def get(self, request, format=None):
        '''查询列表数据'''
        result = {}
        try:
            params =  request.GET
            name = params.get('caseName') # 用例名称
            priority = params.get('priority')
            execution_phase = params.get('executionPhase')
            execution_method = params.get('executionMethod')
            recursive = int(params.get('recursive'))
            tester_id = params.get('testerId')
            assigned_id = params.get('assignedTo')
            test_result = params.get('result')
            tester_name = params.get('tester')
            tag = params.get('tag')
            suite_id = params.get('suiteId')
            # sprint_id = params.get('sprintId')
            suite_type = params.get('suiteType')
            testplan_id = int(params.get('planId'))
            page_size = int(params.get('pageSize'))
            page_no = int(params.get('pageNo'))
            sort = params.get('sort')
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            startIndex = (page_no - 1) * page_size
            endIndex = startIndex + page_size

            filters = {'testplan_id':testplan_id}

            if name:
                filters['name__startswith'] = name

            if priority:
                priority_list = priority.split(',')
                filters['priority__in'] = priority_list

            if execution_method:
                filters['execution_method'] = execution_method


            if test_result:
                filters['result'] = test_result
            # if creater:
            #     filters['creater'] = creater
            #
            # if updater:
            #     filters['updater'] = updater

            if tester_id:
                filters['tester_id'] = tester_id

            if assigned_id:
                filters['assigned_to_id'] = assigned_id

            if tester_name:
                filters['tester_name'] = tester_name

            where_list = []
            if tag:
                temp = 'find_in_set("%s", tags)' % tag
                where_list.append(temp)

            if execution_phase:
                temp  = 'find_in_set("%s", execution_phase)' % execution_phase
                where_list.append(temp)

            if recursive:
                suite_id_list = []
                suite_id_list.append(int(suite_id))
                 # 获取子测试套件id
                query_sql = 'SELECT id FROM tb_testcase_suite AS t ' \
                           'WHERE FIND_IN_SET(%s, t.all_upper_node_ids)' % int(suite_id)
                query_result = TestcaseSuite.objects.raw(query_sql)
                sub_suite_id_list = []
                for item in query_result:
                   sub_suite_id_list.append(int(item.id))
                suite_id_list.extend(sub_suite_id_list)
            else:
                suite_id_list = [int(suite_id)]

            if suite_id_list:
                filters['suite_id__in'] = suite_id_list
            else:
                result['msg'] =  '获取成功'
                result['success'] =  True
                result['data'] = {}
                result['data']['rows'] = []
                result['data']['total'] = 0
                return Response(result, status.HTTP_200_OK)

            # 获取套件关联的测试用例
            if where_list:
                testcases = SprintTestplanTestcase.objects.filter(**filters).extra(where=where_list).order_by(*sort_list)[startIndex:endIndex]
                total = SprintTestplanTestcase.objects.filter(**filters).extra(where=where_list).count()
            else:
                testcases = SprintTestplanTestcase.objects.filter(**filters).order_by(*sort_list)[startIndex:endIndex]
                total = SprintTestplanTestcase.objects.filter(**filters).count()

            temp_dict = OrderedDict()
            if testcases:
                testcases = SprintTestplanTestcaseSerializer(testcases, many=True).data
                for testcase in testcases:
                    testcase['suiteType'] = 'testplan'
                    testcase['detailSuiteType'] = suite_type # 更细分套件类型 base|sprint

                    if testcase['tags']:
                        testcase['tags'] = testcase['tags'].split(',')
                    else:
                        testcase['tags'] = []
                    if testcase['execution_phase']:
                        testcase['execution_phase'] = testcase['execution_phase'].split(',')
                    else:
                        testcase['execution_phase'] = []
                    testcase['children'] = []

                    suite_id = testcase.get('suite_id')
                    if suite_id not in temp_dict:
                        suite_path = self.get_suite_path(suite_id)
                        suite_path = '/' + suite_path
                        guid = shortuuid.uuid()
                        temp_dict[suite_id] = {
                            'id':'',
                            'testplan_id':testplan_id,
                            'guid': guid,
                            'custom_no':'',
                            'suite_id':suite_id,
                            'sprint_testcase_guid':None,
                            'sprint_id':'',
                            'product_id':'',
                            'parent_id': '',
                            'name':suite_path,
                            'priority': '',
                            'execution_phase':'',
                            'execution_method':'',
                            'executed_each_sprint':'',
                            'tags':'',
                            'desc':'',
                            'precondition':'',
                            'postcondition': '',
                            'creater_id': None,
                            'creater_name':'',
                            'create_time':'',
                            'updater_id':None,
                            'updater_name':'',
                            'update_time':'',
                            'result':'',
                            'tester_id':None,
                            'tester_name':'',
                            'assigned_to':'',
                            'children':[]
                        }


                    testcase['children'] = []
                    testcase['suitePath'] = temp_dict[testcase.get('suite_id')]['name']
                    temp_dict[testcase.get('suite_id')]['children'].append(testcase)

                testcases = []
                for key, value in temp_dict.items():
                    testcases.append(value)
            else:
                testcases = []
                total = 0
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = {}
            result['data']['rows'] = testcases
            result['data']['total'] = total
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestplanTestcaseResultAPIView(APIView):
    '''
    测试视图-测试计划管理-计划详情，测试用例-逐条修改用例测试结果（这块逻辑比较复杂，单独编写一个API）
    '''

    @staticmethod
    def update_testplan_info(testplan, plan_status_old, execution_time, updater_id, updater_name):
        '''更新计划实际开始时间和实际完成时间，测试状态
            testplan 测试计划对象
            plan_status_old 更改用例测试结果前，测试计划状态
            execution_time 更新时间对象
        '''

        if not testplan.case_num_blocked and testplan.case_num_executed == testplan.case_num_related: # 已执行用例数 = 关联用例总数 并且 没有阻塞用例,完成测试，更新实际完成时间,测试状态
            testplan.finish_time = execution_time
            testplan.status = '已完成'
        elif testplan.case_num_blocked or (testplan.case_num_executed and testplan.case_num_executed < testplan.case_num_related): # 存在阻塞用例 或者 已执行用例数大于0 但是小于关联用例总数 更新实际完成时间,测试状态
            testplan.finish_time = None
            testplan.status = '未完成'
        elif testplan.case_num_executed == 0: # 没有已执行用例，更新实际开始时间，完成时间
            testplan.start_time = None
            testplan.finish_time = None
            testplan.status = '未执行'
        if plan_status_old == '未执行' and testplan.status != '未执行': # 刚开始测试，更新实际开始时间
            testplan.start_time = execution_time
        testplan.updater_id = updater_id
        testplan.updater_name = updater_name
        testplan.save()

        return {'caseNumRelated': testplan.case_num_related,
                 'caseNumSuccess': testplan.case_num_success,
                 'caseNumFail':testplan.case_num_fail,
                 'caseNumExecuted':testplan.case_num_executed,
                 'caseNumBlocked':testplan.case_num_blocked,
                 'status': testplan.status,
                 'startTime':execution_time.strftime('%Y-%m-%d %H:%M:%S') if testplan.start_time else '',
                 'finishTime': execution_time.strftime('%Y-%m-%d %H:%M:%S') if testplan.finish_time else '',
                 'updaterId':updater_id,
                 'updaterName':updater_name,
                 'updateTime':testplan.update_time.strftime('%Y-%m-%d %H:%M:%S')
                 }

    @staticmethod
    def caculate_testplan_case_statistics(testplan, case_curr_result, case_target_result):
        '''根据用例状态变化，动态计算测试计划用例统计数据'''

        if case_curr_result != '通过' and case_target_result == '通过': # 非通过 -> 通过 执行成功用例数 + 1
            # 更改用例所在的测试计划已成功执行用例数 + 1
            testplan.case_num_success = testplan.case_num_success + 1
        elif case_curr_result == '通过' and case_target_result != '通过': # 通过 -> 非通过， 执行成功用例数 - 1
            testplan.case_num_success = testplan.case_num_success - 1

        if case_curr_result == '未执行' and case_target_result != '未执行': # 未执行 -> 非未执行 已执行用例数 + 1
            testplan.case_num_executed = testplan.case_num_executed + 1
        elif case_curr_result != '未执行' and case_target_result == '未执行':  # 非未执行 -> 未执行 已执行用例数 - 1, 如果标记为“未执行”测试用例执行时间置为NULL
            testplan.case_num_executed = testplan.case_num_executed - 1

        if case_curr_result == '阻塞' and case_target_result !=  '阻塞': # 阻塞 -> 非阻塞 阻塞用例数 + 1
            testplan.case_num_blocked = testplan.case_num_blocked - 1
        elif case_curr_result !=  '阻塞' and case_target_result == '阻塞':  # 非阻塞 -> 阻塞 阻塞行用例数 - 1
            testplan.case_num_blocked = testplan.case_num_blocked + 1

        if case_curr_result == '失败' and case_target_result !=  '失败': # 失败 -> 非失败 失败用例数 + 1
            testplan.case_num_fail = testplan.case_num_fail - 1
        elif case_curr_result !=  '失败' and case_target_result == '失败':  # 非失败 -> 失败 失败用例数 - 1
            testplan.case_num_fail = testplan.case_num_fail + 1

    # 逐条修改用例测试结果
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            updater_id = request.user.id
            updater_name = request.user.name
            case_target_result = data.get('result')
            execution_time = timezone.now()
            data['execution_time'] = execution_time
            if case_target_result == '未执行':
                data['tester_id'] = None
                data['tester_name'] = None
                data['execution_time'] = None
            else:
                data['tester_id'] = updater_id
                data['tester_name'] = updater_name
            id = data.get('id')
            testplan_id = data.get('plan_id')

            del data['id']
            del data['plan_id']

            try:
                with transaction.atomic():
                    # 获取用例当前状态
                    testcase = SprintTestplanTestcase.objects.select_for_update().filter(id=id).first()
                    case_curr_result = testcase.result

                    serializer = SprintTestplanTestcaseSerializer(testcase, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    if case_curr_result == case_target_result: # 已是目标状态
                        result['msg'] =  '修改成功'
                        result['success'] =  True
                        case_data_updated = {}
                        data_keys = list(data.keys())
                        for key in data_keys:
                            case_data_updated[key] = serializer.data.get(key)
                        result['data'] = {}
                        result['data']['caseDataUpdated'] =  case_data_updated
                        result['data']['planDataUpdated'] = {}
                        return Response(result, status.HTTP_200_OK)

                    # 更新计划用例统计数据
                    testplan = SprintTestplan.objects.select_for_update().filter(id=testplan_id).first()
                    plan_status_old = testplan.status # 保存当前测试计划状态

                    TestplanTestcaseResultAPIView.caculate_testplan_case_statistics(testplan, case_curr_result, case_target_result)
                    plan_data_updated = TestplanTestcaseResultAPIView.update_testplan_info(testplan, plan_status_old, execution_time, updater_id, updater_name)
            except Exception as e:
                result['msg'] =  '修改失败：%s' % e
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result['msg'] =  '修改成功'
            result['success'] =  True
            result['data'] = {}
            case_data_updated = {}
            data_keys = list(data.keys())
            for key in data_keys:
                case_data_updated[key] = serializer.data.get(key)
            result['data']['caseDataUpdated'] =  case_data_updated
            result['data']['planDataUpdated'] = plan_data_updated
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestplanTestcasesResultsAPIView(APIView):
    '''
    测试视图-测试计划管理-计划详情，测试用例-批量修改用例测试结果
    '''

    # 批量修改用例测试结果
    def patch(self, request, format=None):
        result = {}
        result['data'] = {}
        result['data']['caseDatasUpdated'] = []
        plan_data_updated = {}
        try:
            data = request.data
            updater_id = request.user.id
            updater_name = request.user.name
            execution_time = timezone.now()
            data['execution_time'] = execution_time
            case_target_result = data.get('result')
            if case_target_result == '未执行':
                data['tester_id'] = None
                data['tester_name'] = None
                data['execution_time'] = None
            else:
                data['tester_id'] = updater_id
                data['tester_name'] = updater_name

            case_id_list = data.get('case_ids')
            testplan_id = data.get('plan_id')

            del data['plan_id']
            del data['case_ids']

            try:
                with transaction.atomic():
                    testplan = SprintTestplan.objects.select_for_update().filter(id=testplan_id).first()
                    for id in case_id_list:
                        with transaction.atomic():
                            # 获取用例当前状态
                            testcase = SprintTestplanTestcase.objects.select_for_update().filter(id=id).first()
                            case_curr_result = testcase.result

                            serializer = SprintTestplanTestcaseSerializer(testcase, data=data, partial=True)
                            serializer.is_valid(raise_exception=True)
                            serializer.save()

                            case_data_updated = {}
                            data_keys = list(data.keys())
                            data_keys.append('id')
                            for key in data_keys:
                                case_data_updated[key] = serializer.data.get(key)
                            result['data']['caseDatasUpdated'].append(case_data_updated)

                            if case_curr_result == case_target_result: # 已是目标状态
                                continue

                            # # 更新计划用例统计数据
                            plan_status = testplan.status
                            TestplanTestcaseResultAPIView.caculate_testplan_case_statistics(testplan, case_curr_result, case_target_result)
                            plan_data_updated = TestplanTestcaseResultAPIView.update_testplan_info(testplan, plan_status, execution_time, updater_id, updater_name)
            except Exception as e:
                result['msg'] =  '修改失败：%s' % e
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result['msg'] =  '修改成功'
            result['success'] =  True
            result['data']['planDataUpdated'] = plan_data_updated
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestplanTestcaseAPIView(APIView):
    '''
    测试视图-测试计划管理-测试计划详情，测试用例，修改用例（当前用于修改测试结果，测试备注等不需要同步迭代、基线用例的字段）
    '''

    # 修改用例
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            updater_id = request.user.id
            if 'assigned_to' not in data.keys():
                data['updater_id'] = updater_id
                data['updater_name'] = request.user.name

            id = data.get('id')

            del data['id']
            try:
                testcase = SprintTestplanTestcase.objects.filter(id=id).first()
                serializer = SprintTestplanTestcaseSerializer(testcase, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except Exception as e:
                result['msg'] =  '修改失败：%s' % e
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result['msg'] =  '修改成功'
            result['success'] =  True
            data_updated = {}
            data_keys = list(data.keys())
            data_keys.append('update_time')
            for key in data_keys:
                data_updated[key] = serializer.data.get(key)
            result['data'] =  data_updated
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 逐条删除用例
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            id = data.get('id')
            testplan_id = data.get('plan_id')
            updater_id = request.user.id
            updater_name = request.user.name
            plan_data_updated = {}

            with transaction.atomic():
                testcase = SprintTestplanTestcase.objects.select_for_update().filter(id=id).first()
                if testcase:
                    case_result = testcase.result

                    # 删除取消关联用例的用附件
                    attachments = SprintTestplanTestcaseAttachment.objects.filter(case_guid=testcase.guid, testplan_id=testplan_id)
                    for attachment in attachments:
                        file_absoulte_path = settings.MEDIA_ROOT + '/'+ attachment.file_path
                        if os.path.exists(file_absoulte_path) and os.path.isfile(file_absoulte_path):
                            os.remove(file_absoulte_path)
                    attachments.delete()
                    testcase.delete()

                    # 更新计划用例统计数据
                    testplan = SprintTestplan.objects.select_for_update().filter(id=testplan_id).first()
                    if testplan:
                        plan_status = testplan.status
                        testplan.case_num_related = testplan.case_num_related - 1 # 已关联用例数-1
                        if case_result == '通过': # 已执行用例数 -1，执行成功用例数 - 1
                            testplan.case_num_success = testplan.case_num_success - 1
                            testplan.case_num_executed = testplan.case_num_executed - 1
                        elif case_result == '失败':
                            testplan.case_num_fail = testplan.case_num_fail - 1
                            testplan.case_num_executed = testplan.case_num_executed - 1
                        elif case_result == '阻塞':
                            testplan.case_num_blocked = testplan.case_num_blocked - 1
                            testplan.case_num_executed = testplan.case_num_executed - 1

                        execution_time = timezone.now()
                        plan_data_updated = TestplanTestcaseResultAPIView.update_testplan_info(testplan, plan_status, execution_time, updater_id, updater_name)
            result['msg'] =  '删除成功'
            result['success'] =  True
            result['data'] = plan_data_updated
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestcaseExportAPIView(APIView):
    '''
    测试视图-测试计划管理-测试详情，测试用例，批量导出测试用例
    '''

    def get(self, request, format=None):
        pass
        result = {}
        result['msg'] = '功能待开发'
        result['success'] = True
        return Response(result, status.HTTP_200_OK)


