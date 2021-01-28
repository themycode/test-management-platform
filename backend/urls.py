#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from django.urls import  path,re_path
# from django.conf.urls import url

from . import views
from backend.system_management.system_config import sys_menu_views
from backend.system_management.system_config import sys_role_views
from backend.system_management.system_config import sys_user_views
from backend.system_management.system_config import sys_group_views

from backend.system_management.env import env_views
from backend.system_management.test_phase import test_phase_views

from backend.system_management.msg_push import msg_push_account_views

from backend.product_view.product import product_views
from backend.product_view.sprint import sprint_views

from backend.project_view.project import project_views
from backend.project_view.project import project_version_views

from backend.project_view import project_env_views

from backend.tester_view.testcase import testcase_suite_views
from backend.tester_view.testcase import testcase_views
from backend.tester_view.testcase import testcase_attachment_views

from backend.tester_view.testplan import testplan_views
from backend.tester_view.testplan import testplan_testcase_views

from backend.tester_view.testreport import sprint_test_report_views



urlpatterns = [
    re_path(r'^api-token-auth/', views.CustomAuthToken.as_view()),

    path('api/v1/login', views.LoginView.as_view()),
    path('api/v1/logout', views.LogoutView.as_view()),
    path('api/v1/user-perms', views.UserPermsView.as_view()),

    # 系统管理-系统配置-菜单管理
    path('api/v1/sys-menu-tree', sys_menu_views.MenuTreeAPIView.as_view()), # 查询菜单树
    path('api/v1/sys-menu', sys_menu_views.MenuAPIView.as_view()), # 新增某个菜单
    re_path('^api/v1/sys-menu/\d+$', sys_menu_views.MenuAPIView.as_view()), # 修改，删除某个菜单


    # 系统管理-系统配置-角色管理
    path('api/v1/sys-roles', sys_role_views.RoleListAPIView.as_view()), # 查询角色列表 批量删除角色
    path('api/v1/sys-role', sys_role_views.RoleAPIView.as_view()), # 新增某个角色
    re_path('^api/v1/sys-role/\d+$', sys_role_views.RoleAPIView.as_view()), # 修改，启用、禁用，删除某个角色
    # 关联菜单
    re_path('^api/v1/sys-role/\d+/related-menus$', sys_role_views.RelatedMenusAPIView.as_view()),  #查询某个角色关联的菜单、给某个角色关联菜单


    # 系统管理-系统配置-用户管理
    path('api/v1/sys-users', sys_user_views.UserListAPIView.as_view()), # 查询用户列表，批量删除用户
    path('api/v1/sys-user', sys_user_views.UserAPIView.as_view()), # 新增单个用户
    path('api/v1/sys-user/userinfo', sys_user_views.UserPersonalInfo.as_view()), # 获取当前登录用户个人信息
    re_path('^api/v1/sys-user/\d+$', sys_user_views.UserAPIView.as_view()), # 修改，启用、禁用，删除某个用户，获取某个指定用户的个人信息
    re_path('^api/v1/sys-user/\d+/passwd$', sys_user_views.UserPasswdAPIView.as_view()), # 重置用户密码
    path('api/v1/sys-user/passwd', sys_user_views.UserPasswdAPIView.as_view()), # 修改用户密码
    path('api/v1/user/menus', sys_user_views.UserMenusAPIView.as_view()), # 获取用户关联的导航菜单
    # 批量获取用户指定字段信息 供“产品管理”，“测试计划”模块使用
    path('api/v1/users/details', sys_user_views.UsersDetailsAPIView.as_view()),

    # 角色相关
    re_path('^api/v1/sys-user/\d+/unrelated-roles$', sys_user_views.UnrelatedRolesAPIView.as_view()), # 获取某个用户未关联角色
    re_path('^api/v1/sys-user/\d+/roles$', sys_user_views.UserRolesAPIView.as_view()), # 给某个用户分配角色
    re_path('^api/v1/sys-user/\d+/role/\d+$', sys_user_views.UserRoleAPIView.as_view()), # 删除某个用户关联的某个角色
    # 组别相关
    re_path('^api/v1/sys-user/\d+/unrelated-groups$', sys_user_views.UnrelatedGroupsAPIView.as_view()), # 获取某个用户未关联组别
    re_path('^api/v1/sys-user/\d+/groups$', sys_user_views.UserGroupsAPIView.as_view()), # 给某个用户关联组别
    re_path('^api/v1/sys-user/\d+/group/\d+$', sys_user_views.UserGroupAPIView.as_view()), # 删除某个用户关联的某个组别
    # 账号相关
    re_path('^api/v1/sys-user/\d+/accounts$', sys_user_views.RelatedAccountListAPIView.as_view()), # 查询某个用户的关联账号列表
    re_path('^api/v1/sys-user/\d+/account$', sys_user_views.RelatedAccountAPIView.as_view()), # 给某个用户新增某个关联账号
    re_path('^api/v1/sys-user/\d+/account/\d+$', sys_user_views.RelatedAccountAPIView.as_view()), #修改，删除某个用户的某个关联账号
    # 获取用户关联的组别信息(按字段获取，支持排序)
    re_path('^api/v1/user/groups/details$', sys_user_views.UserGroupsDetailsAPIView.as_view()),


    # 系统管理-系统配置-组别管理
    path('api/v1/sys-groups', sys_group_views.GroupListAPIView.as_view()), # 查询组别列表，批量删除组别
    path('api/v1/sys-group', sys_group_views.GroupAPIView.as_view()), # 新增某个组别
    re_path('^api/v1/sys-group/\d+$', sys_group_views.GroupAPIView.as_view()), # 修改，删除某个用户

    # 系统管理-环境管理
    path('api/v1/envs', env_views.EnvListAPIView.as_view()), # 查询环境列表，批量删除环境
    path('api/v1/env', env_views.EnvAPIView.as_view()), # 新增某个环境
    re_path('^api/v1/env/\d+$', env_views.EnvAPIView.as_view()), # 修改，删除某个环境
    # 获取环境详细信息 # 供 “测试计划管理”模块使用
    re_path('^api/v1/envs/details$', env_views.EnvDetailsAPIView.as_view()),


    # 系统管理-测试阶段管理
    path('api/v1/test-phases', test_phase_views.TestPhaseListAPIView.as_view()), # 查询环境列表，批量删除测试阶段
    path('api/v1/test-phase', test_phase_views.TestPhaseAPIView.as_view()), # 新增某个测试阶段
    re_path('^api/v1/test-phase/\d+$', test_phase_views.TestPhaseAPIView.as_view()), # 修改，删除某个测试阶段
    # 获取测试阶段指定字信息# 供“测试用例管理模块使用”
    re_path('^api/v1/test-phases/details$', test_phase_views.TestPhaseDetailsAPIView.as_view()),

    # 系统管理-推送账号管理
    path('api/v1/msg-push-accounts', msg_push_account_views.MsgPushAccountListAPIView.as_view()), # 查询账号列表，批量删除账号
    path('api/v1/msg-push-account', msg_push_account_views.MsgPushAccountAPIView.as_view()), # 新增某个账号
    re_path('^api/v1/msg-push-account/\d+$', msg_push_account_views.MsgPushAccountAPIView.as_view()), # 修改，启用、禁用，删除某个账号
    # 组别相关
    re_path('^api/v1/msg-push-account/\d+/unrelated-groups$', msg_push_account_views.UnrelatedGroupsAPIView.as_view()), # 获取某个账号未关联组别
    re_path('^api/v1/msg-push-account/\d+/groups$', msg_push_account_views.MsgPushAccountGroupsAPIView.as_view()), # 给某个账号关联组别
    re_path('^api/v1/msg-push-account/\d+/group/\d+$', msg_push_account_views.MsgPushAccountGroupAPIView.as_view()), # 删除某个账号关联的某个组别

    # 产品视图-产品管理
    path('api/v1/products', product_views.ProductListAPIView.as_view()), # 查询产品列表，批量删除产品
    path('api/v1/product', product_views.ProductAPIView.as_view()), # 新增某个产品
    re_path('^api/v1/product/\d+$', product_views.ProductAPIView.as_view()), # 修改，删除某个产品
    # 批量查询产品列表详细信息,供 “测试计划管理”，“迭代管理”，“项目管理”模块使用
    path('api/v1/products/details', product_views.ProductsDetailsAPIView.as_view()),
    # 按指定字段获取某个产品关联的项目信息，供“测试计划管理”模块使用
    re_path('^api/v1/product/\d+/projects/details$', product_views.ProductProjectsDetailsAPIView.as_view()),
    # 按指定字段获取某个产品关联的迭代信息， 供“测试用例管理”模块使用
    re_path('^api/v1/product/\d+/sprints/details$', product_views.ProductSprintsDetailsAPIView.as_view()),

    # 产品视图-迭代管理
    re_path('^api/v1/product/\d+/sprints$', sprint_views.SprintListAPIView.as_view()), # 查询某个产品的迭代列表
    path('api/v1/sprints', sprint_views.SprintListAPIView.as_view()), # 批量删除某些产品迭代
    re_path('^api/v1/product/\d+/sprint$', sprint_views.SprintAPIView.as_view()), # 为某个产品新增某个迭代
    re_path('^api/v1/product/\d+/sprint/\d+$', sprint_views.SprintAPIView.as_view()), # 修改某个产品的某个迭代
    re_path('^api/v1/sprint/\d+$', sprint_views.SprintAPIView.as_view()), # 删除某个产品迭代

    # 按字段查询某个迭代的测试计划详细信息，供 迭代测试报告使用
    re_path('^api/v1/sprint/\d+/testplans$', sprint_views.SprintTestplansAPIView.as_view()),
     # 按字段查询指定迭代关联的项目及项目版本，供 迭代测试报告使用
    re_path('^api/v1/sprint/\d+/projectsWithVersions$', sprint_views.SprintProjectsVersionsAPIView.as_view()),


    # 项目视图-产品项目管理-项目管理
    path('api/v1/projects', project_views.ProjectListAPIView.as_view()), # 查询项目列表，批量删除项目
    path('api/v1/project', project_views.ProjectAPIView.as_view()), # 新增某个项目
    re_path('^api/v1/project/\d+$', project_views.ProjectAPIView.as_view()), # 修改，删除某个项目
    # 按指定字段批量获取项目详细信息 # 供项目"版本管理"，“迭代测试报告”使用
    path('api/v1/projects/details', project_views.ProjectsDetailsAPIView.as_view()),

    # 获取项目系统自定义字段
    path('api/v1/project/system/fields', project_views.ProjectSystemFieldsAPIVIEW.as_view()),

    # 关联、取消关联项目相关
    re_path('^api/v1/platform/\w+/projects$', project_views.PlatformProjectsAPIView.as_view()), # 获取某个平台关联的项目版本
    path('api/v1/jira/issue-types', project_views.JiraIssueTypeAPIView.as_view()), # 获取jira问题类型列表
    path('api/v1/jira/issue-custom-fields', project_views.JiraIssueCustomFieldAPIView.as_view()), # 获取jira问题自定义字段列表
    path('api/v1/zentao/defect-custom-fields', project_views.ZentaoDefectCustomFieldAPIView.as_view()), # 获取禅道缺陷定义字段列表

    # 为某个项目绑定某个平台的某个项目、更新某个项目已关联项目为某个平台的某个项目
    re_path('^api/v1/project/\d+/platform/\w+/platform-project/\d+$', project_views.PlatformProjectAssociationAPIView.as_view()),
    re_path('^api/v1/project/\d+/platform-project$', project_views.PlatformProjectAssociationAPIView.as_view()), # 为某个项目解除绑定已关联的平台项目


    # 项目视图-产品项目管理-版本管理
    re_path('^api/v1/project/\d+/versions$', project_version_views.ProjectVersionListAPIView.as_view()), # 查询某个项目的版本
    path('api/v1/project/versions', project_version_views.ProjectVersionListAPIView.as_view()), # 批量删除某些项目版本
    re_path('^api/v1/project/\d+/version$', project_version_views.ProjectVersionAPIView.as_view()), # 为某个项目新增版本
    re_path('^api/v1/project/\d+/version/\d+$', project_version_views.ProjectVersionAPIView.as_view()), # 修改某个项目的某个版本
    re_path('^api/v1/project/version/\d+$', project_version_views.ProjectVersionAPIView.as_view()), # 删除某个项目版本
    # 按指定字段获取某个项目关联的项目版本信息 # 供 “迭代测试报告”使用
    re_path('^api/v1/project/\d+/versions/details$', project_version_views.VersionsDetailsForProjectAPIView.as_view()),

    # 关联、取消关联平台项目版本相关
    re_path('^api/v1/project/\d+/project-versions$', project_version_views.PlatformProjectVersionsAPIView.as_view()), # 获取某个项目关联的平台项目版本列表
    # 为某个项目版本绑定某个平台项目版本、更新某个项目版本已关联项目版本为某个平台项目版本
    re_path('^api/v1/project-version/\d+/platform-project-version/\d+$', project_version_views.ProjectVersionAssociationAPIView.as_view()),
    re_path('^api/v1/project-version/\d+/platform-project-version$', project_version_views.ProjectVersionAssociationAPIView.as_view()), # 为某个项目版本解除绑定已关联的平台项目版本

    # # 项目视图-API项目管理

    path('api/v1/project-envs', project_env_views.ProjectEnvListView.as_view()), # 获取项目环境列表
    path('api/v1/project-env', project_env_views.ProjectEnvView.as_view()), # 新增项目环境
    re_path('^api/v1/project-env/\d+$', project_env_views.ProjectEnvView.as_view()), # 修改、删除项目环境

    # 测试视图-测试用例管理
    # 测试套件树
    path('api/v1/testcase-suite-tree', testcase_suite_views.TestcaseSuitTreeAPIView.as_view()), # 查询测试用例套件树
    path('api/v1/testcase-suite', testcase_suite_views.TestcaseSuitAPIView.as_view()), # 新增某个测试用例套件
    re_path('^api/v1/testcase-suite/\d+$', testcase_suite_views.TestcaseSuitAPIView.as_view()), # 修改、删除某个测试用例套件
    re_path('^api/v1/testcase-suite/\d+/testcases-copied$', testcase_suite_views.PasteTestcasesCopiedAPIView.as_view()), # 黏贴拷贝的测试用例到某指定测试集
    re_path('^api/v1/testcase-suite/\d+/testcases-cut$', testcase_suite_views.PasteTestcasesCutAPIView.as_view()), # 黏贴测试用例到某指定测试集
    path('api/v1/paste-suite-by-structure', testcase_suite_views.PasteSuiteByStructureAPIView.as_view()), # 按结构黏贴剪切的测试集
    re_path('^api/v1/paste-suite-cut/\d+$', testcase_suite_views.PasteSuiteCutAPIView.as_view()), # 黏贴剪切的测试集到目标测试集下

    # 用例相关
    re_path('^api/v1/testsuite/\d+/testcases$', testcase_views.TestcaseListAPIView.as_view()), # 查询、批量删除、批量修改某个测试套件下的测试用例
    re_path('^api/v1/product/\d+/testcases$', testcase_views.TestcaseListAPIView.as_view()), # 给某个产品批量导入测试用例
    re_path('^api/v1/testsuite/\d+/testcases/export/excel$', testcase_views.TestcaseExportAPIView.as_view()), # 导出某个测试套件下的测试用例
    re_path('^api/v1/testsuite/\d+/testcases/export/xmind$', testcase_views.XMindTestcaseExportAPIView.as_view()), # 导出某个测试套件下的测试用例
    re_path('^api/v1/testsuite/\d+/testcase$', testcase_views.TestcaseAPIView.as_view()), # 给某个测试套件新增某个用例
    re_path('^api/v1/testsuite/\d+/testcase/\d+$', testcase_views.TestcaseAPIView.as_view()), # 修改，删除某个测试套件下的某个用例
    re_path('^api/v1/sprint/\d+/testcases/bycopy$', testcase_views.CopyTestcasesToSprintAPIView.as_view()), # 复制用例到某个迭代

    #附件相关
    re_path('^api/v1/testcase/\d+/attachments$', testcase_attachment_views.TestcaseAttachmentListAPIView.as_view()), # 获取测试用例关联的附件列表
    re_path('^api/v1/testcase/\d+/attachment$', testcase_attachment_views.TestcaseAttachmentAPIView.as_view()), # 给测试用例添加附件
    re_path('^api/v1/testcase/\d+/attachment/\d+$', testcase_attachment_views.TestcaseAttachmentAPIView.as_view()), # 删除、下载测试用例关联的附件

    # 测试视图-测试计划管理
    re_path('^api/v1/product/\d+/testplans$', testplan_views.TestplanListAPIView.as_view()), # 获取指定产品的测试计划列表
    re_path('^api/v1/product/testplans$', testplan_views.TestplanListAPIView.as_view()), # 批量删除某些产品测试计划
    re_path('^api/v1/product/\d+/testplan$', testplan_views.TestplanAPIView.as_view()), # 为指定产品新增某个测试计划
    re_path('^api/v1/product/testplan/\d+$', testplan_views.TestplanAPIView.as_view()), # 修改、删除某个产品测试计划、查询某个产品测试计划的信息

    # 测试用例相关
    # 为某个迭代测试计划关联测试用例、批量删除某个迭代测试计划关联的用例,、批量修改某个迭代测试计划关联的某个测试套件下的用例
    re_path('^api/v1/testplan/\d+/testcases$', testplan_views.TestplanTestcasesAPIView.as_view()),
    re_path('^api/v1/testplan/\d+/testcases/guids$', testplan_views.TestplanTestcasesGuidsAPIView.as_view()), # 获取测试计划关联的用例的guid
    re_path('^api/v1/testplan/\d+/testsuite/\d+/testcases$', testplan_testcase_views.TestplanTestcaseListAPIView.as_view()), # 获取某个测试计划关联的某个测试套件下的用例列表
    re_path('^api/v1/testplan/\d+/testcase/\d+$', testplan_testcase_views.TestplanTestcaseAPIView.as_view()), # 逐条删除、修改某个测试计划关联的某个用例
    re_path('^api/v1/testplan/\d+/testcase/\d+/result$', testplan_testcase_views.TestplanTestcaseResultAPIView.as_view()), # 逐条修改某个测试计划关联的某个用例的测试结果
    re_path('^api/v1/testplan/\d+/testcases/results$', testplan_testcase_views.TestplanTestcasesResultsAPIView.as_view()), # 批量修改某个测试计划关联的部分用例的测试结果


    # 测试视图-测试报告管理-迭代测试报告
    re_path('^api/v1/sprint/\d+/testreport/statistics$', sprint_test_report_views.SprintTestReportStatisticsAPIView.as_view()),  # 获取某个迭代测试报告统计数据
    re_path('^api/v1/sprint/\d+/testreport$', sprint_test_report_views.SprintTestReportAPIView.as_view()),  # 为某个迭代新增迭代测试报告
    re_path('^api/v1/sprint/testreport/\d+$', sprint_test_report_views.SprintTestReportAPIView.as_view()),    # 查看\修改某个迭代测试报告
    re_path('^api/v1/sprint/\d+/testreports/details$', sprint_test_report_views.SprintTestReportsDetailsAPIView.as_view()),    # 按字段获取某个迭代的迭代测试报告具体信息
    re_path('^api/v1/sprint/testreport/\d+/pdf$', sprint_test_report_views.SprintTestreportPDFAPIView.as_view()),    # 下载某个迭代报告（PDF版）

    #
    # # 度量-项目迭代统计
    # path('api/v1/sprints/statistics', sprints_statistics_views.SprintsStatisticsAPIView.as_view()), # 获取项目迭代统计数据
    # path('api/v1/online/statistics', online_statistics_views.OnlineStatisticsAPIView.as_view()), # 获取项目迭代统计数据
    #

    # # 工作台
    # path('api/v1/workbench/sprints/statistics', workbench_views.WorkbenchSprintsStatisticsAPIView.as_view()), # 获取工作台迭代统计信息
    # path('api/v1/workbench/groups/defects-trend-statistics', workbench_views.GroupDefectTrendStatisticsAPIView.as_view()) # 根据所选时间范围及用户当前关联组别获取组别缺陷趋势统计信息

]
