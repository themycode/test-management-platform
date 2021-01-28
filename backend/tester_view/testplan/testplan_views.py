#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import json
import logging
import os
import shortuuid

from django.utils import timezone
from django.db import transaction
from django.conf import settings
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.models import SprintTestplan
from backend.models import SprintTestplanTestcase
from backend.models import TestcaseAttachment
from backend.models import SprintTestplanTestcaseAttachment
from backend.serializers import SprintTestplanTestcaseSerializer
from backend.serializers import SprintTestplanSerializer
from .testplan_testcase_views import TestplanTestcaseResultAPIView


logger = logging.getLogger('mylogger')

class TestplanListAPIView(APIView):
    '''
    测试视图-测试计划管理，查询测试计划列表数据，批量删除测试计划
    '''

    def get(self, request, format=None):
        '''查询列表数据'''
        result = {}
        try:
            params =  request.GET
            sprint_id = params.get('sprintId') # 关联迭代id
            product_id = params.get('productId') # 所属产品id
            start_time = params.get('startTime') # 创建起时时间
            end_time = params.get('endTime')  # 创建结束时间
            finish_start_time = params.get('finishStartTime') # 完成起始时间
            finish_end_time = params.get('finishEndTime') # 完成结束时间
            name = params.get('name') # 计划名称
            plan_status = params.get('status') # 计划状态
            creater = params.get('creater') # 创建人
            environment = params.get('environment') # 执行环境
            page_size = int(params.get('pageSize'))
            page_no = int(params.get('pageNo'))
            sort = params.get('sort')
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            start_index = (page_no - 1) * page_size
            end_index = start_index + page_size
            if sprint_id:
                filters = {'product_id':product_id, 'sprint_id':sprint_id, 'is_delete':0}
            else:
                filters = {'product_id':product_id,  'is_delete':0}
            if start_time:
                start_datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                filters['create_time__gte'] = start_datetime
            if end_time:
                end_datetime = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                filters['create_time__lte'] = end_datetime

            if finish_start_time:
                finish_start_time = datetime.strptime(finish_start_time, '%Y-%m-%d %H:%M:%S')
                filters['start_time__gte'] = finish_start_time
            if finish_end_time:
                finish_end_time = datetime.strptime(finish_end_time, '%Y-%m-%d %H:%M:%S')
                filters['finish_time__lte'] = finish_end_time

            if name:
                filters['name__startswith'] = name

            if plan_status:
                filters['status__in'] = plan_status.split(',')

            if creater:
                filters['creater_name'] = creater

            if environment:
                filters['env_names__contains'] = environment

            testplans = SprintTestplan.objects.filter(**filters)
            if testplans.exists():
                total = len(testplans)
                testplans = testplans.order_by(*sort_list)[start_index:end_index]
                testplans = SprintTestplanSerializer(testplans, many=True).data
            else:
                testplans = []
                total = 0
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = {}
            result['data']['rows'] = testplans
            result['data']['total'] = total
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


    # 批量删除列表数据
    def delete(self, request, format=None):
        try:
            data = request.data
            plan_ids = data.get('row_ids')
            result = {}
            SprintTestplan.objects.filter(id__in=plan_ids, case_num_related=0).update(is_delete=1)
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestplanAPIView(APIView):
    '''
    测试视图-测试计划管理，新增，修改，删除迭代测试计划,查询某个迭代测试计划的信息
    '''

    # 新增迭代测试计划
    def post(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['start_time'] = None
            data['finish_time'] = None
            data['creater_id'] = request.user.id
            data['updater_id'] = data['creater_id']
            data['creater_name'] = request.user.name
            data['updater_name'] = request.user.name
            data['is_delete'] = False
            data['status'] = '未执行'
            data['case_num_executed'] = 0
            data['case_num_success'] = 0
            data['case_num_fail'] = 0
            data['case_num_blocked'] = 0
            data['case_num_related'] = 0
            try:
                serializer = SprintTestplanSerializer(data=data)
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

    # 修改迭代测试计划
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['updater_id'] = request.user.id
            plan_id = data.get('id')
            del data['id']

            testplan = SprintTestplan.objects.filter(id=plan_id).first()
            if testplan:
                try:
                    serializer = SprintTestplanSerializer(testplan, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                except Exception as e:
                    result['msg'] =  '修改失败：%s!' % e
                    result['success'] =  False
                    return Response(result, status.HTTP_400_BAD_REQUEST)
            else:
                result['msg'] = '修改失败,计划不存在'
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

    # 逐条删除测试计划
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            plan_id = data.get('id')
            testplan = SprintTestplan.objects.filter(id=plan_id).first()
            if testplan and testplan.case_num_related:
                result['msg'] =  '删除失败，请先删除该测试计划关联的测试用例'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)
            else:
                testplan.is_delete=1
                testplan.save()
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


    # 查询详情
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            plan_id = params.get('id')
            fields = params.get('fields')
            query_filters = params.get('filters')

            filters = {'is_delete':0, 'id':plan_id}
            if query_filters:
                query_filters = json.loads(query_filters)
                filters.update(query_filters)

            if fields:
                fields = fields.split(',')
                rows = SprintTestplan.objects.filter(**filters).values(*fields)
            else:
                rows = SprintTestplan.objects.filter(**filters).values()

            result['msg'] =  '获取成功'
            result['success'] =  True
            row = rows[0] if rows else {}
            if 'create_time' in row:
                row['create_time'] = row['create_time'].strftime('%Y-%m-%d %H:%M:%S')
            if 'update_time' in row:
                row['update_time'] = row['update_time'].strftime('%Y-%m-%d %H:%M:%S')
            result['data'] = row
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestplanTestcasesAPIView(APIView):
    '''
    测试视图-测试计划管理，为计划关联测试用例
    '''

    @staticmethod
    def sync_case_attachments(case_guid, testplan_id):
        '''
        同步测试用例附件到测试计划关联测试用例附件表
        case_type：base|sprint 即基线用例、迭代用例
        '''
        try:
            testcase_attatchments = TestcaseAttachment.objects.filter(case_guid=case_guid, is_delete=0)

            for attachment in testcase_attatchments:
                if not SprintTestplanTestcaseAttachment.objects.filter(attachment_guid=attachment.guid, is_delete=0).first(): # 不存在则生成新的附件
                    # 待新生成附件的绝对对路径
                    file_path = attachment.file_path
                    path, suffix = os.path.splitext(file_path)
                    file_name = os.path.basename(file_path)
                    time_str = path[-8:]
                    target_file_name = shortuuid.uuid() + time_str + suffix
                    file_relative_path = file_path.replace(file_name, target_file_name)
                    file_absolute_path = settings.MEDIA_ROOT.rstrip('/') + file_relative_path # file_relative_path 以 / 打头
                    src_file_absolute_path = settings.MEDIA_ROOT.rstrip('/') + file_path
                    if not os.path.exists(src_file_absolute_path): # 源文件不存在，则结束,不做任何处理
                        return

                    target_file = open(file_absolute_path, 'wb')
                    try:
                        with open(src_file_absolute_path, 'rb') as f:
                            for content in f:
                                target_file.write(content)
                    finally:
                        target_file.close()

                    file_path = file_relative_path

                    guid = shortuuid.uuid()
                    obj = SprintTestplanTestcaseAttachment(attachment_guid = attachment.guid, guid=guid, testplan_id=testplan_id, case_guid=attachment.case_guid, name=attachment.name, file_path=file_path, creater_id=attachment.creater_id, create_time=attachment.create_time, is_delete=0)
                    obj.save()
        except Exception as e:
            raise Exception('%s' % e)


    # 为迭代测试计划关联测试用例
    def post(self, request, format=None):
        result = {}
        guids_of_related_cases = [] # 存放当前页面，最新关联的测试用例guid
        try:
            data = request.data
            cases_selected = data.get('rows_selected')
            testplan_id = data.get('plan_id')
            guids_of_related_old_cases = data.get('guids_of_related_old_cases') # 注意，不是全部，而是当前页面刚加载完成时，已关联测试用例的guid

            with transaction.atomic():
                testplan = SprintTestplan.objects.select_for_update().filter(id=testplan_id).first()
                if not testplan:
                     result['msg'] =  '关联失败，计划不存在'
                     result['success'] =  False
                     return Response(result, status.HTTP_400_BAD_REQUEST)

                # 处理需要关联的用例
                for item in cases_selected:
                    if not item.get('children'): # 非测试套件，即为测试用例
                        try:
                            testcase = SprintTestplanTestcase.objects.select_for_update().filter(testplan_id=testplan_id, guid=item.get('guid')).first()
                            if testcase: # 用例已关联，则更新用例信息
                                case_data = {}
                                case_data['custom_no'] = item['custom_no']
                                case_data['suite_id'] = item['suite_id']
                                case_data['sprint_id'] = item['sprint_id']
                                case_data['product_id'] = item['product_id']
                                if 'sprint_testcase_guid' in item:
                                    case_data['sprint_testcase_guid'] = item['sprint_testcase_guid']
                                case_data['name'] = item['name']
                                case_data['priority'] = item['priority']
                                case_data['execution_phase'] = ','.join(item['execution_phase'])
                                case_data['execution_method'] = item['execution_method']
                                case_data['executed_each_sprint'] = item['executed_each_sprint']
                                case_data['tags'] = ','.join(item['tags'])
                                case_data['desc'] = item['desc']
                                case_data['precondition'] = item['precondition']
                                case_data['steps'] = item['steps']
                                case_data['postcondition'] = item['postcondition']
                                case_data['updater_id'] = item['updater_id']
                                case_data['updater_name'] = item['updater_name']
                                case_data['update_time'] = item['update_time']
                                case_data['is_delete'] = 0
                                # 更新已关联测试用例
                                serializer = SprintTestplanTestcaseSerializer(testcase, data=case_data, partial=True)
                            else: # 不存在则插入用例
                                del item['id']
                                del item['suite_path']

                                item['testplan_id'] = testplan_id
                                item['tester_id'] = None
                                item['assigned_to'] = item['updater_name'] # 暂且定义为更新人
                                item['assigned_to_id'] = item['updater_id']
                                item['result'] = '未执行'
                                item['tags'] = ','.join(item['tags']) # tags按字符串存储，彼此之间采用逗号分隔
                                item['execution_phase'] = ','.join(item['execution_phase'])
                                serializer = SprintTestplanTestcaseSerializer(data=item)

                            serializer.is_valid(raise_exception=True)
                            serializer.save()

                            guids_of_related_cases.append(item.get('guid'))

                            # 同步测试用例的附件
                            TestplanTestcasesAPIView.sync_case_attachments(item.get('guid'), testplan_id)
                        except Exception as e:
                            result['msg'] =  '关联失败：%s' % e
                            result['success'] =  False
                            return Response(result, status.HTTP_400_BAD_REQUEST)

                # 删除取消关联的用例
                temp_guid_set = set(guids_of_related_old_cases) - set(guids_of_related_cases)
                SprintTestplanTestcase.objects.select_for_update().filter(testplan_id=testplan_id, guid__in=list(temp_guid_set)).delete()


                # 删除取消关联的用例附件
                attachments = SprintTestplanTestcaseAttachment.objects.filter(testplan_id=testplan_id,case_guid__in=list(temp_guid_set) )
                for attachment in attachments:
                    file_absoulte_path = settings.MEDIA_ROOT.rstrip('/') + attachment.file_path
                    if os.path.exists(file_absoulte_path) and os.path.isfile(file_absoulte_path):
                        os.remove(file_absoulte_path)
                attachments.delete()

                testplan.case_num_success = SprintTestplanTestcase.objects.filter(testplan_id=testplan_id, result='通过').count()
                testplan.case_num_fail = SprintTestplanTestcase.objects.filter(testplan_id=testplan_id, result='失败').count()
                testplan.case_num_blocked = SprintTestplanTestcase.objects.filter(testplan_id=testplan_id, result='阻塞').count()
                testplan.case_num_executed = testplan.case_num_success + testplan.case_num_fail
                testplan.case_num_related =  SprintTestplanTestcase.objects.filter(testplan_id=testplan_id).count()
                res = TestplanTestcaseResultAPIView.update_testplan_info(testplan, testplan.status, timezone.now(), request.user.id, request.user.name)
            result['msg'] =  '关联成功'
            result['success'] =  True
            result['data'] = res
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


    # 批量删除列表数据
    def delete(self, request, format=None):
        result = {}
        def sync_delete_attatchment(guid_list):
            # 删除取消关联的用例附件
            attachments = SprintTestplanTestcaseAttachment.objects.filter(case_guid__in=guid_list, testplan_id=testplan_id)
            for attachment in attachments:
                file_absoulte_path = settings.MEDIA_ROOT.rstrip('/') + attachment.file_path # attachment.file_path 以 / 打头
                if os.path.exists(file_absoulte_path) and os.path.isfile(file_absoulte_path):
                    os.remove(file_absoulte_path)
            attachments.delete()

        try:
            data = request.data
            case_id_list = data.get('case_ids')
            testplan_id = data.get('plan_id')
            testcase_num_pass = 0
            testcase_num_fail = 0
            testcase_num_blocked = 0
            testcase_num_unexecuted  = 0


            with transaction.atomic():
                # 先统一查找，再执行删除，避免因为删除操作带来的查询结果不准确问题
                testcases_pass = SprintTestplanTestcase.objects.select_for_update().filter(id__in=case_id_list, result='通过')
                testcases_fail = SprintTestplanTestcase.objects.select_for_update().filter(id__in=case_id_list, result='失败')
                testcases_blocked = SprintTestplanTestcase.objects.select_for_update().filter(id__in=case_id_list, result='阻塞')
                testcase_unexecuted = SprintTestplanTestcase.objects.select_for_update().filter(id__in=case_id_list, result='未执行')

                if testcases_pass.exists():
                    sync_delete_attatchment(testcases_pass.values_list('guid', flat=True))
                    testcase_num_pass = len(testcases_pass)
                    testcases_pass.delete()

                if testcases_fail.exists():
                    sync_delete_attatchment(testcases_fail.values_list('guid', flat=True))
                    testcase_num_fail = len(testcases_fail)
                    testcases_fail.delete()

                if testcases_blocked.exists():
                    sync_delete_attatchment(testcases_blocked.values_list('guid', flat=True))
                    testcase_num_blocked = len(testcases_blocked)
                    testcases_blocked.delete()

                if testcase_unexecuted.exists():
                    sync_delete_attatchment(testcase_unexecuted.values_list('guid', flat=True))
                    testcase_num_unexecuted = len(testcase_unexecuted)
                    testcase_unexecuted.delete()

                # 更新计划用例统计数据
                testplan = SprintTestplan.objects.select_for_update().filter(id=testplan_id).first()
                if testplan:
                    testcase_num_executed = testcase_num_pass + testcase_num_fail + testcase_num_blocked
                    testplan.case_num_related = testplan.case_num_related - testcase_num_executed - testcase_num_unexecuted
                    testplan.case_num_success = testplan.case_num_success - testcase_num_pass
                    testplan.case_num_fail = testplan.case_num_fail - testcase_num_fail
                    testplan.case_num_executed = testplan.case_num_executed - testcase_num_executed
                    testplan.case_num_blocked = testplan.case_num_blocked - testcase_num_blocked

                    res = TestplanTestcaseResultAPIView.update_testplan_info(testplan, testplan.status, timezone.now(), request.user.id, request.user.name)
            result['msg'] =  '删除成功'
            result['success'] =  True
            result['data'] = res
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 批量修改用例
    def patch(self, request, format=None):
        result = {}
        result['data'] = []
        try:
            data = request.data
            assigned_to = data.get('batch_assigned_to').get('name')
            assigned_to_id = data.get('batch_assigned_to').get('id')
            case_id_list = data.get('case_ids')


            if 'batch_assigned_to' in data.keys(): # 批量修改用例"指派给对象"
                testcases = SprintTestplanTestcase.objects.filter(id__in=case_id_list)
                testcases.update(assigned_to=assigned_to)
                testcases.update(assigned_to_id=assigned_to_id)

                result['data'] = testcases.values('id', 'assigned_to', 'assigned_to_id')
            else:
                # updater_id = request.user.updater_id
                # updater_name = request.user.name
                # data['updater_id'] = updater_id
                # data['updater_name'] = updater_name
                # data['update_time'] = timezone.now()
                # del data['plan_id']
                # del data['case_ids']
                pass
                # 暂时不实现

            result['msg'] =  '修改成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '修改失败：%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestplanTestcasesGuidsAPIView(APIView):
    '''
    测试视图-测试计划管理，获取计划关联的测试用例guid
    '''
    # 获取计划关联的测试用例guid
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            testplan_id = params.get('planId')
            rows = SprintTestplanTestcase.objects.filter(testplan_id=testplan_id).values_list('guid', flat=True)
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = rows
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
