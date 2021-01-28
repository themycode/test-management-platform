#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import os


MAX_CASES_NUM_EXCEL_EXPORT = 5000 # 单次导出最大用例数（Excel导出）
MAX_CASES_NUM_XMIND_EXPORT = 2000  # 单次导出最大用例数（XMind导出）

head, tail = os.path.split(__file__)
# 供导出测试用例为xmind时使用的xmind文档路径
XMIND_TEMPLATE_FILE_PATH  = os.path.normpath(os.path.join(head, '../document/export_testcase.xmind'))

USER_MEDIA_ROOT = ''   # 存放用户媒体文件，如果这里配置为空，默认使用TMP/settings.py 中的 MEDIA_ROOT

SYS_CUSTOM_FIELDS = [{'id':'severity', 'name':'缺陷严重程度'}, {'id':'defect_type', 'name':'缺陷类型'},{'id':'person_liable', 'name':'缺陷责任人'},
                     {'id':'is_history', 'name':'是否历史遗留'}, {'id':'source', 'name':'缺陷根因'}, {'id':'is_effective', 'name':'是否有效缺陷'},
                     {'id':'is_online', 'name':'是否线上问题'}, {'id':'is_advice', 'name':'是否为建议'}
                    ]

# 禅道数据库缺陷自定义字段
ZENTAO_DEFECT_CUSTOM_FIELDS = ['isHistory', 'personLiable', 'source']

# 系统字段和禅道数据库缺陷自定义字段映射 系统字段:禅道自定义字段
# ZENTAO_DEFECT_CUSTOM_FIELD_MAP = {'person_liable':'personLiable', 'is_history':'isHistory', 'source':'source', 'is_advice':'isAdvice', 'is_online':'isOnline'}
ZENTAO_DEFECT_CUSTOM_FIELD_MAP = {'person_liable':'personLiable', 'is_history':'isHistory', 'source':'source'}

# jiar缺陷默认类型名称
JIRA_ISSUE_TYPE_NAME = '缺陷' # 如果项目未配置缺陷归属类型，则使用该名称进行类型过滤

# 缺陷严重程度映射（# 系统严重程度定义： 致命，严重，一般，轻微）
DEFECT_SEVERITY_MAP = {'致命':'致命', '严重':'严重', '一般':'一般', '轻微':'轻微', '提示':'轻微', '建议':'轻微',
                       1:'致命', 2:'严重', 3:'一般', 4:'轻微',  5:'轻微'}

# 缺陷状态映射（系统缺陷状态定义：新建，处理中，已解决，延期处理，已拒绝，重新打开，已关闭）
DEFECT_STATUS_MAP = {'新建':'新建',
                     '已转需求':'新建',
                     '处理中':'处理中',
                     '已受理':'处理中',
                     'resolved':'已解决',
                     '已解决':'已解决',
                     '延期处理':'延期处理',
                     '已拒绝':'已拒绝',
                     '重新打开':'重新打开',
                     '已关闭':'已关闭',
                     'closed':'已关闭'}

# 缺陷类型映射（系统缺陷类型定义：界面缺陷，功能缺陷，性能缺陷，其它缺陷）
DEFECT_TYPE_MAP = { 'interface': '界面缺陷',
                    'codeerror':'功能缺陷',
                    '功能缺陷':'功能缺陷',
                    '兼容性问题':'功能缺陷',
                    'compatibility':'功能缺陷',
                    '功能异常':'功能缺陷',
                    'security':'安全缺陷',
                    'performance':'性能缺陷',
                    '性能缺陷':'性能缺陷',
                    '性能问题':'性能缺陷',
                    '设计规范问题':'其它缺陷',
                    'designdefect':'其它缺陷',
                    'RequirementChange':'其它缺陷',
                    'RequirementMissing':'其它缺陷',
                    'others':'其它缺陷',
                    'online':'其它缺陷',
                    'optimization':'其它缺陷',
                    '其他问题':'其它缺陷',
                    '其它问题':'其它缺陷',
                    '优化建议':'其它缺陷',
                    '页面样式':'界面缺陷',
                    '线上问题':'其它缺陷'
                    }

# 缺陷是否历史遗留映射（系统缺陷是否历史遗留标识定义：历史遗留，非历史遗留）  '0':'非历史遗留' 配置不能少
DEFECT_IS_HISTORY_MAP = {'1':'历史遗留', '是':'历史遗留', '否':'非历史遗留', '0':'非历史遗留'}

# 缺陷根因映射
DEFECT_SOURCE_MAP = {'产品设计问题':'产品需求错误',
                     'requirementError':'产品需求错误',
                     '产品设计问题,需求遗漏':'产品需求遗漏',
                     '产品设计问题,需求变更':'产品需求变更未及时同步',
                     'requirementChanged':'产品需求变更未及时同步',
                     '产品设计问题,需求不清晰':'产品需求不清晰',
                     '开发问题,需求规格未达标':'产品需求不清晰',
                     'requirementUnclear':'产品需求不清晰',
                     'lackOfHighFidelityUI':'缺少高保真图',
                     '开发问题,代码实现错误':'程序代码实现错误',
                     'codeError':'程序代码实现错误',
                     '开发问题,兼容性问题':'程序代码实现错误',
                     '开发问题,场景遗漏':'程序代码实现错误',
                     '开发问题,代码配置错误':'程序配置错误',
                     '开发问题,需求理解偏差':'开发者需求理解偏差',
                     '开发问题,未参考高保真':'未参照高保真开发',
                     '开发问题,设计规范问题':'开发设计规范问题',
                     '环境因素,部署遗漏':'程序部署遗漏'

                     }

# 缺陷是否有效标记（如果“是否有效缺陷”字段值，包含列表中元素值则表示缺陷无效）
DEFECT_NOT_EFFECTIVE_FLAG =  ['非问题', '重复Bug', 'notBug', '构建出错', '网络问题', '第三方问题']

# 缺陷是否为建议标记（如果“是否为建议”字段值，包含列表中元素值则表示缺陷为建议类型）
DEFECT_SUGGEST_FLAG =  ['建议', 'optimization']

JIRA_ISSUE_BROWSE_BASE_URL = "https://jira.casstime.com/browse/EC-" # jira issue查阅基础地址
ZENTAO_BUG_BROWSE_BASE_URL = "http://10.118.71.212/zentaopms/www/bug-view-" # 禅道 Bug查阅基础地址


