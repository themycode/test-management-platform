#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = '赖富玉'

import json
import logging
import base64
import re
import time

from django.conf import settings

from backend.http.httpprotocol import MyHttp
from backend.http.request import HttpRequest

from backend.models import TpadDefect
from backend.serializers import TpadDefectSerializer
from backend.common.wrappers import close_old_database_connections
from datetime import datetime,date



logger = logging.getLogger('mylogger')


# 对api_user:password进行base64编码
auth_key = base64.b64encode('rOqXp_d0:8BFCE2EC-BF9A-1DBB-6DDC-9951D205AA1F'.encode('utf-8'))
auth_key = str(auth_key).lstrip('b')

# tpad站点信息
TPAD_PROTOCAOL = 'https'
TPAD_HOST = 'api.tapd.cn'
TPAD_PORT = 443
TPAD_AUTHORIZATION = 'Basic %s'% auth_key


class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field,datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field,date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self,field)

class TpadProjectTool:
    '''Tpad项目工具类'''

    def __init__(self):
        pass


    @staticmethod
    def create_or_update_project_version(version_info):
        '''
        创建、修改tpad项目版本
        version_info ：key1=value1&key2=value2...'''

        try:
            http = MyHttp(TPAD_PROTOCAOL, TPAD_HOST, TPAD_PORT, {'Authorization': TPAD_AUTHORIZATION })
            url = '/versions'
            result = HttpRequest.urlencode_request('post', url , version_info, http, parse_type="quote_plus")
            return result
        except Exception as e:
            return [False, '%s' % e ]



class TpadDefectTool:
    '''tpad 缺陷工具类'''


    def __init__(self):
        try:
            self.auth_key = base64.b64encode('rOqXp_d0:8BFCE2EC-BF9A-1DBB-6DDC-9951D205AA1F'.encode('utf-8'))
            self.auth_key = str(self.auth_key).lstrip('b')
        except Exception as e:
            raise Exception('对api_user:password进行base64编码失败：%s' % e)

    @staticmethod
    def get_custom_fields_settings(params):
        '''
        获取缺陷自定义字段配置信息
        '''

        try:
            http = MyHttp(TPAD_PROTOCAOL, TPAD_HOST, TPAD_PORT, {'Authorization': TPAD_AUTHORIZATION })
            url = '/bugs/custom_fields_settings?'
            result = HttpRequest.urlencode_request('get', url , params, http, parse_type="quote_plus")
            return result
        except Exception as e:
            return [False, '%s' % e ]


    @staticmethod
    def get_single_page_defects(params):
        '''
        获取缺单页缺陷数据
        '''

        try:
            http = MyHttp(TPAD_PROTOCAOL, TPAD_HOST, TPAD_PORT, {'Authorization': TPAD_AUTHORIZATION })
            url = '/bugs?'
            result = HttpRequest.urlencode_request('get', url , params, http, parse_type="quote_plus")
            return result
        except Exception as e:
            return [False, '%s' % e ]


    @staticmethod
    def get_all_defects(params):
        '''
        获取所有缺陷数据
        '''

        try:
            result = []
            request_next_page = True # 标记是否继续请求下一页数据
            page = 0
            page_size = re.findall('limit\s*=(.+)&*', params)
            if page_size:
                page_size = int(page_size[0])
            else:
                page_size = 200
            while request_next_page:
                page += 1
                time.sleep(1)

                request_params = params + '&page=%s' % page
                http = MyHttp(TPAD_PROTOCAOL, TPAD_HOST, TPAD_PORT, {'Authorization': TPAD_AUTHORIZATION })
                url = '/bugs?'
                request_result = HttpRequest.urlencode_request('get', url , request_params, http, parse_type="quote_plus")
                if request_result[0]:
                    response_body = request_result[1]
                    response_body = response_body.replace('\t', ' ') # 替换tab输入，防止json格式化报错
                    response_body= json.loads(response_body)
                    info = response_body.get('info')
                    if info != 'success':
                        return [False, info]
                    else:
                        data = response_body.get('data')
                        if data and len(data) < page_size: # 不存在下一页数据
                            request_next_page = False
                        if data:
                            result.extend(data)
                else:# 请求结果出错
                    return [False, request_result[1]]
            return [True, result]
        except Exception as e:
            logger.error('%s' % e)
            return [False, '%s' % e ]


    @staticmethod
    @close_old_database_connections
    def sync_tpad_project_online_defects():
        '''同步tpad所有线上缺陷数据'''
        try:
            project_id = settings.TPAD_PROJECT_ID
            fields = 'id,title,severity,status,bugtype,source,created,resolved,closed,version_report,reporter,closer,priority,iteration_id,' \
                    'module,version_test,version_fix,version_close,current_owner,participator,te,de,auditer,confirmer,lastmodify,in_progress_time,' \
                    'verify_time,reject_time,modified,begin,due,deadline,os,platform,custom_field_two,custom_field_three'
            params = "workspace_id=%s&fields=%s&limit=200"  % (project_id, fields)
            result = TpadDefectTool.get_all_defects(params)
            severity_map = {'fatal':'致命','一般':'一般', 'normal':'一般', 'serious':'严重', 'prompt':'轻微', 'advice':'建议'}
            source_map = {'产品优化':'产品设计问题','需求建议':'产品设计问题','产品设计问题':'产品设计问题', '建议优化问题':'产品设计问题', '必须优化问题':'产品设计问题','优化建议':'产品设计问题','业务部门改进问题':'产品设计问题',
                          'bug':'Bug', '重复bug':'Bug','正常业务':'Bug', '配置错误':'配置问题', '运营配置问题':'配置问题','咨询问题':'业务咨询',
                          '用户操作问题':'业务咨询', '用户环境/操作问题':'业务咨询','业务协助处理':'咨询问题', '客户环境问题':'其它问题', '疑似bug确认':'其它问题'} # 旧数据根因重定义

            source_type_map = {'产品设计问题':'产品设计问题','用户新需求':'用户新需求','Bug':'功能问题', '兼容性问题':'功能问题','数据问题':'功能问题',
                          '用户界面问题':'界面问题','服务问题':'性能问题','慢SQL':'性能问题','配置问题':'配置问题','第三方问题':'其它问题', '网络问题':'其它问题', '日志告警':'其它问题','其它问题':'其它问题',
                         '业务咨询':'咨询问题', '咨询问题':'咨询问题'} # 根因和问题类型的映射

            if result[0]:
                result = result[1]
                for item in result:
                    bug = item.get('Bug')
                    bug['product'] = bug.get('custom_field_two')
                    if bug['product'] == '数据团队':
                        bug['product'] = '基础数据'

                    if not bug['product']:
                        bug['product'] = '其它'
                    bug.pop('custom_field_two')

                    bug['event_level'] = bug.get('custom_field_three')
                    bug.pop('custom_field_three')

                    if bug['severity']:
                        bug['severity'] = severity_map[bug['severity']]

                    if not bug['bugtype']:
                        bug['bugtype'] = '其它问题'

                    if not bug['source']:
                        bug['source'] = bug['bugtype']

                    if bug['source'] in source_map.keys():
                        bug['source'] = source_map[bug['source']]

                    if bug['source'] in source_type_map.keys():
                        bug['bugtype'] = source_type_map[bug['source']]

                    if not bug['version_report']:
                        bug['version_report'] = '000000000001'

                    tpad_defect = TpadDefect.objects.filter(id=bug.get('id')).first()
                    if tpad_defect: # 存在则更新
                        serializer = TpadDefectSerializer(tpad_defect, data=bug)
                    else: # 新增
                        serializer = TpadDefectSerializer(data=bug)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            else:
                logger.error('同步TPAD缺陷出错：%s' %  result[1])
        except Exception as e:
            logger.error('同步TPAD缺陷出错：%s' % e)


    @staticmethod
    def get_defect_type_statistics(filters='', group_by='', fields=''):
        '''
        缺陷类型统计数据
        filters: 供查询where子句使用的额外过滤条件，格式遵循 MySQL语法
        params：查询参数，形如（value1,value2,...）
        group_by: 用于分组的字段，字段间使用英文逗号分隔,形如 product,status 先按product字段分组，再按status分组
        fields:附加查询字段，字段间使用英文逗号分隔
        '''


        try:
            query_sql ='SELECT id,{} bugtype, ' \
                       'COUNT(id) as num ' \
                       'FROM tb_tpad_defect ' \
                       '{} ' \
                       '{}'

            if group_by:
                group_by = 'GROUP BY %s' % group_by
            else:
                group_by = ''

            if filters:
                filters = 'WHERE %s' % filters
            else:
                filters = ''

            if fields:
                fields = fields + ','
            else:
                fields = ''
            query_sql = query_sql.format(fields, filters, group_by)
            query_result = TpadDefect.objects.raw(query_sql)
            return [True, query_result]
        except Exception as e:
            logger.error('%s' % e)
            return [False, '%s' % e]


    @staticmethod
    def get_defect_status_statistics(filters='', group_by='', fields=''):
        '''
        缺陷状态统计数据
        filters: 供查询where子句使用的额外过滤条件，格式遵循 MySQL语法
        params：查询参数，形如（value1,value2,...）
        group_by: 用于分组的字段，字段间使用英文逗号分隔,形如 product,status 先按product字段分组，再按status分组
        fields:附加查询字段，字段间使用英文逗号分隔
        '''


        try:
            query_sql ='SELECT id,{} CASE status  WHEN "new"  THEN "新建" '  \
                       'WHEN "in_progress" THEN "接受/处理" ' \
                       'WHEN "resolved" THEN "已解决" ' \
                       'WHEN "closed" THEN "已关闭" ' \
                       'WHEN "reopened" THEN "重新打开"' \
                       'WHEN "rejected" THEN "已拒绝" ELSE "其它" END AS defect_status, ' \
                       'COUNT(id) as num ' \
                       'FROM tb_tpad_defect ' \
                       '{} ' \
                       '{}'

            if group_by:
                group_by = 'GROUP BY %s' % group_by
            else:
                group_by = ''

            if filters:
                filters = 'WHERE %s' % filters
            else:
                filters = ''

            if fields:
                fields = fields + ','
            else:
                fields = ''
            query_sql = query_sql.format(fields, filters, group_by)
            query_result = TpadDefect.objects.raw(query_sql)
            return [True, query_result]
        except Exception as e:
            logger.error('%s' % e)
            return [False, '%s' % e]

    @staticmethod
    def get_defect_product_statistics(filters='', group_by='', fields=''):
        '''获取缺陷产品统计数据'''

        try:
            query_sql ='SELECT id, {} product as `name`, count(id) as `value` ' \
                       'FROM tb_tpad_defect ' \
                       '{} ' \
                       '{}'

            if group_by:
                group_by = 'GROUP BY %s' % group_by
            else:
                group_by = ''

            if filters:
                filters = 'WHERE %s' % filters
            else:
                filters = ''

            if fields:
                fields = fields + ','
            else:
                fields = ''
            query_sql = query_sql.format(fields, filters, group_by)
            query_result = TpadDefect.objects.raw(query_sql)
            return [True, query_result]
        except Exception as e:
            logger.error('%s' % e)
            return [False, '%s' % e]

    @staticmethod
    def get_defect_source_statistics(filters='', group_by='', fields='', order_by=''):
        '''获取缺陷根源统计数据'''

        try:
            query_sql ='SELECT id, {} source as `name`, count(id) as `value` ' \
                       'FROM tb_tpad_defect ' \
                       '{} ' \
                       '{} ' \
                       '{}'

            if group_by:
                group_by = 'GROUP BY %s' % group_by
            else:
                group_by = ''
            if order_by:
                order_by = 'ORDER BY %s' % order_by

            if filters:
                filters = 'WHERE %s' % filters
            else:
                filters = ''

            if fields:
                fields = fields + ','
            else:
                fields = ''
            query_sql = query_sql.format(fields, filters, group_by, order_by)
            query_result = TpadDefect.objects.raw(query_sql)
            return [True, query_result]
        except Exception as e:
            logger.error('%s' % e)
            return [False, '%s' % e]

    @staticmethod
    def get_defect_severity_statistics(filters='', group_by='', fields=''):
        '''获取缺陷级别统计数据'''

        try:
            query_sql ='SELECT id, {} severity as `name`, count(id) as `value` ' \
                       'FROM tb_tpad_defect ' \
                       'WHERE severity != "" {} ' \
                       '{}'

            if group_by:
                group_by = 'GROUP BY %s' % group_by
            else:
                group_by = ''

            if filters:
                filters = 'AND %s' % filters
            else:
                filters = ''

            if fields:
                fields = fields + ','
            else:
                fields = ''
            query_sql = query_sql.format(fields, filters, group_by)
            query_result = TpadDefect.objects.raw(query_sql)
            return [True, query_result]
        except Exception as e:
            logger.error('%s' % e)
            return [False, '%s' % e]


    @staticmethod
    def get_defect_event_level_statistics(filters='', group_by='', fields=''):
        '''获取缺陷事件等级统计数据'''

        try:
            query_sql ='SELECT id, {} event_level as `name`, count(id) as `value` ' \
                       'FROM tb_tpad_defect ' \
                       'WHERE event_level NOT IN ("", "非bug") {} ' \
                       '{}'

            if group_by:
                group_by = 'GROUP BY %s' % group_by
            else:
                group_by = ''

            if filters:
                filters = 'AND %s' % filters
            else:
                filters = ''

            if fields:
                fields = fields + ','
            else:
                fields = ''
            query_sql = query_sql.format(fields, filters, group_by)
            query_result = TpadDefect.objects.raw(query_sql)
            return [True, query_result]
        except Exception as e:
            logger.error('%s' % e)
            return [False, '%s' % e]


    @staticmethod
    def get_defect_fixing_time_summary_statistics(filters='', fields='', group_by=''):
        '''
        获取问题历时统计汇总数据[新建-已关闭]
        '''

        try:
            query_sql = "SELECT id, {} TRUNCATE(MAX((UNIX_TIMESTAMP(closed) - UNIX_TIMESTAMP(created))/3600), 3) AS 'maxTimeTook'," \
                        "TRUNCATE(MIN((UNIX_TIMESTAMP(closed) - UNIX_TIMESTAMP(created))/3600), 3) AS 'minTimeTook'," \
                        "TRUNCATE(AVG((UNIX_TIMESTAMP(closed) - UNIX_TIMESTAMP(created))/3600), 3) AS 'avgTimeTook' " \
                        "FROM tb_tpad_defect WHERE status = 'closed' {} " \
                        "{}"
            if filters:
                filters = 'AND %s' % filters
            else:
                filters = ''

            if fields:
                fields = fields + ','
            else:
                fields = ''

            if group_by:
                group_by = 'GROUP BY %s' % group_by
            else:
                group_by = ''
            query_sql = query_sql.format(fields, filters, group_by)
            query_result = TpadDefect.objects.raw(query_sql)
            return [True, query_result]
        except Exception as e:
            logger.error('%s' % e)
            return [False, '%s' % e]

    @staticmethod
    def get_defect_fixing_time_statistics(filters='', fields=''):
        '''
        获取缺陷、咨询类问题历时统计数据【新建-已关闭】
        '''

        try:
            query_sql = "SELECT id, {} CASE WHEN CEIL((UNIX_TIMESTAMP(closed) - UNIX_TIMESTAMP(created))/3600)<=4 THEN '0-4小时' " \
                        "WHEN CEIL((UNIX_TIMESTAMP(closed) - UNIX_TIMESTAMP(created))/3600)<=8 THEN  '4-8小时'" \
                        "WHEN CEIL((UNIX_TIMESTAMP(closed) - UNIX_TIMESTAMP(created))/3600)<=24 THEN '8-24小时' " \
                        "WHEN CEIL((UNIX_TIMESTAMP(closed) - UNIX_TIMESTAMP(created))/3600)<=72 THEN '1-3天'" \
                        "WHEN CEIL((UNIX_TIMESTAMP(closed) - UNIX_TIMESTAMP(created))/3600)<=336 THEN '3-14天'" \
                        "ELSE '14天+'END AS 'name', COUNT(id) AS 'value' " \
                        "FROM tb_tpad_defect WHERE status = 'closed' {} " \
                        "GROUP BY `name`"

            if filters:
                filters = 'AND %s' % filters
            else:
                filters = ''

            if fields:
                fields = fields + ','
            else:
                fields = ''
            query_sql = query_sql.format(fields, filters)
            query_result = TpadDefect.objects.raw(query_sql)
            return [True, query_result]
        except Exception as e:
            logger.error('%s' % e)
            return [False, '%s' % e]


    def search_tpad_bugs(self, filters):
        '''input_params格式 ：filter1=value1&filter2=value2...'''
        try:

            http = MyHttp(TPAD_PROTOCAOL, TPAD_HOST, TPAD_PORT, {'Authorization': TPAD_AUTHORIZATION })
            url = '/bugs?'

            result = HttpRequest.urlencode_request('get', url , filters, http, parse_type="quote_plus")

            logger.info(result)
            return result
        except Exception as e:
            return [False, '%s' % e ]


    def search_tpad_requirement(self, filters):
        try:
            http = MyHttp(TPAD_PROTOCAOL, TPAD_HOST, TPAD_PORT, {'Authorization': TPAD_AUTHORIZATION })
            url = '/stories?'
            result = HttpRequest.urlencode_request('get', url , filters, http)
            logger.info(result)
            return result
        except Exception as e:
            return [False, '%s' % e ]
