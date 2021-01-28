#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = '赖富玉'

from datetime import date
from datetime import timedelta
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Min
from django.db.models import Max

from backend.models import Sprint
from backend.models import SprintTestplan
from backend.models import SysGroupRelatedGroup
from backend.models import ZentaoGroupDefectTrendDailyStatistics
from backend.zentao.zentaoTool import ZentaoQueryTool


logger = logging.getLogger('mylogger')



class WorkbenchSprintsStatisticsAPIView(APIView):
    '''
    工作台-迭代测试统计
    '''


    def get(self, request, format=None):
        '''展示工作台内容'''

        result = {}
        sprints_statistics = {} # 存放迭代相关统计数据
        try:
            data = request.GET
            sprint_ids = data.get('sprintIds')
            sprint_id_list = sprint_ids.split(',')
            user_group_ids = data.get('userGroupIds')
            user_group_id_list = user_group_ids.split(',')

            # 获取迭代项目名称
            sprints = Sprint.objects.filter(id__in=sprint_id_list, is_delete=0)
            if not sprints.exists():
                result['msg'] =  '迭代项目不存在，或者已删除'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            # 获取最早的测试计划实际开始时间，最晚的测试计划实际结束时间,作为统计起始和结束时间
            filters = {'sprint_id__in':sprint_id_list, 'is_delete':0}
            fields = ['id', 'start_time', 'finish_time']
            related_plans = SprintTestplan.objects.filter(**filters).values(*fields)
            if related_plans:
                statistic_start_time = related_plans.aggregate(Min('start_time'))['start_time__min']
                statistic_finish_time = related_plans.aggregate(Max('finish_time'))['finish_time__max']
                plan_id_list = related_plans.values_list('id', flat=True)
            else:
                result['msg'] =  '加载迭代统计信息失败：所选迭代项目未关联任何测试计划'
                result['success'] =  True
                return Response(result, status.HTTP_200_OK)

            if not statistic_start_time:
                result['msg'] =  '加载迭代统计信息失败：所选迭代项目关联的测试计划都还没开始执行'
                result['success'] =  True
                return Response(result, status.HTTP_200_OK)

            if not statistic_finish_time:
                statistic_finish_time = timezone.now() # 完成时间为空，计划都没执行完成，默认为当前时间

            ################################ 获取映射的组别 ################################
            related_group_list = SysGroupRelatedGroup.objects.filter(group_id__in=user_group_id_list).values_list('related_group_id', flat=True)
            if not related_group_list:
                result['msg'] =  '加载迭代统计信息失败：未获取到所选组别映射的组别'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            ################################ 缺陷状态统计 ################################
            zengtao_query_tool = ZentaoQueryTool()
            query_result = zengtao_query_tool.get_defect_status_doughnut_pie_statistics(statistic_start_time, statistic_finish_time, related_group_list)
            if not query_result['success']:
                result['msg'] =  '加载迭代统计信息失败：' + query_result['msg']
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                sprints_statistics['defectStatusPie'] = query_result['dataForPie']

            ################################ 缺陷级别统计 ################################
            query_result = zengtao_query_tool.get_defect_severity_doughnut_pie_statistics(statistic_start_time, statistic_finish_time, related_group_list)
            if not query_result['success']:
                result['msg'] =  '加载迭代统计信息失败：' + query_result['msg']
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                sprints_statistics['defectSeverityPie'] = query_result['dataForPie']

            ################################# 用例通过率统计 ################################
            query_result = SprintTestreportAPIView.query_testcase_pass_rate_statistics(plan_id_list, user_group_id_list)
            if not query_result['success']:
                result['msg'] =  '加载迭代统计信息失败：' + query_result['msg']
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                sprints_statistics['casePassRatePie'] = query_result['dataForPie']

            ################################ 用例状态统计 ################################
            query_result = SprintTestreportAPIView.query_testcase_status_statistics(plan_id_list, user_group_id_list)
            if not query_result['success']:
                result['msg'] =  '加载迭代统计信息失败：' + query_result['msg']
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                sprints_statistics['caseStatusPie'] = query_result['dataForPie']

            ################################ 个人测试情况统计 ################################
            # 个人提交缺陷数统计
            query_result = zengtao_query_tool.query_individual_defect_statistics(statistic_start_time, statistic_finish_time, related_group_list)
            if not query_result['success']:
                result['msg'] =  '加载迭代统计信息失败：' + query_result['msg']
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                individual_defect_statistics = query_result['defect_statistics']

            # 个人用例执行情况统计
            query_result = SprintTestreportAPIView.query_individual_testcase_statistics(plan_id_list, user_group_id_list)
            if not query_result['success']:
                result['msg'] =  '加载迭代统计信息失败：' + query_result['msg']
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                individual_testcase_statistics = query_result['testcase_statistics']

            # 汇总个人测试情况统计数据
            for item in individual_testcase_statistics:
                value = item['related_account']
                if value in individual_defect_statistics:
                    item['defect_created'] = individual_defect_statistics[value]['defect_created']
                    individual_defect_statistics.pop(value)
                else:
                    item['defect_created'] = 0
            sprints_statistics['individualTestStatistics'] = individual_testcase_statistics

            # 继续汇总没有在平台建立关联账号的缺陷数据
            for account, value in individual_defect_statistics.items():
                temp = {}
                temp['username'] = value['realname']
                temp['testcase_assigned'] = 0
                temp['testcase_executed'] = 0
                temp['testcase_passed'] = 0

                testcase_execution_rate = '0.00'
                testcase_pass_rate = '0.00'
                temp['testcase_execution_rate'] = testcase_execution_rate
                temp['testcase_pass_rate'] = testcase_pass_rate
                temp['related_account'] = account
                temp['defect_created'] = value['defect_created']

                sprints_statistics['individualTestStatistics'].append(temp)

            # 排序
            sprints_statistics['individualTestStatistics'].sort(key= lambda item:item['defect_created'], reverse=True) # 默认按提交缺陷数降序排序

            ################################ 组别测试情况统计 ################################
            # 组别提交缺陷数统计
            query_result = zengtao_query_tool.query_product_defect_statistics(statistic_start_time, statistic_finish_time, related_group_list)
            if not query_result['success']:
                result['msg'] = '加载迭代统计信息失败：' + query_result['msg']
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                group_defect_statistics = query_result['defect_statistics']

            # 组别用例执行情况统计
            query_result = SprintTestreportAPIView.query_product_testcase_statistics(plan_id_list, user_group_id_list)
            if not query_result['success']:
                result['msg'] = '加载迭代统计信息失败：' + query_result['msg']
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                group_testcase_statistics = query_result['testcase_statistics']

            # 汇总组别测试情况统计数据
            for item in group_testcase_statistics:
                item['defect_created'] = 0
                related_groups = item['related_groups']
                if related_groups:
                    temp_related_group_list = related_groups.split(',')

                    for related_group in temp_related_group_list:
                        key = int(related_group)
                        if key in group_defect_statistics:
                            item['defect_created'] += group_defect_statistics[key]['defect_created']
                            group_defect_statistics.pop(key)

            sprints_statistics['groupTestStatistics'] = group_testcase_statistics

            # 继续汇总没有在平台建立关联组别的缺陷数据
            for id, value in group_defect_statistics.items():
                temp = {}
                temp['groupname'] = value['name']
                temp['testcase_assigned'] = 0
                temp['testcase_executed'] = 0
                temp['testcase_passed'] = 0

                testcase_execution_rate = '0.00'
                testcase_pass_rate = '0.00'
                temp['testcase_execution_rate'] = testcase_execution_rate
                temp['testcase_pass_rate'] = testcase_pass_rate
                temp['related_groups'] = id
                temp['defect_created'] = value['defect_created']

                sprints_statistics['groupTestStatistics'].append(temp)

            # 排序
            sprints_statistics['groupTestStatistics'].sort(key=lambda item:item['defect_created'], reverse=True) # 默认按提交缺陷数降序排序

            ################################ 组别缺陷状态统计 ################################
            # 查询映射的组别
            query_sql = 'SELECT t1.related_group_id as id, t1.group_id AS sys_group_id, t2.name AS sys_group_name ' \
                        'FROM tb_sys_group_related_group AS t1 ' \
                        'JOIN tb_sys_group AS t2 ON t1.group_id = t2.id AND t2.id IN (%s)' % ','.join(user_group_id_list)
            query_result = SysGroupRelatedGroup.objects.raw(query_sql)
            group_map_dict = {}
            for item in query_result:
                key = int(item.id)
                group_map_dict[key] = {'sys_group_id': item.sys_group_id, 'sys_group_name': item.sys_group_name}

            # 查询组别缺陷状态统计数据
            query_result = zengtao_query_tool.query_group_defect_status_statistics(statistic_start_time, statistic_finish_time, group_map_dict, related_group_list)
            if not query_result['success']:
                result['msg'] = '加载迭代统计信息失败：' + query_result['msg']
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                sprints_statistics['groupDefectStatusBar'] = query_result['dataForBar']

            ################################ 组别缺陷趋势图统计 ################################
            # 先判断是否已经在系统平台数据库中录入了禅道组别缺陷趋势统计数据
            obj = ZentaoGroupDefectTrendDailyStatistics.objects.first()
            if not obj:
                zengtao_query_tool.make_up_group_defect_trend_data(date.today(), 180) # 补录近6个月的数据 每个月的天数按30天计算

            statistic_start_time = (timezone.now() - timedelta(days=14)).strftime('%Y-%m-%d')
            statistic_finish_time = (timezone.now() - timedelta(days=1)).strftime('%Y-%m-%d')

            query_result = SprintTestreportAPIView.query_group_defect_trend_statistics(statistic_start_time, statistic_finish_time, group_map_dict, related_group_list)
            if not query_result['success']:
                result['msg'] = '加载组别缺陷趋势图统计失败：' + query_result['msg']
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                sprints_statistics['groupDefectTrendLine'] = query_result['dataForLine']

            result['msg'] =  ''
            result['success'] =  True
            result['data'] = sprints_statistics
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class GroupDefectTrendStatisticsAPIView(APIView):
    '''
    工作台-按时间段和组别查询组别缺陷趋势统计
    '''


    def get(self, request, format=None):
        '''按时间段和和组别查询组别缺陷趋势统计'''

        result = {}
        statistics = {} # 存放迭代相关统计数据
        try:
            data = request.GET
            user_group_ids = data.get('userGroupIds')
            user_group_id_list = user_group_ids.split(',')
            statistic_start_time = data.get('statisticStartTime')
            statistic_finish_time = data.get('statisticFinishTime')


            ################################ 获取映射的组别 ################################
            related_group_list = SysGroupRelatedGroup.objects.filter(group_id__in=user_group_id_list).values_list('related_group_id', flat=True)
            if not related_group_list:
                result['msg'] =  '获取组别缺陷趋势统计信息失败：未获取到所选组别映射的组别'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            ################################ 组别缺陷趋势图统计 ################################
           # 查询映射的组别
            query_sql = 'SELECT t1.related_group_id as id, t1.group_id AS sys_group_id, t2.name AS sys_group_name ' \
                        'FROM tb_sys_group_related_group AS t1 ' \
                        'JOIN tb_sys_group AS t2 ON t1.group_id = t2.id AND t2.id IN (%s)' % ','.join(user_group_id_list)
            query_result = SysGroupRelatedGroup.objects.raw(query_sql)

            group_map_dict = {}
            for item in query_result:
                key = int(item.id)
                group_map_dict[key] = {'sys_group_id': item.sys_group_id, 'sys_group_name': item.sys_group_name}

            zengtao_query_tool = ZentaoQueryTool()
            # 先判断是否已经在系统平台数据库中录入了禅道组别缺陷趋势统计数据
            obj = ZentaoGroupDefectTrendDailyStatistics.objects.first()
            if not obj:
                zengtao_query_tool.make_up_group_defect_trend_data(date.today(), 180) # 补录近6个月的数据 每个月的天数按30天计算

            query_result = SprintTestreportAPIView.query_group_defect_trend_statistics(statistic_start_time, statistic_finish_time, group_map_dict, related_group_list)
            if not query_result['success']:
                result['msg'] = '加载组别缺陷趋势图统计失败：' + query_result['msg']
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                statistics['groupDefectTrendLine'] = query_result['dataForLine']

            result['msg'] =  ''
            result['success'] =  True
            result['data'] = statistics
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
