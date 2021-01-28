#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
@CreateTime: 2020/09/17 10:21
@Author : shouke
'''

import logging
from backend.models import SprintTestplan
from backend.models import ProjectVersionAssociated
from backend.models import SprintTestplanTestcase
from backend.zentao.defect import ZentaoDefect
from backend.zentao.user import ZentaoUser
from backend.jira.defect import JiraDefect
from backend.conf.config import DEFECT_NOT_EFFECTIVE_FLAG, DEFECT_SUGGEST_FLAG, ZENTAO_DEFECT_CUSTOM_FIELD_MAP, DEFECT_TYPE_MAP, DEFECT_IS_HISTORY_MAP, DEFECT_SOURCE_MAP
from backend.conf.config import JIRA_ISSUE_BROWSE_BASE_URL, ZENTAO_BUG_BROWSE_BASE_URL

logger = logging.getLogger('mylogger')


class SprintTestReportStatisticsUtils:
    '''测试报告数据统计辅助工具'''

    @staticmethod
    def get_testplans_by_sprint_id(sprint_id):
        '''根据迭代id获取迭代关联的测试计划'''

        fields = ['id', 'name', 'begin_time', 'start_time', 'end_time', 'finish_time', 'project_names', 'env_names',
                  'status', 'case_num_related', 'case_num_executed', 'case_num_success', 'case_num_fail', 'case_num_blocked']
        testplans = SprintTestplan.objects.filter(sprint_id=sprint_id, is_delete=0).extra(select={'begin_time': "DATE_FORMAT(begin_time, '%%Y-%%m-%%d')",
                                                                                                  'end_time':"DATE_FORMAT(end_time, '%%Y-%%m-%%d')",
                                                                                                  'start_time':"DATE_FORMAT(start_time, '%%Y-%%m-%%d)",
                                                                                                  'start_time':"IFNULL(DATE_FORMAT(start_time, '%%Y-%%m-%%d %%H:%%I'),'')",
                                                                                                  'finish_time':"IFNULL(DATE_FORMAT(finish_time, '%%Y-%%m-%%d %%H:%%I'), '')"
                                                                                                  }).order_by('start_time').values(*fields)
        testplans = list(testplans)
        return testplans

    @staticmethod
    def get_testplans_by_testplan_ids(testplan_id_list):
        '''根据计划id获取迭代关联的计划信息'''

        fields = ['id', 'name', 'begin_time', 'start_time', 'end_time', 'finish_time', 'project_names', 'env_names',
                  'status', 'case_num_related', 'case_num_executed', 'case_num_success', 'case_num_fail', 'case_num_blocked']
        testplans = SprintTestplan.objects.filter(id__in=testplan_id_list, is_delete=0).extra(select={'begin_time': "DATE_FORMAT(begin_time, '%%Y-%%m-%%d')",
                                                                                                      'end_time':"DATE_FORMAT(end_time, '%%Y-%%m-%%d')",
                                                                                                      'start_time':"DATE_FORMAT(start_time, '%%Y-%%m-%%d)",
                                                                                                      'start_time':"IFNULL(DATE_FORMAT(start_time, '%%Y-%%m-%%d %%H:%%I'),'')",
                                                                                                      'finish_time':"IFNULL(DATE_FORMAT(finish_time, '%%Y-%%m-%%d %%H:%%I'), '')"
                                                                                                      }).order_by('start_time').values(*fields)
        testplans = list(testplans)
        return testplans

    @staticmethod
    def get_projects_with_versions_info_by_version_ids(version_id_list):
        '''根据项目版本id获取项目，项目版本，关联项目，关联项目版本及关联项目所在平台,字段映射等信息'''

        version_ids = str(version_id_list).replace('[', '(').replace(']', ')')

        query_sql = "SELECT DISTINCT t1.project_version_id, t1.id, t1.platform_project_version_id, t2.project_id, " \
                    "t3.platform_project_name, t3.platform_project_id, t1.platform, t3.defect_issue_type_id, t3.defect_status_map, t3.defect_severity_map, t3.custom_field_map " \
                    "FROM `tb_project_version_associated` AS t1 " \
                    "JOIN `tb_project_version` AS t2 ON t1.project_version_id = t2.id " \
                    "JOIN `tb_project_associated` AS t3 ON t2.project_id = t3.project_id " \
                    "WHERE t1.project_version_id IN %s;" % version_ids

        query_rows = ProjectVersionAssociated.objects.raw(query_sql)
        return query_rows

    @staticmethod
    def get_projects_with_versions_info_by_sprint_id(sprint_id):
        '''根据sprint_id获取项目，项目版本，关联项目，关联项目版本及关联项目所在平台,字段映射等信息'''

        query_sql = "SELECT DISTINCT t1.project_version_id, t1.id, t1.platform_project_version_id, t2.project_id, " \
                    "t3.platform_project_name, t3.platform_project_id, t1.platform, t3.defect_issue_type_id, t3.defect_status_map, t3.defect_severity_map, t3.custom_field_map " \
                    "FROM `tb_project_version_associated` AS t1 " \
                    "JOIN `tb_project_version` AS t2 ON t1.project_version_id = t2.id AND t2.is_delete=0 AND t2.sprint_id = %s " \
                    "JOIN `tb_project_associated` AS t3 ON t2.project_id = t3.project_id "  % sprint_id

        query_rows = ProjectVersionAssociated.objects.raw(query_sql)
        return query_rows

    @staticmethod
    def get_projects_with_versions_info_by_project_ids(project_ids_str):
        '''根据项目id列表获取项目，项目版本，关联项目，关联项目版本及关联项目所在平台,字段映射等信息'''

        query_sql = "SELECT DISTINCT t1.project_version_id, t1.id, t1.platform_project_version_id, t2.project_id, " \
                    "t3.platform_project_name, t3.platform_project_id, t1.platform, t3.defect_issue_type_id, t3.defect_status_map, t3.defect_severity_map, t3.custom_field_map " \
                    "FROM `tb_project_version_associated` AS t1 " \
                    "JOIN `tb_project_version` AS t2 ON t1.project_version_id = t2.id AND t2.is_delete=0 AND t2.project_id in (%s) " \
                    "JOIN `tb_project_associated` AS t3 ON t2.project_id = t3.project_id "  % project_ids_str

        query_rows = ProjectVersionAssociated.objects.raw(query_sql)
        return query_rows

    @staticmethod
    def get_projects_with_versions_info_by_plan_ids(testplan_id_list):
        '''根据测试计划id列表获取计划关联的项目，项目版本，关联项目，关联项目版本及关联项目所在平台,字段映射等信息'''
        project_ids_list = SprintTestplan.objects.filter(id__in=testplan_id_list).values_list('project_ids')
        project_ids_str = ','.join(project_ids_list)
        project_ids_str = ','.join(list(set(project_ids_str.split(','))))
        query_rows = []
        if project_ids_str:
            query_rows = SprintTestReportStatisticsUtils.get_projects_with_versions_info_by_project_ids(project_ids_str)
        return query_rows

    @staticmethod
    def get_zentao_users():
        query_rows = ZentaoUser.get_all_users()
        result = {}
        for item in query_rows:
            account = item.get('account')
            name = item.get('realname')
            result[account] = name
        return result


    @staticmethod
    def get_all_defects(jira_project_version_ids_dict, zentao_project_version_ids_dict, version_selected):
        ''' 获取所有缺陷数据 '''

        all_defects_dict = { 'jira':{}, 'zentao':[]}
        for project_id in jira_project_version_ids_dict:
            if project_id not in all_defects_dict:
                all_defects_dict['jira'][project_id] = []
            all_defects_dict['jira'][project_id].extend(JiraDefect.get_defects_by_version_ids(jira_project_version_ids_dict[project_id].get('versions'), jira_project_version_ids_dict[project_id].get('issue_type_id')))

        all_defects_dict['zentao'].extend(ZentaoDefect.get_defects_by_project_version_ids(zentao_project_version_ids_dict, version_selected))
        return all_defects_dict

    @staticmethod
    def analyze_defect_data(defects_dict, project_defect_field_map, zen_users):
        try:
            defect_status_num_dict = {'新建':0, '处理中':0, '已解决':0, '延期处理':0, '已拒绝':0, '重新打开':0, '已关闭':0}
            defect_severity_num_dict = {'致命':0, '严重':0, '一般':0, '轻微':0}
            defect_type_num_dict = {'界面缺陷':0, '功能缺陷':0, '性能缺陷':0, '其它缺陷':0}
            defect_history_num_dict = {'历史遗留':0, '非历史遗留':0}
            defect_source_num_dict = {}
            defect_di_map = {'致命':9, '严重':3, '一般':1, '轻微':0.1} # 缺陷密度值映射

            defect_total = 0 # 缺陷总数
            bug_total = 0  # bug类缺陷总数
            suggest_total = 0 # 建议类型缺陷总数
            error_info = set()

            defects_created_by_individual_dict = {} # 存放用户创建的缺陷记录
            defects_resolved_by_individual_dict = {} # 存放问题处理人解决的缺陷记录
            defects_unclosed = [] # 存放为关闭问题
            for platform in defects_dict:
                if platform == 'jira':
                    for project_id in defects_dict[platform]:
                        project_defects = defects_dict[platform][project_id]
                        defect_custom_field_map = project_defect_field_map[project_id]['defect_custom_field_map']
                        is_effective_field = defect_custom_field_map.get('is_effective')
                        severity_field = defect_custom_field_map.get('severity')
                        defect_type_field = defect_custom_field_map.get('defect_type')
                        person_liable_field = defect_custom_field_map.get('person_liable')
                        is_history_field = defect_custom_field_map.get('is_history')
                        defect_source_field = defect_custom_field_map.get('source')
                        is_online_field = defect_custom_field_map.get('is_online')
                        is_advice_field = defect_custom_field_map.get('is_advice')

                        defect_status_map = project_defect_field_map[project_id]['defect_status_map']
                        defect_severity_map = project_defect_field_map[project_id]['defect_severity_map']

                        for defect in project_defects:
                            defect_id = defect.get('id')
                            defect_extra_info_rows = JiraDefect.get_defect_custom_field_info(defect_id)
                            defect_extra_info_dict = {}
                            for item in defect_extra_info_rows:
                                custom_field = item.get('custom_field')
                                custom_field_value = item.get('cfvalue')
                                custom_field_value = custom_field_value.decode('utf-8') if custom_field_value else ''
                                defect_extra_info_dict[str(int(custom_field))] = custom_field_value

                            is_defect_effective = defect_extra_info_dict.get(is_effective_field)
                            if is_defect_effective:
                                is_defect_effective = str(is_defect_effective).lower()
                                res = [item for item in DEFECT_NOT_EFFECTIVE_FLAG if item.lower() in is_defect_effective]
                                if res: # 无效bug，不记录统计
                                    continue

                            creater_account = defect.get('createrAccount')
                            creater = defect.get('creater')
                            assigned_to_account = defect.get('assignedToAccount')
                            assigned_to = defect.get('assignedTo')
                            if creater_account not in defects_created_by_individual_dict:
                                defects_created_by_individual_dict[creater_account] = {'creater':creater, 'DI':0, 'total_created': 1, '致命':0, '严重':0, '一般':0, '轻微':0}
                            else:
                                defects_created_by_individual_dict[creater_account]['total_created'] += 1


                            is_advice = defect_extra_info_dict.get(is_advice_field)
                            if is_advice:
                                is_advice = str(is_advice).lower()
                                res = [item for item in DEFECT_SUGGEST_FLAG if item.lower() in is_advice]
                                if res: # 建议类型bug
                                    suggest_total += 1
                                else:
                                    bug_total += 1
                            else:
                                bug_total += 1

                            defect_total += 1
                            defect_status = defect.get('status')
                            project_name = defect.get('projectName')
                            try:
                                defect_status = defect_status_map[defect_status]
                                defect_status_num_dict[defect_status] += 1

                            except Exception as e:
                                error = '缺陷状态映射配置错误或者未配置(所在项目：%s，获取状态为：%s )<br/>' %  (project_name, defect_status)
                                error_info.add(error)
                                logger.error(error)

                            defect_person_liable = defect_extra_info_dict.get(person_liable_field)
                            person_liable_account = None
                            if defect_person_liable:
                                defect_person_liable, person_liable_account = defect_person_liable.split('__')

                            if person_liable_account and person_liable_account not in defects_resolved_by_individual_dict:
                                defects_resolved_by_individual_dict[person_liable_account] = {'resolver':defect_person_liable, 'DI':0, 'total_raised':1, 'total_resolved': '- -', '致命':0, '严重':0, '一般':0, '轻微':0}
                            elif person_liable_account:
                                defects_resolved_by_individual_dict[person_liable_account]['total_raised'] += 1

                            defect_severity = defect_extra_info_dict.get(severity_field)
                            try:
                                temp_defect_severity = defect_severity_map[defect_severity]
                                defect_severity_num_dict[temp_defect_severity] += 1
                                defects_created_by_individual_dict[creater_account][temp_defect_severity] += 1
                                defects_created_by_individual_dict[creater_account]['DI'] += defect_di_map[temp_defect_severity]
                                if person_liable_account:
                                    defects_resolved_by_individual_dict[person_liable_account][temp_defect_severity] += 1
                                    defects_resolved_by_individual_dict[person_liable_account]['DI'] += defect_di_map[temp_defect_severity]
                            except Exception as e:
                                error = '缺陷严重级别映射配置错误或者未配置(所在项目：%s，获取的级别为：%s )<br/>' %  (project_name, defect_severity)
                                defect_severity = '未获取'
                                error_info.add(error)
                                logger.error(error)

                            defect_type = defect_extra_info_dict.get(defect_type_field)
                            try:
                                temp_defect_type = DEFECT_TYPE_MAP[defect_type]
                                defect_type_num_dict[temp_defect_type] += 1
                            except Exception as e:
                                error = '缺陷类型映射配置错误或者未配置(所在项目：%s，获取的类型为：%s )<br/>' %  (project_name, defect_type)
                                error_info.add(error)
                                logger.error(error)


                            defect_history = defect_extra_info_dict.get(is_history_field)
                            if not defect_history:
                                defect_history = '0'
                            try:
                                temp_defect_history = DEFECT_IS_HISTORY_MAP[defect_history]
                                defect_history_num_dict[temp_defect_history] += 1
                            except Exception as e:
                                error = '缺陷是否历史遗留映射配置错误或者未配置(所在项目：%s，获取的遗留标识为：%s )<br/>' %  (project_name, defect_history)
                                error_info.add(error)
                                logger.error(error)

                            defect_source = defect_extra_info_dict.get(defect_source_field)
                            if defect_source is not None:
                                temp_defect_source = DEFECT_SOURCE_MAP.get(defect_source) # 如果存在映射则使用映射
                                if temp_defect_source:
                                    defect_source = temp_defect_source
                                if defect_source not in defect_source_num_dict:
                                    defect_source_num_dict[defect_source] = 1
                                else:
                                    defect_source_num_dict[defect_source] += 1
                            if defect_status != '已关闭':
                                defects_unclosed.append({'defect_id': int(defect['issuenum']), 'title':defect['title'], 'severity':defect_severity, 'status':defect_status, 'remark':defect_source or '', 'creater':creater ,
                                                         'assigned_to':assigned_to, 'person_liable': defect_person_liable , 'resolver':'--', 'platform':'jira'})
                elif platform == 'zentao':
                    for defect in defects_dict[platform]:
                        defect_status = defect.get('status')
                        defect_severity = defect.get('severity')
                        defect_resolution = defect.get('resolution')
                        defect_type = defect.get('type')
                        is_history = defect.get(ZENTAO_DEFECT_CUSTOM_FIELD_MAP.get('is_history'))
                        if is_history is None:
                            is_history = 0
                        person_liable_account = defect.get(ZENTAO_DEFECT_CUSTOM_FIELD_MAP.get('person_liable'))
                        is_advice = defect.get(ZENTAO_DEFECT_CUSTOM_FIELD_MAP.get('is_advice'))
                        defect_source = defect.get(ZENTAO_DEFECT_CUSTOM_FIELD_MAP.get('source'))
                        project_id = str(defect.get('projectID'))
                        project_name = defect.get('projectName')

                        temp_defect_resolution = str(defect_resolution).lower()
                        temp_defect_source = defect_source.lower()
                        res = [item for item in DEFECT_NOT_EFFECTIVE_FLAG if item.lower() in temp_defect_resolution or item.lower() in temp_defect_source]
                        if res: # 无效bug，不记录统计
                            continue

                        creater_account = defect.get('createrAccount')
                        creater = defect.get('creater')
                        assigned_to = defect.get('assignedTo')
                        resolver_account = defect.get('resolvedByAccount')
                        resolver = defect.get('resolver')
                        if creater_account not in defects_created_by_individual_dict:
                            defects_created_by_individual_dict[creater_account] = {'creater':creater, 'DI':0, 'total_created': 1, '致命':0, '严重':0, '一般':0, '轻微':0}
                        else:
                            defects_created_by_individual_dict[creater_account]['total_created'] += 1

                        if resolver_account and resolver_account not in defects_resolved_by_individual_dict:
                            defects_resolved_by_individual_dict[resolver_account] = {'resolver':resolver, 'DI':0, 'total_raised':0, 'total_resolved': 1, '致命':0, '严重':0, '一般':0, '轻微':0}
                        elif resolver_account:
                            defects_resolved_by_individual_dict[resolver_account]['total_resolved'] += 1

                        if person_liable_account and person_liable_account not in defects_resolved_by_individual_dict:
                            resolver_name = zen_users.get(person_liable_account)
                            if resolver_name:
                                defects_resolved_by_individual_dict[person_liable_account] = {'resolver':resolver_name, 'DI':0,  'total_raised':1, 'total_resolved': 0, '致命':0, '严重':0, '一般':0, '轻微':0}
                        elif person_liable_account in defects_resolved_by_individual_dict:
                            defects_resolved_by_individual_dict[person_liable_account]['total_raised'] += 1

                        if is_advice:
                            is_advice = str(is_advice).lower()
                            res = [item for item in DEFECT_SUGGEST_FLAG if item.lower() in is_advice]
                            if res: # 建议类型bug
                                suggest_total += 1
                            else:
                                bug_total += 1
                        else:
                            bug_total += 1

                        defect_total += 1
                        try:
                            temp_project_defect_field_map = project_defect_field_map[project_id]
                            try:
                                temp_defect_status = temp_project_defect_field_map['defect_status_map'][defect_status]
                                defect_status_num_dict[temp_defect_status] += 1
                            except Exception as e:
                                error = '缺陷状态映射配置错误或者未配置(所在项目：%s，获取的状态为：%s )<br/>' %  (project_name, defect_status)
                                error_info.add(error)
                                logger.error(error)

                            try:
                                temp_defect_severity = temp_project_defect_field_map['defect_severity_map'][defect_severity]
                                defect_severity_num_dict[temp_defect_severity] += 1
                                defects_created_by_individual_dict[creater_account][temp_defect_severity] += 1
                                defects_created_by_individual_dict[creater_account]['DI'] += defect_di_map[temp_defect_severity]
                                if person_liable_account in defects_resolved_by_individual_dict:
                                    defects_resolved_by_individual_dict[person_liable_account][temp_defect_severity] += 1
                                    defects_resolved_by_individual_dict[person_liable_account]['DI'] += defect_di_map[temp_defect_severity]
                            except Exception as e:
                                error = '缺陷严重级别映射配置错误或者未配置(所在项目：%s，获取的级别为：%s )<br/>' %  (project_name, defect_severity)
                                error_info.add(error)
                                logger.error(error)
                        except Exception as e:
                            error = '未获取到平台项目(项目：%s )缺陷映射配置</br>' % project_name
                            error_info.add(error)
                            logger.error(error)
                            continue

                        try:
                            temp_defect_type = DEFECT_TYPE_MAP[defect_type]
                            defect_type_num_dict[temp_defect_type] += 1
                        except Exception as e:
                            error = '缺陷类型映射配置错误或者未配置(所在项目：%s，类获取的类型为：%s )<br/>' %  (project_name, defect_type)
                            error_info.add(error)
                            logger.error(error)

                        try:
                            is_defect_history = DEFECT_IS_HISTORY_MAP[str(is_history)]
                            defect_history_num_dict[is_defect_history] += 1
                        except Exception as e:
                            error = '缺陷是否历史遗留映射配置错误或者未配置(所在项目：%s，获取的遗留标识为：%s )<br/>' %  (project_name, is_history)
                            error_info.add(error)
                            logger.error(error)

                        if defect_source is not None:
                            temp_defect_source = DEFECT_SOURCE_MAP.get(defect_source) # 如果存在映射则使用映射
                            if temp_defect_source:
                                defect_source = temp_defect_source
                            if defect_source not in defect_source_num_dict:
                                defect_source_num_dict[defect_source] = 1
                            else:
                                defect_source_num_dict[defect_source] += 1

                        if defect_status != '已关闭':
                            remark = ''
                            if defect_status == '已拒绝':
                                remark = defect['resolution']
                            defects_unclosed.append({'defect_id': defect['id'], 'title':defect['title'], 'severity':defect_severity, 'status':defect_status, 'remark':defect_source or remark, 'creater':creater ,
                                                     'assigned_to':assigned_to, 'person_liable': zen_users.get(defect.get('person_liable')) , 'resolver':defect['resolver'], 'platform':'禅道'})
                else:
                    pass

            #缺陷状态饼图所需数据
            defect_status_pie_data = {
                'centerText': "消缺率\n0%",
                'seriesData': [],
                'aroundTextConfig':[]
            }

            # 缺陷严重级别饼图所需数据
            defect_severity_pie_data = {
                'centerText': "总数\n%s" % defect_total,
                'seriesData': [],
                'aroundTextConfig':[]
            }

            # 缺陷类型饼图所需数据
            defect_type_pie_data = {
                'centerText': "建议数\n0",
                'seriesData': [],
                'aroundTextConfig':[]
            }

            # 缺陷根源分组柱状图所需数据
            defect_source_bar_data = {
                'seriesData': [],
                'yAxisData':['缺陷根源']
            }

            unclosed_defect_num = defect_total - defect_status_num_dict.get('已关闭')
            if defect_total:
                for num_dict, pie_data in [(defect_status_num_dict, defect_status_pie_data), (defect_severity_num_dict, defect_severity_pie_data),
                             (defect_type_num_dict, defect_type_pie_data)]:
                    for item in num_dict:
                        value = num_dict.get(item)
                        pie_data['seriesData'].append({'value':value, 'name': item, 'percent': '%.2f' % (value/defect_total * 100) })

                defect_status_pie_data["centerText"] = '消缺率\n%.2f%%' % (defect_status_num_dict['已关闭'] / defect_total * 100)
                unclosed_defect_percent =  '%.2f' % (unclosed_defect_num / defect_total * 100) # 未关闭缺陷占比
                advice_type_defect_percent =  '%.2f' % (suggest_total / defect_total * 100) # 建议类缺陷占比
                not_advice_type_defect_percent = '%.2f' % (100 - float(advice_type_defect_percent)) # 非建议类缺陷占比
                defect_type_pie_data["centerText"] = '建议\n%s' % suggest_total
                defect_history_percent =  '%.2f' % (defect_history_num_dict['历史遗留'] / defect_total * 100) # 建议类缺陷占比

                defect_source_num_list = sorted(defect_source_num_dict.items(), key=lambda arg:arg[1], reverse=True)
                for item in defect_source_num_list:
                    source, value = item
                    defect_source_bar_data['seriesData'].append({'name': source, 'type': 'bar', 'barMaxWidth':50, 'data': [value],
                        'itemStyle':{
                            'normal': {
                                'label': {
                                    'show':'true',
                                    'position': 'right',
                                    'formatter': source + ' %s' % value +  ' (%.1f%%)' % (value / defect_total * 100),
                                    'textStyle': {
                                        'color': 'black',
                                        'fontSize': 12
                                    }
                                }
                            }
                        }
                    })
            else:
                unclosed_defect_percent = '0'
                advice_type_defect_percent = '0'
                not_advice_type_defect_percent = '0'
                defect_history_percent = '0'
                for num_dict, pie_data in [(defect_status_num_dict, defect_status_pie_data), (defect_severity_num_dict, defect_severity_pie_data),
                             (defect_type_num_dict, defect_type_pie_data)]:
                    for item in num_dict:
                        value = num_dict.get(item)
                        pie_data['seriesData'].append({'value':value, 'name': item, 'percent': '0' })

            defect_status_pie_data['aroundTextConfig'].append({
                        'type': "text",
                        'left': "left",
                        'bottom': 0,
                        'style': {
                            'fill': "#000",
                            'text': "总数：%s  未关闭：%s(%s%%)  历史遗留：%s(%s%%)" % (defect_total, unclosed_defect_num, unclosed_defect_percent, defect_history_num_dict['历史遗留'], defect_history_percent),
                            'font':'bolder 13px Microsoft YaHei'
                        }
                    })

            defect_type_pie_data['aroundTextConfig'].append({
                        'type': "text",
                        'left': "left",
                        'bottom': 0,
                        'style': {
                            'fill': "#000",
                            'text': "非建议：%s%%   建议：%s%% " % (not_advice_type_defect_percent, advice_type_defect_percent),
                            'font':'bolder 13px Microsoft YaHei'
                        }
                    })

            defects_created_by_individual_list = sorted(defects_created_by_individual_dict.items(), key=lambda arg:arg[1].get('DI'), reverse=True)
            defects_created_by_individual = []
            for item in defects_created_by_individual_list:
                item = item[1]
                defects_created_by_individual.append({'creater':item['creater'], 'DI':'%.1f' % item['DI'], 'total_created': item['total_created'], 'deadly':item['致命'], 'critical':item['严重'], 'general':item['一般'], 'minor':item['轻微']})

            defects_resolved_by_individual_list = sorted(defects_resolved_by_individual_dict.items(), key=lambda arg:arg[1].get('DI'), reverse=True)
            defects_resolved_by_individual = []
            for item in defects_resolved_by_individual_list:
                item = item[1]
                defects_resolved_by_individual.append({'resolver':item['resolver'], 'DI':'%.1f' % item['DI'], 'total_raised': item['total_raised'], 'total_resolved': item['total_resolved'],  'deadly':item['致命'], 'critical':item['严重'], 'general':item['一般'], 'minor':item['轻微']})

            result = {'success':True, 'defect_status_pie_data':defect_status_pie_data, 'defect_severity_pie_data':defect_severity_pie_data, 'defect_type_pie_data':defect_type_pie_data,
                      'defect_source_bar_data':defect_source_bar_data,  'defects_created_by_individual':defects_created_by_individual, 'defects_resolved_by_individual':defects_resolved_by_individual,
                      'defects_unclosed':defects_unclosed,
                      'error':''.join(list(error_info))
                      }
            return result
        except Exception as e:
            return {'success':False, 'error':'%s' % e}


    @staticmethod
    def get_testcase_execution_statistics(plan_id_list):
        '''获取用例执行饼图统计数据'''


        case_status = ['未执行', '通过', '失败', '阻塞']
        series_data = []
        temp_dict = {}
        for item in case_status:
            temp_dict[item] = 0
            series_data.append({'value':0, 'name': item})

        # 展示饼图所需数据
        data_for_pie = {
            'centerText': "通过率\n0%",
            'seriesData': series_data,
            'aroundTextConfig':[]
        }

        data_for_db = {'通过率':'0.0'}
        data_for_db.update(temp_dict)  # 保存到数据库所需数据
        try:
            testcase_total = 0 # 用例总数
            if len(plan_id_list):
                plan_ids = str(plan_id_list)
                plan_ids = plan_ids.replace('[', '(').replace(']', ')')

                query_sql = 'SELECT id, result AS testResult, COUNT(id) AS num ' \
                            'FROM tb_sprint_testplan_testcase ' \
                            'WHERE testplan_id IN %s GROUP BY testResult' % plan_ids

                testplans = SprintTestplanTestcase.objects.raw(query_sql)

                for testplan in testplans:
                    key, value = testplan.testResult, testplan.num
                    data_for_db[key] = value
                    testcase_total += value

            # 更新饼图series data
            if testcase_total:
                for item in series_data:
                    if item['name'] in data_for_db:
                        item['value'] = data_for_db[item['name']]
                        item['percent'] = '%.2f' % (item['value'] / testcase_total * 100)

                # 更新通过率
                testcase_pass_rate = '%.2f' % (data_for_db['通过'] / testcase_total * 100)
                data_for_pie['centerText'] = "通过率\n%s%%" % testcase_pass_rate

                testcase_executed_rate = '%.2f' % ((testcase_total - data_for_db['未执行']) / testcase_total * 100)
                data_for_pie['aroundTextConfig'].append({
                            'type': "text",
                            'left': "left",
                            'bottom': 0,
                            'style': {
                                'fill': "#000",
                                'text': "执行率：%s%%  " %  testcase_executed_rate,
                                'font':'bolder 13px Microsoft YaHei'
                            }
                        })

            else:
                for item in series_data:
                    if item['name'] in data_for_db:
                        item['value'] = data_for_db[item['name']]
                        item['percent'] =  '0'
            result = {'success':True, 'dataForPie':data_for_pie}
        except Exception as e:
            logger.error('%s' % e)
            result = {'success':False, 'msg':'获取用例执行统计数据出错：%s' % e}
        finally:
            return result


    @staticmethod
    def get_case_execution_individual_statistics(plan_id_list):
        '''获取个人用例执行统计'''

        try:
            testcase_statistics = []
            if len(plan_id_list):
                plan_ids = str(plan_id_list)
                plan_ids = plan_ids.replace('[', '(').replace(']', ')')

                query_sql = '''
                SELECT  t1.id, t1.name, IFNULL(t2.assigned, 0) AS assigned, IFNULL(t3.executed, 0) AS executed, IFNULL(t4.passed, 0) AS passed
                FROM (
                      SELECT tb_user.id, tb_user.name
                      FROM tb_sprint_testplan_testcase  AS `tc`
                      LEFT JOIN tb_user ON (tc.tester_id=tb_user.id AND tc.tester_id<>0 AND tc.tester_id IS NOT NULL) OR tc.assigned_to_id=tb_user.id
                      WHERE tc.testplan_id IN %s
                      GROUP BY tb_user.id) AS t1
                      LEFT JOIN (SELECT tc.assigned_to_id,  COUNT(tc.id) AS assigned
                          FROM tb_sprint_testplan_testcase  AS `tc`
                          WHERE tc.testplan_id IN %s
                          GROUP BY tc.assigned_to_id
                      ) AS t2 ON t2.assigned_to_id = t1.id
                      LEFT JOIN (SELECT tc.tester_id, COUNT(tc.id) AS executed
                          FROM tb_sprint_testplan_testcase AS `tc`
                          WHERE tc.testplan_id IN %s AND tc.result != "未执行" AND tc.tester_id IS NOT NULL
                          GROUP BY tc.tester_id) AS t3 ON t3.tester_id = t1.id
                      LEFT JOIN (SELECT tc.tester_id, COUNT(tc.id) AS passed
                             FROM tb_sprint_testplan_testcase AS `tc`
                             WHERE tc.testplan_id IN %s AND tc.result = "通过" AND tc.tester_id IS NOT NULL
                             GROUP BY tc.tester_id) AS t4 ON t4.tester_id = t1.id
                 ''' % (plan_ids, plan_ids, plan_ids, plan_ids)

                query_result = SprintTestplanTestcase.objects.raw(query_sql)
                for result in query_result:
                    temp = {}
                    temp['username'] = result.name
                    temp['testcase_assigned'] = result.assigned
                    temp['testcase_executed'] = result.executed
                    temp['testcase_passed'] = result.passed

                    testcase_execution_rate = '0.0'
                    testcase_pass_rate = '0.0'
                    if temp['testcase_assigned']:
                        testcase_execution_rate =  '%.1f' %  (result.executed / result.assigned * 100)
                    if temp['testcase_executed']:
                        testcase_pass_rate = '%.1f' % (result.passed / result.executed * 100)

                    temp['testcase_execution_rate'] = testcase_execution_rate
                    temp['testcase_pass_rate'] = testcase_pass_rate
                    testcase_statistics.append(temp)
            result = {'success':True, 'case_execution_individual_statistics':testcase_statistics}
        except Exception as e:
            logger.error('%s' % e)
            result = {'success':False, 'msg':'获取个人用例执行统计失败：%s' % e}
        finally:
            return result


    @staticmethod
    def convert_related_plans_to_html(related_plans):
        '''转换报告关联的测试计划数据格式为html格式数据，返回转换后的数据'''

        result = ''
        tr = '''<tr>
                <td style="text-align: left;">
                    <div>
                        {name}
                    </div>
                </td>
                <td>
                    <div>
                        {begin_time}
                    </div>
                </td>
                <td>
                    <div>
                        {start_time}
                    </div>
                </td>
                <td>
                    <div>
                        {end_time}
                    </div>
                </td>
                <td>
                    <div>
                        {finish_time}
                    </div>
                </td>
                <td>
                    <div>
                        {status}
                    </div>
                </td>
                <td>
                    <div>
                        {progress}%({case_num_executed}/{case_num_related})
                    </div>
                </td>
                <td>
                    <div>
                        {pass_rate}%({case_num_success}/{case_num_related})
                    </div>
                </td>
                <td>
                    <div>
                    {case_num_fail}
                    </div>
                </td>
                <td>
                    <div>
                        {case_num_blocked}
                    </div>
                </td>
                <td>
                    <div>
                        {case_num_unexecuted}
                    </div>
                </td>
                <td style="text-align: left;">
                    <div>
                        {project_names}
                    </div>
                </td>
                <td style="text-align: left;">
                    <div>
                        {env_names}
                    </div>
                </td>
            </tr>'''

        for related_plan in related_plans:
            result += tr.format(**related_plan)
        return result

    @staticmethod
    def convert_defect_source_bar_to_html(img_data):
        '''转换缺陷根因横向柱状图为html'''

        if img_data:
            return '''<div class="report-sub-session">
                        <div class="report-sub-session-title">缺陷根源分组统计</div>
                        <div class="stacked-column-chart">
                            <img src="%s" />
                        </div>
                    </div>''' % img_data
        else:
            return ''

    @staticmethod
    def convert_case_execution_individual_to_html(case_execution_individual):
        '''转换个人用例执行统计数据格式为html格式数据，返回转换后的数据'''

        result = ''
        tr = '''<tr class="el-table__row">
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {username}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {testcase_assigned}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {testcase_executed}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {testcase_passed}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {testcase_execution_rate}%
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {testcase_pass_rate}%
                    </div>
                </td>
            </tr>'''

        for item in case_execution_individual:
            result += tr.format(**item)

        return result

    @staticmethod
    def convert_defects_created_individual_to_html(defects_created_individual):
        '''转换个人提交缺陷数据格式为html格式数据，返回转换后的数据'''

        result = ''
        tr = '''<tr class="el-table__row">
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {creater}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {DI}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {total_created}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {deadly}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {critical}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {general}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {minor}
                    </div>
                </td>
            </tr>'''

        for item in defects_created_individual:
            result += tr.format(**item)

        return result

    @staticmethod
    def convert_defects_resolved_individual_to_html( defects_resolved_individual):
        '''转换个人处理缺陷数据格式为html格式数据，返回转换后的数据'''

        result = ''
        tr = '''<tr class="el-table__row">
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {resolver}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {total_resolved}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {total_raised}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {DI}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {deadly}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {critical}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {general}
                    </div>
                </td>
                <td rowspan="1" colspan="1" class="is-center ">
                    <div class="cell">
                        {minor}
                    </div>
                </td>
            </tr>'''

        for item in defects_resolved_individual:
            result += tr.format(**item)
        return result

    @staticmethod
    def convert_unclosed_defect_statistics_to_html(unclosed_defect_statistics):
        '''转换遗留缺陷统计数据格式为html格式数据，返回转换后的数据'''

        result = ''
        tr = '''<tr class="el-table__row">
            <td rowspan="1" colspan="1" class="is-center" width="8%">
                <div class="cell">
                    <a target="_blank" href="{defect_href}">{defect_id}</a>
                </div>
            </td>
            <td rowspan="1" colspan="1" class="is-left" width="45%">
                <div class="cell">
                    {title}
                </div>
            </td>
            <td rowspan="1" colspan="1" class="is-center" width="5%">
                \
                <div class="cell">
                    {severity}
                </div>
            </td>
            <td rowspan="1" colspan="1" class="is-center" width="6%">
                <div class="cell">
                    {status}
                </div>
            </td>
            <td rowspan="1" colspan="1" class="is-center" width="6%">
                <div class="cell">
                    {remark}
                </div>
            </td>
            <td rowspan="1" colspan="1" class="is-center" width="6%">
                <div class="cell">
                    {creater}
                </div>
            </td>
            <td rowspan="1" colspan="1" class="is-center" width="6%">
                <div class="cell">
                    {assigned_to}
                </div>
            </td>
            <td rowspan="1" colspan="1" class="is-center" width="6%">
                <div class="cell">
                    {person_liable}
                </div>
            </td>
            <td rowspan="1" colspan="1" class="is-center" width="6%">
                <div class="cell">
                    {resolver}
                </div>
            </td>
            <td rowspan="1" colspan="1" class="is-center" width="5%">
                <div class="cell">
                    {platform}
                </div>
            </td>
        </tr>'''

        for item in unclosed_defect_statistics:
            if item['platform'] == 'jira':
                item['defect_href'] = JIRA_ISSUE_BROWSE_BASE_URL + item['defect_id']
            elif item['platform'] == '禅道':
                item['defect_href'] = ZENTAO_BUG_BROWSE_BASE_URL + item['defect_id'] + '.html'
            result += tr.format(**item)
        return result
