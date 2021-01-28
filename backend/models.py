from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

# refresh token
class RefreshToken(models.Model):
    key = models.CharField(max_length=80, verbose_name='key')
    created = models.DateTimeField(verbose_name='创建时间')
    user_id = models.IntegerField(unique=True, verbose_name='创建人ID')

    class Meta:
            db_table = 'tb_authtoken_refresh_token'
            verbose_name = 'refresh token表'
            verbose_name_plural = verbose_name

class User(AbstractUser):
    name = models.CharField(max_length=50, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    job_number = models.CharField(max_length=20, verbose_name='工号')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'tb_user'  # 指明数据库表名
        verbose_name = '系统用户表'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

class SysMenu(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    parent_id = models.IntegerField(verbose_name='上级ID')
    type = models.CharField(max_length=5, verbose_name='资源类型')
    name = models.CharField(max_length=50, verbose_name='资源名称')
    desc = models.CharField(max_length=300, null=True,  blank=True, verbose_name='资源描述')
    url = models.CharField(max_length=100, null=True,  blank=True, verbose_name='资源url')
    icon = models.CharField(max_length=30, null=True,  blank=True, verbose_name='资源图标')
    perms = models.CharField(max_length=50, null=True, blank=True, verbose_name='权限标识')
    require_auth = models.BooleanField(default=True, verbose_name='是否需要登录')
    show = models.BooleanField(default=True, verbose_name='是否在前端展示')
    show_without_auth = models.BooleanField(default=False, verbose_name='未登陆是否展示')
    collapsed = models.BooleanField(default=False, verbose_name='是否折叠')
    order = models.IntegerField(verbose_name='顺序')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_sys_menu'  # 指明数据库表名
        verbose_name = '系统菜单表'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

class SysRole(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    name = models.CharField(max_length=50, verbose_name='角色名称')
    desc = models.CharField(max_length=300, null=True,  blank=True, verbose_name='角色描述')
    is_active = models.BooleanField(default=1, verbose_name='是否启用')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_sys_role'
        verbose_name = '系统角色表'
        verbose_name_plural = verbose_name

class SysRoleMenu(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    role_id = models.IntegerField(verbose_name='角色ID')
    menu_id = models.IntegerField(verbose_name='菜单ID')

    class Meta:
        db_table = 'tb_sys_role_menu'
        verbose_name = '角色菜单关联表'
        verbose_name_plural = verbose_name

class SysUserRole(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    user_id = models.IntegerField(verbose_name='用户ID')
    role_id = models.IntegerField(verbose_name='角色ID')

    class Meta:
        db_table = 'tb_sys_user_role'
        verbose_name = '用户角色关联表'
        verbose_name_plural = verbose_name

class SysGroup(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    name = models.CharField(max_length=50, unique=True, verbose_name='组别名称')
    desc = models.CharField(max_length=300, null=True,  blank=True, verbose_name='组别描述')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_sys_group'
        verbose_name = '系统组别表'
        verbose_name_plural = verbose_name

class SysGroupRelatedGroup(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    group_id = models.IntegerField(verbose_name='组别ID')
    related_group  = models.CharField(max_length=50, verbose_name='组别')
    related_group_id  = models.CharField(max_length=50, verbose_name='关联组别的ID')
    platform  = models.CharField(max_length=30, verbose_name='平台')

    class Meta:
        db_table = 'tb_sys_group_related_group'
        verbose_name = '用户账号关联表'
        verbose_name_plural = verbose_name

class SysUserGroup(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    user_id = models.IntegerField(verbose_name='用户ID')
    group_id = models.IntegerField(verbose_name='组别ID')

    class Meta:
        db_table = 'tb_sys_user_group'
        verbose_name = '用户组别关联表'
        verbose_name_plural = verbose_name

class SysUserAccount(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    user_id = models.IntegerField(verbose_name='用户ID')
    account  = models.CharField(max_length=50, verbose_name='账号')
    password  = models.CharField(max_length=32, verbose_name='密码')
    platform  = models.CharField(max_length=30, verbose_name='平台')

    class Meta:
        db_table = 'tb_sys_user_account'
        verbose_name = '用户账号关联表'
        verbose_name_plural = verbose_name


class Env(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    name = models.CharField(max_length=50, verbose_name='环境名称')
    desc = models.CharField(max_length=300, null=True,  blank=True, verbose_name='环境描述')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_env'
        verbose_name = '环境表'
        verbose_name_plural = verbose_name


class TestPhase(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    name = models.CharField(max_length=50, verbose_name='执行阶段')
    code = models.CharField(max_length=20, verbose_name='唯一编码')
    desc = models.CharField(max_length=300, null=True,  blank=True, verbose_name='描述')
    order = models.IntegerField(verbose_name='阶段顺序')
    default = models.BooleanField(verbose_name='是否默认测试阶段')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_test_phase'
        verbose_name = '测试阶段表'
        verbose_name_plural = verbose_name

class MsgPushAccount(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    account = models.CharField(max_length=50, verbose_name='账号')
    type = models.CharField(max_length=20, verbose_name='类型')
    desc = models.CharField(max_length=300, null=True,  blank=True, verbose_name='账号描述')
    is_active = models.BooleanField(default=1, verbose_name='是否启用')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_msg_push_account'
        verbose_name = '消息推送账号表'
        verbose_name_plural = verbose_name

class MsgPushAccountGroup(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    account_id = models.IntegerField(verbose_name='账户ID')
    group_id = models.IntegerField(verbose_name='组别ID')

    class Meta:
        db_table = 'tb_msg_push_account_group'
        verbose_name = '消息推送账号和组别关联表'
        verbose_name_plural = verbose_name


class Product(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    name = models.CharField(max_length=50, verbose_name='产品名称')
    code = models.CharField(max_length=50, verbose_name='产品编码')
    status =  models.CharField(max_length=50, verbose_name='产品状态')
    product_owner_id = models.IntegerField(null=True, blank=True, verbose_name='产品负责人id')
    product_owner = models.CharField(null=True, blank=True, max_length=50, verbose_name='产品负责人')
    develop_owner_id = models.IntegerField(null=True, verbose_name='研发负责人id')
    develop_owner = models.CharField(null=True, blank=True, max_length=50, verbose_name='研发负责人')
    test_owner_id = models.IntegerField(null=True, verbose_name='测试负责人id')
    test_owner = models.CharField(null=True, blank=True, max_length=50, verbose_name='测试负责人')
    desc = models.CharField(max_length=300, null=True,  blank=True, verbose_name='描述')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    external_product_id = models.CharField(null=True, blank=True, max_length=50, verbose_name='关联的外部产品ID')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_product'
        verbose_name = '产品表'
        verbose_name_plural = verbose_name


class Sprint(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    name = models.CharField(max_length=50, verbose_name='迭代名称')
    version = models.CharField(null=True, blank=True, max_length=50, verbose_name='版本')
    begin_time =  models.DateField(verbose_name='预估开始时间')
    end_time =  models.DateField(verbose_name='预估结束时间')
    status = models.CharField(max_length=10, verbose_name='迭代状态')
    desc = models.CharField(max_length=300, null=True,  blank=True, verbose_name='描述')
    product_id = models.CharField(max_length=1000, verbose_name='迭代关联的产品ID')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_sprint'
        verbose_name = '产品迭代表'
        verbose_name_plural = verbose_name


class Project(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    name = models.CharField(max_length=50, verbose_name='项目名称')
    status = models.CharField(max_length=10, verbose_name='项目状态')
    begin_time =  models.DateField(verbose_name='预估开始时间')
    end_time =  models.DateField(verbose_name='预估结束时间')
    product_id = models.IntegerField(verbose_name='关联的产品ID')
    desc = models.CharField(max_length=300, null=True,  blank=True, verbose_name='描述')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_project'
        verbose_name = '项目表'
        verbose_name_plural = verbose_name


class ProjectAssociated(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    project_id = models.IntegerField(verbose_name='项目id')
    platform_project_name = models.CharField(max_length=50, verbose_name='关联项目名称')
    platform_project_id = models.CharField(max_length=32, verbose_name='关联项目id')
    platform = models.CharField(max_length=50, verbose_name='关联项目所在的平台')
    defect_issue_type_id = models.CharField(null=True, blank=True, max_length=32, verbose_name='缺陷归属类型id(主要针对jira')
    defect_status_map = models.CharField(null=True, blank=True, max_length=500, verbose_name='缺陷状态映射')
    defect_severity_map = models.CharField(null=True, blank=True, max_length=500, verbose_name='缺陷严重级别映射')
    custom_field_map = models.CharField(null=True, blank=True, max_length=1000, verbose_name='自定义字段映射')
    creater_id = models.IntegerField(verbose_name='创建人id')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人id')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'tb_project_associated'
        verbose_name = '项目与外部平台项目关联表'
        verbose_name_plural = verbose_name


class ProjectVersion(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    name = models.CharField(max_length=50, verbose_name='版本名称')
    begin_time =  models.DateField(verbose_name='预估开始时间')
    end_time =  models.DateField(verbose_name='预估结束时间')
    desc = models.CharField(max_length=300, null=True,  blank=True, verbose_name='描述')
    project_id = models.IntegerField(verbose_name='关联的项目ID')
    product_id = models.IntegerField(verbose_name='关联的产品ID')
    sprint_id = models.IntegerField(verbose_name='关联的迭代ID')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_project_version'
        verbose_name = '项目版本表'
        verbose_name_plural = verbose_name

class ProjectVersionAssociated(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    platform_project_version_name = models.CharField(max_length=50, verbose_name='关联项目版本名称')
    platform_project_version_id = models.CharField(max_length=32, verbose_name='关联项目版本id')
    platform = models.CharField(max_length=50, verbose_name='关联版本所在的平台')
    project_version_id = models.IntegerField(verbose_name='项目版本id')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'tb_project_version_associated'
        verbose_name = '项目版本与外部平台项目版本关联表'
        verbose_name_plural = verbose_name


class TestcaseSuite(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    name = models.CharField(max_length=50, verbose_name='套件名称')
    type = models.CharField(max_length=20, verbose_name='套件类型') # 可选值  base-基线测试套件 sprint-迭代测试套件
    parent_id = models.IntegerField(verbose_name='父级套件ID') # 顶级套件 parent_id = -1
    product_id = models.IntegerField(verbose_name='套件所属产品')
    sprint_id = models.IntegerField(verbose_name='sprintID')
    all_upper_node_ids = models.CharField(max_length=1000, verbose_name='所有父级套件ID')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_testcase_suite'
        verbose_name = '测试用例套件表'
        verbose_name_plural = verbose_name


# 测试视图-测试用例管理-迭代测试用例套件和基线测试用例套件关联表
class SprintBaseCaseSuiteRelation(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    base_case_suite_id = models.IntegerField(null=True, verbose_name='base 测试用例套件id')
    sprint_case_suite_id = models.IntegerField(null=True, verbose_name='迭代测试套件id')

    class Meta:
        db_table = 'tb_sprint_base_case_suite_relation'
        verbose_name = '迭代测试用例套件和基线测试用例套件关联表'
        verbose_name_plural = verbose_name


class APIProjectGroup(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    name = models.CharField(max_length=50, verbose_name='分组名称')
    parent_id = models.IntegerField(verbose_name='父级分组ID') # 顶级分组 parent_id = -1
    type = models.CharField(max_length=10, verbose_name='分组类型')
    desc = models.CharField(blank=True, null=True, max_length=300, verbose_name='描述')
    order = models.IntegerField(verbose_name='顺序ID')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_api_project_group'
        verbose_name = 'API项目分组表'
        verbose_name_plural = verbose_name


class APIProject(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    name = models.CharField(max_length=50, verbose_name='项目名称')
    group_id = models.IntegerField(verbose_name='项目分组ID')
    desc = models.CharField(blank=True, null=True, max_length=300, verbose_name='项目描述')
    status = models.CharField(blank=True, null=True, max_length=15, verbose_name='项目状态')
    swagger_url = models.CharField(blank=True, null=True, max_length=100, verbose_name='swagger地址')
    mock_base_url = models.CharField(blank=True, null=True, max_length=100, verbose_name='mock基础地址')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_api_project'
        verbose_name = 'API项目表'
        verbose_name_plural = verbose_name

class APIProjectFavorites(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    project_id = models.IntegerField(verbose_name='项目id')
    user_id = models.IntegerField(verbose_name='用户id')

    class Meta:
        db_table = 'tb_api_project_favorities'
        unique_together = ("project_id", "user_id")
        verbose_name = 'API项目收藏表'
        verbose_name_plural = verbose_name

class ProjectEnv(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    project_id = models.IntegerField(verbose_name='项目id')
    env_name = models.CharField(max_length=20, verbose_name='环境名称')
    addr = models.CharField(max_length=200, verbose_name='项目地址')
    headers = models.CharField(null=True, blank=True, max_length=1000, verbose_name='全局请求头')
    cookies = models.CharField(null=True, blank=True, max_length=1000, verbose_name='全局Cookie')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'tb_project_env'
        verbose_name = 'API项目环境配置表'
        verbose_name_plural = verbose_name


# 开发视图-接口管理-接口模块划分表
class APIGroup(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    name = models.CharField(max_length=50, verbose_name='模块名称')
    parent_id = models.IntegerField(verbose_name='父级模块ID')  # 顶级模块 parent_id = -1
    order = models.IntegerField(verbose_name='模块顺序')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')
    all_upper_node_ids = models.CharField(max_length=1000, verbose_name='所有父级模块ID')
    project_id = models.IntegerField(verbose_name='所属项目ID')
    project_group_id = models.IntegerField(verbose_name='所属项目分组id')

    class Meta:
        db_table = 'tb_api_group'
        verbose_name = 'API模块划分表'
        verbose_name_plural = verbose_name

# 开发视图-接口管理-项目接口列表
class ProjectAPI(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    group_id = models.IntegerField(verbose_name='所属分类id')
    project_id = models.IntegerField(verbose_name='所属项目id')
    name = models.CharField(blank=True, max_length=500, verbose_name='接口名称')
    status = models.CharField(max_length=20, verbose_name='接口状态')
    method = models.CharField(max_length=10, verbose_name='接口请求方法')
    path = models.CharField(max_length=500, verbose_name='接口url')
    # req_params =
    # req_body_form =
    # req_headers =
    # req_body_type
    # res_body_type
    # res_body
    # req_body_other
    desc = models.CharField(blank=True,max_length=1000, verbose_name='接口描述')
    #
    # tags = models.CharField(blank=True,max_length=1000, verbose_name='接口标签')
    # opened = models.BooleanField(default=False, verbose_name='是否对外开放')
    #
    #
    # priority = models.CharField(blank=True, max_length=10, verbose_name='优先级')

    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_project_api'
        verbose_name = '项目API'
        verbose_name_plural = verbose_name

class ZtProjectVersion(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    name = models.CharField(max_length=50, verbose_name='版本名称')
    begin_time =  models.DateField(verbose_name='预估开始时间')
    end_time =  models.DateField(verbose_name='预估结束时间')
    desc = models.CharField(max_length=300, null=True,  blank=True, verbose_name='描述')
    project_id = models.IntegerField(verbose_name='关联的项目ID')
    project_version_id = models.IntegerField(verbose_name='关联的项目版本ID')
    product_id = models.IntegerField(verbose_name='关联的产品ID')
    zt_project_id = models.IntegerField(blank=True, null=True,verbose_name='关联的禅道项目ID')
    zt_product_id = models.IntegerField(verbose_name='关联的禅道产品ID')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_zt_project_version'
        verbose_name = '禅道项目版版本表'
        verbose_name_plural = verbose_name


# 测试视图-测试用例管理-迭代测试用例表
class SprintTestcase(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    guid = models.CharField(blank=True, max_length=50, verbose_name='全局唯一标识')
    custom_no = models.CharField(null=True,blank=True, max_length=50, verbose_name='用例编号')
    suite_id = models.IntegerField(verbose_name='测试集id')
    product_id = models.IntegerField(verbose_name='所属产品id')
    sprint_id = models.IntegerField(null=True, verbose_name='所属迭代id')
    name = models.CharField(blank=True, max_length=500, verbose_name='测试用例名称')
    priority = models.CharField(blank=True, max_length=10, verbose_name='优先级')
    executed_each_sprint = models.CharField(max_length=100, verbose_name='是否每个迭代都要执行')
    execution_method = models.CharField(max_length=50, verbose_name='执行方法')
    execution_phase = models.CharField(max_length=100,verbose_name='执行阶段')
    tags = models.CharField(blank=True,max_length=1000, verbose_name='用例标签')
    desc = models.CharField(blank=True,max_length=1000, verbose_name='用例描述')
    precondition = models.CharField(blank=True, max_length=1000, verbose_name='前置条件')
    steps = models.TextField(blank=True, default=[], verbose_name='测试步骤')
    postcondition = models.CharField(blank=True, max_length=1000, verbose_name='后置条件')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_sprint_testcase'
        verbose_name = '迭代测试用例表'
        verbose_name_plural = verbose_name

# 测试视图-测试用例管理-基线测试用例表
class BaseTestcase(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    guid = models.CharField(blank=True, max_length=50, verbose_name='全局唯一标识')
    custom_no = models.CharField(null=True, blank=True, max_length=50, verbose_name='用例编号')
    suite_id = models.IntegerField(verbose_name='测试集id')
    product_id = models.IntegerField(verbose_name='所属产品id')
    sprint_id = models.IntegerField(null=True, verbose_name='所属迭代id')
    sprint_testcase_guid = models.CharField(null=True, max_length=50, verbose_name='关联的sprint测试用例guid')
    name = models.CharField(blank=True, max_length=500, verbose_name='测试用例名称/测试集路径')
    priority = models.CharField(blank=True, max_length=10, verbose_name='优先级')
    executed_each_sprint = models.CharField(max_length=100, verbose_name='是否每个迭代都要执行')
    execution_method = models.CharField(max_length=50, verbose_name='执行方法')
    execution_phase = models.CharField(max_length=100,verbose_name='执行阶段')
    tags = models.CharField(blank=True,max_length=1000, verbose_name='用例标签')
    desc = models.CharField(blank=True,max_length=1000, verbose_name='用例描述')
    precondition = models.CharField(blank=True, max_length=1000, verbose_name='前置条件')
    steps = models.TextField(blank=True, default=[], verbose_name='测试步骤')
    postcondition = models.CharField(blank=True, max_length=1000, verbose_name='后置条件')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_base_testcase'
        verbose_name = '基线测试用例表'
        verbose_name_plural = verbose_name


# 测试视图-测试用例管理-测试用例附件表
class TestcaseAttachment(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    guid = models.CharField(max_length=50, verbose_name='附件guid')
    case_guid = models.CharField(max_length=50, verbose_name='关联测试用例的guid')
    sprint_case_guid = models.CharField(null=True, max_length=50, verbose_name='关联迭代测试用例的guid')
    attachment_guid = models.CharField(null=True, max_length=50, verbose_name='关联的迭代用例的附件guid')
    name = models.CharField(max_length=200, verbose_name='附件名称')
    file_path = models.CharField(max_length=200, verbose_name='附件相对路径')
    creater_id = models.IntegerField(verbose_name='上传者ID')
    create_time =  models.DateTimeField(verbose_name='上传时间')
    is_delete = models.BooleanField(default=0, verbose_name='是否删除')

    class Meta:
        db_table = 'tb_testcase_attachment'
        verbose_name = '测试用例附件表'
        verbose_name_plural = verbose_name


# 系统管理-下载中心-其它普通文件
class NormalFileDownload(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    type = models.CharField(max_length=20, verbose_name='文件类型')
    name = models.CharField(max_length=200, verbose_name='文件名称')
    file_path = models.CharField(max_length=200, verbose_name='文件相对路径')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater = models.CharField(max_length=50, verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater = models.CharField(max_length=50, verbose_name='更新人姓名')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=0, verbose_name='是否删除')

    class Meta:
        db_table = 'tb_normal_file_download'
        verbose_name = '已下载的普通文件表'
        verbose_name_plural = verbose_name

# 测试视图-测试计划管理-迭代测试计划表
class SprintTestplan(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    name = models.CharField(max_length=50, verbose_name='计划名称')
    desc = models.CharField(blank=True, null=True, max_length=300, verbose_name='计划描述')
    begin_time =  models.DateField(verbose_name='预估开始时间')
    end_time =  models.DateField(verbose_name='预估结束时间')
    sprint_id = models.IntegerField(verbose_name='所属迭代ID')
    sprint_name = models.CharField(max_length=50, verbose_name='所属迭代名称')
    product_id = models.IntegerField(verbose_name='关联产品ID')
    start_time = models.DateTimeField(null=True, verbose_name='实际开始时间')
    finish_time = models.DateTimeField(null=True, verbose_name='实际完成时间')
    project_names = models.CharField(max_length=200, verbose_name='关联项目名称')
    project_ids = models.CharField(max_length=200, verbose_name='关联项目id')
    env_names = models.CharField(max_length=100, verbose_name='执行环境名称')
    status = models.CharField(max_length=10, verbose_name='计划状态')
    case_num_executed = models.IntegerField(verbose_name='已执行用例数')
    case_num_success = models.IntegerField(verbose_name='执行成功用例数')
    case_num_blocked = models.IntegerField(verbose_name='执行阻塞用例数')
    case_num_fail = models.IntegerField(verbose_name='执行失败用例数')
    case_num_related = models.IntegerField(verbose_name='关联用例总数')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    updater_name = models.CharField(max_length=10,verbose_name='更新人姓名')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_sprint_testplan'
        verbose_name = '迭代测试计划表'
        verbose_name_plural = verbose_name



# 测试视图-测试计划管理-迭代测试计划关联用例表
class SprintTestplanTestcase(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    testplan_id = models.IntegerField(verbose_name='关联的迭代测试计划Id')
    guid = models.CharField(blank=True, max_length=50, verbose_name='用例的全局唯一标识')
    custom_no = models.CharField(null=True, blank=True, max_length=50, verbose_name='用例编号')
    suite_id = models.IntegerField(verbose_name='测试集id')
    product_id = models.IntegerField(verbose_name='所属产品id')
    sprint_id = models.IntegerField(null=True, verbose_name='所属迭代id')
    sprint_testcase_guid = models.CharField(null=True, max_length=50, verbose_name='关联的sprint测试用例guid')
    name = models.CharField(blank=True, max_length=500, verbose_name='测试用例名称')
    priority = models.CharField(blank=True, max_length=10, verbose_name='优先级')
    executed_each_sprint = models.CharField(max_length=100, verbose_name='是否每个迭代都要执行')
    execution_method = models.CharField(max_length=50, verbose_name='执行方法')
    execution_phase = models.CharField(max_length=100,verbose_name='执行阶段')
    tags = models.CharField(blank=True,max_length=1000, verbose_name='用例标签')
    desc = models.CharField(blank=True,max_length=1000, verbose_name='用例描述')
    precondition = models.CharField(blank=True, max_length=1000, verbose_name='前置条件')
    steps = models.TextField(blank=True, default=[], verbose_name='测试步骤')
    postcondition = models.CharField(blank=True, max_length=1000, verbose_name='后置条件')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10, blank=True, verbose_name='创建人姓名')
    create_time =  models.DateTimeField(verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, blank=True, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(verbose_name='更新时间')
    result = models.CharField(max_length=10, verbose_name='测试结果')
    remark = models.CharField(blank=True, null=True, max_length=500, verbose_name='测试备注')
    execution_time = models.DateTimeField(null=True, verbose_name='执行时间')
    tester_id = models.IntegerField(null=True, blank=True, verbose_name='测试人ID')
    tester_name = models.CharField(null=True, blank=True, max_length=10, verbose_name='测试人姓名')
    assigned_to = models.CharField(max_length=10, verbose_name='指派给对象') # 默认为创建人
    assigned_to_id = models.IntegerField(verbose_name='指派给对象id') # 默认为创建人ID

    class Meta:
        db_table = 'tb_sprint_testplan_testcase'
        verbose_name = '迭代测试计划关联用例表'
        verbose_name_plural = verbose_name


# 测试视图-测试计划管理-测试用例附件表
class SprintTestplanTestcaseAttachment(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    guid = models.CharField(max_length=50, verbose_name='附件guid')
    testplan_id = models.IntegerField(verbose_name='关联的迭代测试计划Id')
    case_guid = models.CharField(max_length=50, verbose_name='关联测试用例的guid')
    attachment_guid = models.CharField(null=True, blank=True, max_length=50, verbose_name='关联的迭代用例的附件guid')
    name = models.CharField(max_length=200, verbose_name='附件名称')
    file_path = models.CharField(max_length=200, verbose_name='附件相对路径')
    creater_id = models.IntegerField(verbose_name='上传者ID')
    create_time =  models.DateTimeField(verbose_name='上传时间')
    is_delete = models.BooleanField(default=0, verbose_name='是否删除')


    class Meta:
        db_table = 'tb_sprint_testplan_testcase_attachment'
        verbose_name = '迭代测试计划关联用例附件表'
        verbose_name_plural = verbose_name

# 测试视图-测试报告管理-迭代测试报告
class SprintTestReport(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    sprint_id = models.IntegerField(verbose_name='关联的迭代id')
    title = models.CharField(max_length=100, verbose_name='报告标题')
    introduction = models.CharField(blank=True, null=True, max_length=1000, verbose_name='引言')
    related_plans = models.TextField(verbose_name='关联的测试计划')
    test_scope = models.CharField(blank=True, null=True, max_length=1000, verbose_name='测试范围')
    requirement_pie =  models.TextField(blank=True, null=True, verbose_name='需求饼图数据')
    defect_status_pie =  models.TextField(verbose_name='缺陷状态饼图数据')
    defect_severity_pie =  models.TextField(verbose_name='缺陷严重级别饼图数据')
    defect_type_pie =  models.TextField(verbose_name='缺陷类型饼图数据')
    case_execution_pie =  models.TextField(verbose_name='用例执行饼图数据')
    defect_source_bar = models.TextField(verbose_name='缺陷根源柱状图数据')
    case_execution_individual =  models.TextField(verbose_name='个人用例执行统计')
    defects_created_individual =  models.TextField(verbose_name='个人提交缺陷数据')
    defects_resolved_individual =  models.TextField(verbose_name='个人处理缺陷数据')
    conclusion = models.CharField(max_length=1000, verbose_name='测试结论')
    suggestion = models.CharField(blank=True, max_length=1000, verbose_name='相关建议')
    risk_analysis = models.CharField(blank=True, max_length=1000, verbose_name='风险分析')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater_name = models.CharField(max_length=10,verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    updater_name = models.CharField(max_length=10, verbose_name='更新人姓名')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    if_regenerate_pdf = models.BooleanField(default=False, verbose_name='是否需要重新生成PDF标记 0不需要 1需要')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'tb_sprint_testreport'
        verbose_name = '迭代测试报告表'
        verbose_name_plural = verbose_name


# 测试视图-测试报告管理-迭代测试报告-遗留未关闭缺陷统计列表
class SprintTestReportUnclosedDefectStatistics(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    sprint_report_id = models.IntegerField(verbose_name='迭代测试报告ID')
    defect_id = models.CharField(max_length=50, verbose_name='缺陷ID')
    title = models.CharField(max_length=200, verbose_name='缺陷标题')
    severity = models.CharField(max_length=10, verbose_name='严重程度')
    status = models.CharField(max_length=10, verbose_name='缺陷状态')
    remark = models.CharField(null=True,blank=True, max_length=200, verbose_name='补充说明')
    creater = models.CharField(max_length=20, verbose_name='缺陷提交人')
    person_liable = models.CharField(null=True, blank=True, max_length=20, verbose_name='缺陷责任人')
    assigned_to = models.CharField(null=True,blank=True, max_length=20, verbose_name='指派给')
    resolver = models.CharField(null=True, blank=True, max_length=20, verbose_name='处理人')
    platform = models.CharField(max_length=20, verbose_name='所属平台')

    class Meta:
        db_table = 'tb_sprint_testreport_unclosed_defect_statistics'
        verbose_name = '迭代测试报告遗留未关闭缺陷统计列表'
        verbose_name_plural = verbose_name


# 系统管理-下载中心-迭代PDF测试报告
class SprintPDFTestReport(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    testreport_id = models.CharField(max_length=50, verbose_name='关联测试报告的id')
    name = models.CharField(max_length=200, verbose_name='报告名称')
    file_path = models.CharField(max_length=200, verbose_name='附件相对路径')
    creater_id = models.IntegerField(verbose_name='创建人ID')
    creater = models.CharField(max_length=50, verbose_name='创建人姓名')
    create_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updater = models.CharField(max_length=50, verbose_name='更新人姓名')
    updater_id = models.IntegerField(verbose_name='更新人ID')
    update_time =  models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=0, verbose_name='是否删除')

    class Meta:
        db_table = 'tb_sprint_pdf_testreport'
        verbose_name = '迭代pdf测试报告表'
        verbose_name_plural = verbose_name

# 测试视图-测试报告管理-迭代测试报告-迭代测试报告组别缺陷趋势统计表
class ZentaoGroupDefectTrendDailyStatistics(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='自增id')
    data_date =  models.DateField(verbose_name='数据日期')
    group_id = models.IntegerField(verbose_name='组别ID')
    groupname = models.CharField(max_length=150, verbose_name='组别名称')
    defect_total = models.IntegerField(verbose_name='缺陷总数')
    defect_increased =  models.IntegerField(verbose_name='新增缺陷数')
    defect_di = models.CharField(max_length=10, verbose_name='缺陷遗留DI值')
    class Meta:
        db_table = 'tb_zentao_group_defect_trend_daily_statistics'
        verbose_name = '禅道组别缺陷趋势统计日常统计表'
        verbose_name_plural = verbose_name


class TpadDefect(models.Model):
    id = models.CharField(max_length=50, primary_key=True, verbose_name='ID')
    title = models.CharField(max_length=200, verbose_name='标题')
    severity = models.CharField(blank=True, max_length=10, verbose_name='严重程度')
    event_level = models.CharField(blank=True, null=True, max_length=20, verbose_name='事件等级')
    status = models.CharField(max_length=20, verbose_name='状态')
    bugtype = models.CharField(max_length=20, verbose_name='缺陷类型')
    source = models.CharField(null=True, blank=True, max_length=20, verbose_name='缺陷根源')
    product = models.CharField(max_length=50, verbose_name='所属产品') # custom_field_
    created = models.DateTimeField(verbose_name='创建时间')
    resolved = models.DateTimeField(null=True, blank=True, verbose_name='解决时间')
    closed = models.DateTimeField(null=True, blank=True, verbose_name='关闭时间')
    version_report = models.CharField(max_length=40, null=True, blank=True, verbose_name='发现版本')
    reporter = models.CharField(max_length=20, verbose_name='创建人')
    closer = models.CharField(max_length=20, null=True, blank=True, verbose_name='关闭人')
    priority = models.CharField(max_length=20, null=True, blank=True, verbose_name='优先级')
    iteration_id = models.CharField(max_length=50, null=True, blank=True, verbose_name='迭代ID')
    module =  models.CharField(max_length=50,null=True, blank=True, verbose_name='模块')
    version_test =  models.CharField(max_length=20, null=True, blank=True, verbose_name='验证版本')
    version_fix =  models.CharField(max_length=20, null=True, blank=True, verbose_name='合入版本')
    version_close =  models.CharField(max_length=20, null=True, blank=True, verbose_name='关闭版本')
    current_owner =  models.CharField(max_length=100, null=True, blank=True, verbose_name='当前处理人')
    participator = models.CharField(max_length=100, null=True, blank=True, verbose_name='参与人')
    te = models.CharField(max_length=100, null=True, blank=True, verbose_name='测试人员')
    de = models.CharField(max_length=100, null=True, blank=True, verbose_name='开发人员')
    auditer = models.CharField(max_length=10, null=True, blank=True, verbose_name='审核人')
    confirmer = models.CharField(max_length=10, null=True, blank=True, verbose_name='验证人')
    lastmodify = models.CharField(max_length=20, null=True, blank=True, verbose_name='最后修改人')
    in_progress_time = models.DateTimeField(null=True, blank=True, verbose_name='接受处理时间')
    verify_time = models.DateTimeField(null=True, blank=True, verbose_name='验证时间')
    reject_time = models.DateTimeField(null=True, blank=True, verbose_name='拒绝时间')
    modified = models.DateTimeField(null=True, blank=True, verbose_name='最后修改时间')
    begin = models.DateField(null=True, blank=True, verbose_name='预计开始日期')
    due = models.DateField(null=True, blank=True, verbose_name='预计结束日期')
    deadline = models.DateField(null=True, blank=True, verbose_name='解决期限')
    os = models.CharField(max_length=10, null=True, blank=True, verbose_name='操作系统')
    platform = models.CharField(max_length=20, null=True, blank=True, verbose_name='软件平台')

    class Meta:
        db_table = 'tb_tpad_defect'
        verbose_name = 'tpad线上缺陷'
        verbose_name_plural = verbose_name







