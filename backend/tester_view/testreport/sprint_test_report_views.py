#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'


import json
import shortuuid
import os
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction
from django.utils import timezone
from django.core import serializers
from django.http import FileResponse
from django.core.cache import cache
from django.conf import settings
from backend.conf.config import DEFECT_SEVERITY_MAP, DEFECT_STATUS_MAP

from backend.models import Sprint
from backend.models import Product
from backend.models import ProjectVersionAssociated

from backend.models import SprintTestReport
from backend.models import SprintTestReportUnclosedDefectStatistics
from backend.models import SprintPDFTestReport
from backend.serializers import SprintTestReportSerializer
from backend.utils import utils
from .sprint_test_report_utils import SprintTestReportStatisticsUtils


logger = logging.getLogger('mylogger')


class SprintTestReportsDetailsAPIView(APIView):
    '''
    按字段，批量获取某个迭代的迭代测试报告信息
    '''

    # 查询详情
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            fields = params.get('fields')
            sprint_id = params.get('sprintId')
            sort = params.get('sort')
            if fields:
                fields = fields.split(',')
            else:
                fields = ['id', 'title']
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            filters = {'is_delete':0, 'sprint_id':sprint_id}
            rows = SprintTestReport.objects.filter(**filters).order_by(*sort_list).values(*fields)
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = rows
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SprintTestReportStatisticsAPIView(APIView):
    @staticmethod
    def get_associated_project_versions_by_sprint_id(sprint_id):
        '''获取关联项目版本信息'''
        sql =  'SELECT pva.id, pva.platform_project_version_id AS version_id, platform ' \
               'FROM tb_project_version_associated AS pva JOIN tb_project_version AS pv ON pva.project_version_id=pv.id AND pv.is_delete=0 AND pv.sprint_id=%s ' \
               'WHERE pv.is_delete=0 '% sprint_id
        query_rows = ProjectVersionAssociated.objects.raw(sql)
        return query_rows


    def post(self, request, format=None):
        '''生成迭代测试报告统计数据'''

        result = {}
        report_data = {} # 存放用于展示报告的相关数据
        report_db_data = {} # 存放存储到数据库的报告相关数据

        try:
            data = request.data
            sprint_id = data.get('sprint_id')
            report_db_data['sprint_id'] = sprint_id
            testplan_id_list = data.get('plan_ids')
            project_list = data.get('projects')
            project_version_list = data.get('project_versions')

            plan_selected = True # 标记前端是否选中了计划 True 选中了 False 未选中
            project_selected = True # 标记前端是否选中了项目 True 选中了 False 未选中
            version_selected = True # 标记前端是否选中了项目版本  True 选中了 False 未选中

            cache_key = '%s_%s_sprint_function_test_report' % (sprint_id, request.user.id)

             # 获取迭代信息
            sprint = Sprint.objects.filter(id=sprint_id).first()
            if not sprint:
                cache.delete(cache_key)
                result['msg'] =  '获取统计数据失败：未找到当前迭代'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)


            # 获取关联产品
            product = Product.objects.filter(id=sprint.product_id).first()
            if not product:
                cache.delete(cache_key)
                result['msg'] =  '获取统计数据失败：未找到当前产品'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            # 获取测试计划
            if testplan_id_list:
                testplan_list = SprintTestReportStatisticsUtils.get_testplans_by_testplan_ids(testplan_id_list)
            else:
                testplan_list = SprintTestReportStatisticsUtils.get_testplans_by_sprint_id(sprint_id)
                plan_selected = False

            testplan_id_list = []
            for item in testplan_list:
                testplan_id_list.append(item['id'])
                item['case_num_unexecuted'] = item['case_num_related'] - item['case_num_executed']
                if item['case_num_related']:
                    item['progress'] =  str(round((item['case_num_executed'] - item['case_num_blocked']) / item['case_num_related']*100))
                    item['pass_rate'] =  str(round(item['case_num_success'] / item['case_num_related']*100))
                else:
                    item['progress'] = '0'
                    item['pass_rate'] = '0'

            if not project_list:
                project_selected = False

            # 获取迭代、计划、项目id、项目版本id获取关联的项目，项目版本，关联项目，关联项目版本及关联项目所在平台,字段映射等信息
            if project_version_list: # 前端有选中项目版本 # 根据项目版本id获取
                projects_with_versions_info_dict = SprintTestReportStatisticsUtils.get_projects_with_versions_info_by_version_ids(project_version_list)
            elif not (plan_selected and project_selected): # 前端未选中任何计划，任何项目,及任何项目版本 # 通过迭代id获取
                projects_with_versions_info_dict = SprintTestReportStatisticsUtils.get_projects_with_versions_info_by_sprint_id(sprint_id)
                version_selected = False
            elif plan_selected and not project_selected :# 前端有选中计划，但是未选中任何项目，及任何项目版本 # 根据选中计划获取
                projects_with_versions_info_dict = SprintTestReportStatisticsUtils.get_projects_with_versions_info_by_plan_ids(testplan_id_list)
                version_selected = False
            else:# 有选中计划，项目，但是为选中任何项目版本 # 根据选中项目获取
                projects_with_versions_info_dict = SprintTestReportStatisticsUtils.get_projects_with_versions_info_by_project_ids(','.join(project_list))
                version_selected = False

            zentao_project_version_ids_dict = {'projects':[], 'versions':[]}  # 用于存放禅道项目及项目版本id
            jira_project_version_id_dict = {}  # 用于存放jira项目版本id
            project_defect_field_map = {} # 用于存放平台项目缺陷字段映射信息

            for item in projects_with_versions_info_dict:
                item = item.__dict__
                platform_project_id = item.get('platform_project_id')
                platform = item.get('platform')
                defect_custom_field_map = item.get('custom_field_map')
                defect_status_map = item.get('defect_status_map')
                defect_severity_map = item.get('defect_severity_map')
                defect_issue_type_id = item.get('defect_issue_type_id')
                platform_project_version_id = item.get('platform_project_version_id')

                if platform_project_id not in project_defect_field_map:
                    project_defect_field_map[platform_project_id] = {'defect_severity_map':DEFECT_SEVERITY_MAP, 'defect_status_map':DEFECT_STATUS_MAP, 'defect_custom_field_map':{}}

                if defect_status_map:
                    defect_status_map = json.loads(defect_status_map.strip(), encoding='utf-8')
                    project_defect_field_map[platform_project_id]['defect_status_map'].update(defect_status_map)

                if defect_severity_map:
                    defect_severity_map = json.loads(defect_severity_map.strip(), encoding='utf-8')
                    project_defect_field_map[platform_project_id]['defect_severity_map'].update(defect_severity_map)

                if defect_custom_field_map:
                    defect_custom_field_map = json.loads(defect_custom_field_map, encoding='utf-8')
                    project_defect_field_map[platform_project_id]['defect_custom_field_map'].update(defect_custom_field_map)

                if platform == 'jira':
                    if platform_project_id not in jira_project_version_id_dict:
                        jira_project_version_id_dict[platform_project_id] = {'versions':[], 'issue_type_id': defect_issue_type_id}
                    jira_project_version_id_dict[platform_project_id]['versions'].append(platform_project_version_id)
                elif platform == 'zentao':
                    if platform_project_id not in zentao_project_version_ids_dict['projects']:
                        zentao_project_version_ids_dict['projects'].append(platform_project_id)

                    if platform_project_version_id not in zentao_project_version_ids_dict['versions']:
                        zentao_project_version_ids_dict['versions'].append(platform_project_version_id)


            ################################ 生成报告标题 ################################
            curr_time_str = timezone.now().strftime('%Y%m%d%H%M%S')
            title =  '%s %s测试报告%s' % (product.name, sprint.name, curr_time_str)
            report_data['title'] = title
            report_db_data['title'] = title

            # ################################ 生成引言 ################################
            introduction = '报告针对 "%s" "%s"迭代测试情况汇总统计，内容涵盖测试结论、建议、风险分析，测试计划执行情况、测试范围描述、测试统计，遗留缺陷等，方便团队了解当前产品质量，识别产品上线风险' % (product.name, sprint.name)
            report_data['introduction'] = introduction
            report_db_data['introduction'] = introduction

            # ################################ 测试结论 ################################
            report_data['conclusion'] = '请填写测试结论'
            report_db_data['conclusion'] = report_data['conclusion']

            # ################################ 相关建议 ################################
            report_data['suggestion'] = '暂无'
            report_db_data['suggestion'] = '暂无'

            # ################################ 风险分析 ################################
            report_data['risk_analysis'] = '暂无'
            report_db_data['risk_analysis'] = '暂无'

            # ################################ 测试范围 ################################
            report_data['testScope'] = '请填写测试范围(如果无特殊情况，建议填写已测试的转测内容)'
            report_db_data['test_scope'] = report_data['testScope']

            # ################################ 测试计划 ################################
            report_data['relatedPlans'] = testplan_list
            report_db_data['related_plans'] = json.dumps(testplan_list, ensure_ascii=True )

            ################################ 测试统计 ################################
            # 获取禅道用户数据
            zen_users = SprintTestReportStatisticsUtils.get_zentao_users()

            # 获取缺陷数据
            all_defects = SprintTestReportStatisticsUtils.get_all_defects(jira_project_version_id_dict, zentao_project_version_ids_dict, version_selected)
            res = SprintTestReportStatisticsUtils.analyze_defect_data(all_defects, project_defect_field_map, zen_users)
            if not res.get('success'):
                result['msg'] =  '获取统计数据失败：%s' % res.get('error')
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)
            error_info = res.get('error')


            # 缺陷状态饼图统计数据
            defect_status_pie_data = res.get('defect_status_pie_data')
            report_data['defectStatusPie'] = defect_status_pie_data
            report_db_data['defect_status_pie'] = json.dumps(defect_status_pie_data, ensure_ascii=True )

            # 缺陷级别统计
            defect_severity_pie_data = res.get('defect_severity_pie_data')
            report_data['defectSeverityPie'] = defect_severity_pie_data
            report_db_data['defect_severity_pie'] = json.dumps(defect_severity_pie_data, ensure_ascii=True )

            # 缺陷类型统计
            defect_type_pie_data = res.get('defect_type_pie_data')
            report_data['defectTypePie'] = defect_type_pie_data
            report_db_data['defect_type_pie'] = json.dumps(defect_type_pie_data, ensure_ascii=True )

            # 缺陷根源分组统计
            defect_source_bar_data =  res.get('defect_source_bar_data')
            report_data['defectSourceBar'] = defect_source_bar_data
            report_db_data['defect_source_bar'] = json.dumps(report_data['defectSourceBar'], ensure_ascii=True)

            # 个人缺陷提交统计
            defects_created_by_individual = res.get('defects_created_by_individual')
            report_data['defects_created_individual'] = defects_created_by_individual
            report_db_data['defects_created_individual'] = json.dumps(defects_created_by_individual, ensure_ascii=True)

            # 个人缺陷处理统计
            defects_resolved_by_individual = res.get('defects_resolved_by_individual')
            report_data['defects_resolved_individual'] = defects_resolved_by_individual
            report_db_data['defects_resolved_individual'] = json.dumps(defects_resolved_by_individual, ensure_ascii=True)

            # 遗留缺陷统计
            defects_unclosed = res.get('defects_unclosed')
            report_data['unclosedDefects'] = defects_unclosed
            report_db_data['unclosed_defects'] = json.dumps(defects_unclosed, ensure_ascii=True)

            # 用例执行统计饼图
            query_result = SprintTestReportStatisticsUtils.get_testcase_execution_statistics(testplan_id_list)
            if not query_result['success']:
                cache.delete(cache_key)
                result['msg'] =  '获取统计数据失败：' + query_result['msg']
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                report_data['caseExecutionPie'] = query_result['dataForPie']
                report_db_data['case_execution_pie'] = json.dumps(report_data['caseExecutionPie'], ensure_ascii=True )

            # 个人用例执行统计
            query_result = SprintTestReportStatisticsUtils.get_case_execution_individual_statistics(testplan_id_list)
            if not query_result['success']:
                cache.delete(cache_key)
                result['msg'] =  '获取统计数据失败：' + query_result['msg']
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                report_data['case_execution_individual'] = query_result['case_execution_individual_statistics']
                report_db_data['case_execution_individual'] = json.dumps(report_data['case_execution_individual'], ensure_ascii=True )


            report_db_data['creater_id'], report_data['creater_id'] = request.user.id, request.user.id
            report_db_data['creater_name'], report_data['creater_name'] = request.user.name, request.user.name

            report_db_data['updater_id'], report_data['updater_id'] = request.user.id, request.user.id
            report_db_data['updater_name'], report_data['updater_name'] = request.user.name, request.user.name
            report_db_data['is_delete'], report_data['is_delete'] = 0, 0

            # 临时存储查询结果
            cache_key = '%s_%s_sprint_func_test_report' % (sprint_id, request.user.id)
            temp_report_data = {'reportRecordForDb':report_db_data, 'reportDataForDisplay':report_data}
            cache.set(cache_key, temp_report_data, timeout=600)

            result['msg'] =  '获取统计数据成功'
            result['success'] =  True
            result['data'] = report_data
            result['msg'] = error_info
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SprintTestReportAPIView(APIView):
    '''
    测试视图-测试报告管理-迭代测试报告，新增迭代测试报告
    '''

    def post(self, request, format=None):
        '''生成(新增）迭代测试报告'''

        result = {}
        try:
            data = request.data
            sprint_id = data.get('sprint_id')

            # 保存报告
            try:
                cache_key = '%s_%s_sprint_func_test_report' % (sprint_id, request.user.id)
                temp_report_data = cache.get(cache_key)
                if not temp_report_data:
                    result['msg'] =  '生成报告失败：获取统计数据失败，请重新查询统计数据后再试'
                    result['success'] =  False
                    return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

                report_db_data = temp_report_data['reportRecordForDb']
                report_data = temp_report_data['reportDataForDisplay']

                with transaction.atomic():
                    serializer = SprintTestReportSerializer(data=report_db_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    sprint_report_id = serializer.data.get('id')
                    # 保存报告关联的缺陷列表&遗留缺陷DI值获取
                    for item in report_data['unclosedDefects']:
                        # item['severity'] = defect_severity_map[item['severity']]
                        item['sprint_report_id'] = sprint_report_id
                        defect = SprintTestReportUnclosedDefectStatistics(**item)
                        defect.save()
            except Exception as e:
                result['msg'] =  '生成报告失败：%s' % e
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

            report_data['id'] =sprint_report_id
            result['msg'] =  '生成报告成功'
            result['success'] =  True
            result['data'] = report_data
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



    def get(self, request, format=None):
        '''查看迭代测试报告'''

        result = {}
        report_data = {} # 存放用于展示报告的相关数据
        try:
            data = request.GET
            sprint_report_id = data.get('reportId')

            sprint_report = SprintTestReport.objects.filter(id=sprint_report_id)
            if sprint_report.first():
                try:
                    report_data = sprint_report.values()[0]
                    temp_keys =  [ 'related_plans', 'requirement_pie', 'defect_status_pie', 'defect_severity_pie', 'defect_type_pie',
                                  'case_execution_pie', 'defect_source_bar', 'case_execution_individual','defects_created_individual',
                                  'defects_resolved_individual']
                    for key in temp_keys:
                        if key in report_data:
                            if report_data[key]:
                                report_data[key] = json.loads(report_data[key])

                    report_data['create_time'] = report_data['create_time'].strftime('%Y-%m-%d %H:%M:%S')
                    report_data['update_time'] = report_data['update_time'].strftime('%Y-%m-%d %H:%M:%S')

                    # 获取遗留缺陷
                    query_sql = 'SELECT id, t.defect_id, t.title, ' \
                                't.severity, ' \
                                't.status, t.remark, t.creater, t.assigned_to, t.person_liable, t.resolver, t.platform ' \
                                'FROM tb_sprint_testreport_unclosed_defect_statistics AS t ' \
                                'WHERE t.sprint_report_id = %s ' \
                                'ORDER BY t.severity' % sprint_report_id

                    defects = SprintTestReportUnclosedDefectStatistics.objects.raw(query_sql)
                    defects = json.loads(serializers.serialize('json', defects), encoding='utf-8')

                    temp_defect_list = []
                    if defects:
                        for item in defects:
                            temp_defect_list.append(item['fields'])
                        defects = temp_defect_list
                    report_data['unclosedDefects'] = defects
                except Exception as e:
                    result['msg'] =  '获取报告失败：%s' % e
                    result['success'] =  False
                    return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

            result['msg'] =  '获取报告成功'
            result['success'] =  True
            result['data'] = report_data
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


    # 修改报告
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['updater_id'] = request.user.id
            data['updater_name'] = request.user.name
            report_id = data.get('report_id')

            obj = SprintTestReport.objects.filter(id=report_id).first()
            target_item = utils.string_hump_to_underline(data['target_item'])
            data[target_item] = data['value']
            data['if_regenerate_pdf'] = 1
            data.pop('target_item')
            data.pop('value')
            data.pop('report_id')
            if obj:
                try:
                    with transaction.atomic():
                        serializer = SprintTestReportSerializer(obj, data=data, partial=True)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()

                        SprintPDFTestReport.objects.filter(testreport_id=report_id,is_delete=0).update(is_delete = 1)
                except Exception as e:
                    result['msg'] =  '修改失败：%s' % e
                    result['success'] =  False
                    return Response(result, status.HTTP_400_BAD_REQUEST)
            else:
                result['msg'] = '修改失败,报告不存在'
                result['success'] =  False
                return Response(request, status.HTTP_404_NOT_FOUND)

            result['msg'] =  '修改成功'
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


class SprintTestreportPDFAPIView(APIView):
    '''迭代测试报告pdf文件下载'''

    def post(self, request, format=None):
        '''下载pdf格式报告'''

        result = {}
        try:
            data = request.data
            sprint_report_id = data.get('report_id')
            sprint_report = SprintTestReport.objects.filter(id=sprint_report_id)
            if sprint_report.first():
                if_regenerate_pdf = sprint_report.first().if_regenerate_pdf

                # 获取pdf报告信息
                pdf_report_obj = SprintPDFTestReport.objects.filter(testreport_id=sprint_report_id, is_delete=0).first()
                if not if_regenerate_pdf and pdf_report_obj:
                    file_absolute_path =  settings.MEDIA_ROOT.rstrip('/') + pdf_report_obj.file_path # pdf_report_obj.file_path 以 / 打头
                    if os.path.exists(file_absolute_path) and os.path.isfile(file_absolute_path):
                        file = open(file_absolute_path, 'rb')
                        file_response = FileResponse(file)
                        file_response['Content-Type']='application/octet-stream'
                        file_response['Content-Disposition']='attachment;filename={}.pdf'.format(pdf_report_obj.name) # 不知道为啥，前端获取不到请求头Content-Disposition
                        return file_response

                echart_base64_info_dict = data.get('echart_base64_info')

                # 读取迭代测试报告html模板
                report_html_str = '' # 存放html格式的迭代测试报告

                current_dir, tail = os.path.split(os.path.abspath(__file__))
                template_file = 'sprint_test_report/sprint_test_report_template.html'
                template_filepath = os.path.normpath(os.path.join(current_dir, template_file))
                with open(template_filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        report_html_str += line

                # 读取报告数据
                try:
                    field_list =  ['title', 'introduction',  'test_scope', 'conclusion', 'suggestion',  'risk_analysis']
                    report_data = sprint_report.values('title','introduction', 'related_plans', 'test_scope', 'case_execution_individual',
                                                       'defects_created_individual','defects_resolved_individual', 'conclusion', 'suggestion',  'risk_analysis')[0]

                    # 替换模板中对应项
                    # 替换标题,引言，测试范围，测试结论，相关建议，风险分析
                    for field in field_list:
                        report_html_str = report_html_str.replace('${%s}' % field, report_data[field])

                    # 替换测试计划
                    related_plans = json.loads(report_data['related_plans'])
                    related_plans = SprintTestReportStatisticsUtils.convert_related_plans_to_html(related_plans)
                    report_html_str = report_html_str.replace('${related_plans}', related_plans)

                    echarts_may_not_exists_dict = {'defect_source_bar':SprintTestReportStatisticsUtils.convert_defect_source_bar_to_html}

                    # 替换一定存在的echart图(4个统计饼图)
                    for key, value in echart_base64_info_dict.items():
                        if key not in echarts_may_not_exists_dict:
                            report_html_str = report_html_str.replace('${%s}' % key, value)

                    # 替换其它echart图（可能不存在）
                    for key, func in echarts_may_not_exists_dict.items():
                        report_html_str = report_html_str.replace('${%s}' % key, func(echart_base64_info_dict.get(key)))

                    # 替换个人用例执行统计
                    case_execution_individual = json.loads(report_data['case_execution_individual'])
                    case_execution_individual = SprintTestReportStatisticsUtils.convert_case_execution_individual_to_html(case_execution_individual)
                    report_html_str = report_html_str.replace('${case_execution_individual}', case_execution_individual)


                    # 替换个人提交缺陷数据统计
                    defects_created_individual = json.loads(report_data['defects_created_individual'])
                    defects_created_individual = SprintTestReportStatisticsUtils.convert_defects_created_individual_to_html(defects_created_individual)
                    report_html_str = report_html_str.replace('${defects_created_individual}', defects_created_individual)

                    # 替换个人处理缺陷数据
                    defects_resolved_individual = json.loads(report_data['defects_resolved_individual'])
                    defects_resolved_individual = SprintTestReportStatisticsUtils.convert_defects_resolved_individual_to_html(defects_resolved_individual)
                    report_html_str = report_html_str.replace('${defects_resolved_individual}', defects_resolved_individual)

                    # 获取遗留缺陷
                    query_sql = 'SELECT id, t.defect_id, t.title, severity,t.status, ' \
                                't.remark, t.creater, t.assigned_to, t.resolver, t.platform ' \
                                'FROM tb_sprint_testreport_unclosed_defect_statistics AS t ' \
                                'WHERE t.sprint_report_id = %s ' \
                                'ORDER BY t.severity' % sprint_report_id

                    unclosed_defect_statistics = SprintTestReportUnclosedDefectStatistics.objects.raw(query_sql)
                    unclosed_defect_statistics = json.loads(serializers.serialize('json', unclosed_defect_statistics), encoding='utf-8')

                    temp_defect_list = []
                    if unclosed_defect_statistics:
                        for item in unclosed_defect_statistics:
                            temp_defect_list.append(item['fields'])
                        unclosed_defect_statistics = temp_defect_list

                    # 替换未关闭缺陷
                    unclosed_defect_statistics = SprintTestReportStatisticsUtils.convert_unclosed_defect_statistics_to_html(unclosed_defect_statistics)
                    report_html_str = report_html_str.replace('${unclosed_defects}', unclosed_defect_statistics)


                    # 生成pdf文档
                    time_str = timezone.now().strftime('%Y%m%d')
                    file_name = shortuuid.uuid() + time_str + '.pdf'
                    temp_result = utils.html_str_to_pdf_file(report_html_str, file_name)

                    # 返回数据给前端
                    if temp_result[0]:
                        file_absolute_path = temp_result[1]
                        if os.path.exists(file_absolute_path) and os.path.isfile(file_absolute_path):
                            relative_file_path = '/sprint/testreport/%s' % file_name
                            old_pdf_report_file_path = ''

                            with transaction.atomic():
                                # 存储pdf报告信息到数据库
                                pdf_report_obj = SprintPDFTestReport.objects.filter(testreport_id=sprint_report_id, is_delete=0).first()
                                if pdf_report_obj:
                                    old_pdf_report_file_path = pdf_report_obj.file_path

                                    pdf_report_obj.name=report_data['title']
                                    pdf_report_obj.file_path=relative_file_path
                                    pdf_report_obj.updater_id=request.user.id
                                    pdf_report_obj.updater = request.user.name
                                    pdf_report_obj.save()
                                else:
                                    obj = SprintPDFTestReport(testreport_id=sprint_report_id, name=report_data['title'], file_path=relative_file_path, creater=request.user.name, creater_id=request.user.id,  updater_id=request.user.id,  updater=request.user.name, is_delete=0)
                                    obj.save()

                                # 重置迭代测试报告是否重新生成pdf标记为0
                                SprintTestReport.objects.filter(id=sprint_report_id, is_delete=0).update(if_regenerate_pdf=0)

                            # 删除旧的测试报告
                            if old_pdf_report_file_path:
                                old_pdf_report_file_path = settings.MEDIA_ROOT.rstrip('/') + '/%s' % old_pdf_report_file_path
                                if os.path.exists(old_pdf_report_file_path) and os.path.isfile(old_pdf_report_file_path):
                                    os.remove(old_pdf_report_file_path)

                            file = open(file_absolute_path, 'rb')
                            file_response = FileResponse(file)
                            file_response['Content-Type']='application/octet-stream'
                            file_response['Content-Disposition']='attachment;filename={}.pdf'.format(report_data['title'] ) # 不知道为啥，前端获取不到请求头Content-Disposition
                            return file_response
                        else:
                            result['msg'] =  '生成pdf报告失败'
                            result['success'] =  False
                            return Response(result, status.HTTP_400_BAD_REQUEST)
                    else:
                        result['msg'] =  temp_result[1]
                        result['success'] =  False
                        return Response(result, status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    result['msg'] =  '%s' % e
                    result['success'] =  False
                    return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                result['msg'] =  '生成迭代测试报告失败,报告不存在'
                result['success'] =  False
                return  Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)