#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from backend.models import Sprint
from backend.models import TestcaseSuite
from backend.models import SprintTestplan
from backend.models import ProjectVersion
from backend.serializers import SprintSerializer
from backend.serializers import TestcaseSuiteSerializer

import json
import logging


logger = logging.getLogger('mylogger')

class SprintListAPIView(APIView):
    '''
    产品管理-迭代管理-迭代列表
    '''
    # 查询列表数据
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            product_id = params.get('productId')
            page_size = int(params.get('pageSize'))
            page_no = int(params.get('pageNo'))
            name = params.get('name')
            version = params.get('version')
            sprint_status = params.get('status')
            sort = params.get('sort')
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            startIndex = (page_no - 1) * page_size
            endIndex = startIndex + page_size
            filters = {'is_delete':0, 'product_id':product_id}
            if name:
                filters['name__startswith'] = name
            if version:
                filters['version__startswith'] = version
            if sprint_status:
                filters['status'] = sprint_status
            rows = Sprint.objects.filter(**filters).order_by(*sort_list)[startIndex:endIndex]
            rows = SprintSerializer(rows, many=True).data
            total = Sprint.objects.filter(**filters).count()

            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = {}
            result['data']['rows'] = rows
            result['data']['total'] = total
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


    # 批量删除列表数据
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            row_ids = data.get('row_ids')
            if TestcaseSuite.objects.filter(sprint_id__in=row_ids, is_delete=0).exclude(parent_id=-1).exists():
                result['msg'] =  '删除失败，请先删除关联产品的测试套件'
                result['success'] =  True
                return Response(result, status.HTTP_200_OK)

            if SprintTestplan.objects.filter(sprint_id__in=row_ids, is_delete=0).exists():
                result['msg'] =  '删除失败，请先删除迭代关联的测试计划'
                result['success'] =  True
                return Response(result, status.HTTP_200_OK)

            with transaction.atomic():
                Sprint.objects.filter(id__in=row_ids).update(is_delete=1)

                # 逻辑删除同迭代关联的迭代测试套件
                TestcaseSuite.objects.filter(sprint_id__in=row_ids).update(is_delete=True)
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SprintAPIView(APIView):
    '''
    产品视图-迭代管理，新增，修改，删除迭代
    '''

    # 新增迭代
    def post(self, request, format=None):
        result = {}

        try:
            data = request.data
            sprint_name = data.get('name')
            product_id = data.get('product_id')
            data['creater_id'] = request.user.id
            data['updater_id'] = data['creater_id']
            data['creater_name'] = request.user.name
            data['updater_name'] = data['creater_name']
            data['is_delete'] = False

            if Sprint.objects.filter(product_id=product_id,name=sprint_name, is_delete=0).exists():
                result['msg'] =  '新增失败，迭代已存在'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            testcase_suite_data = {}
            testcase_suite_data['name'] = data.get('name')
            testcase_suite_data['type'] = 'sprint'
            testcase_suite_data['parent_id'] = -1
            testcase_suite_data['creater_id'] = data['creater_id']
            testcase_suite_data['updater_id'] = data['creater_id']
            testcase_suite_data['is_delete'] = False
            testcase_suite_data['all_upper_node_ids'] = '-1'

            try:
                with transaction.atomic():
                    serializer = SprintSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    sprint_id = serializer.data.get('id')

                    # 新增对应产品的迭代对应的迭代根测试套件
                    testcase_suite_data['sprint_id'] = sprint_id
                    testcase_suite_data['product_id'] = product_id

                    testcase_suite_serializer = TestcaseSuiteSerializer(data=testcase_suite_data)
                    testcase_suite_serializer.is_valid(raise_exception=True)
                    testcase_suite_serializer.save()
            except Exception as e:
                result['msg'] =  '新增失败：%s' % e
                result['success'] =  False
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

            result['msg'] =  '新增成功'
            result['success'] =  True
            result['data'] =  serializer.data
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


    # 修改迭代
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['updater_id'] = request.user.id
            data['updater_name'] = request.user.name
            product_id = data.get('product_id')
            sprint_name = data.get('name')
            sprint_id = data.get('id')

            if Sprint.objects.exclude(product_id=product_id, id=sprint_id).filter(name=sprint_name, is_delete=0).exists():
                result['msg'] =  '修改失败，迭代名称已存在'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)
            obj = Sprint.objects.filter(id=sprint_id).first()

            del data['id']
            del data['product_id']
            if obj:
                try:
                    testcase_suite_data = {}
                    testcase_suite_data['name'] = sprint_name
                    testcase_suite_data['type'] = 'sprint'
                    testcase_suite_data['parent_id'] = -1
                    testcase_suite_data['creater_id'] = data['updater_id']
                    testcase_suite_data['updater_id'] = data['updater_id']
                    testcase_suite_data['is_delete'] = False
                    testcase_suite_data['all_upper_node_ids'] = '-1'
                    with transaction.atomic():
                         # 修改、新增对应产品的迭代对应的迭代测试套件
                        testcase_suite_data['sprint_id'] = sprint_id
                        testcase_suite_data['product_id'] = product_id
                        test_suite = TestcaseSuite.objects.filter(product_id=product_id, sprint_id=sprint_id, parent_id=-1, all_upper_node_ids='-1').first()
                        if test_suite:
                            test_suite.is_delete = False
                            test_suite.name = sprint_name
                            test_suite.save()
                        else:
                            testcase_suite_serializer = TestcaseSuiteSerializer(data=testcase_suite_data)
                            testcase_suite_serializer.is_valid(raise_exception=True)
                            testcase_suite_serializer.save()

                        serializer = SprintSerializer(obj, data=data, partial=True)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                except Exception as e:
                    result['msg'] =  '修改失败：%s!' % e
                    result['success'] =  False
                    return Response(result, status.HTTP_400_BAD_REQUEST)
            else:
                result['msg'] = '修改失败,迭代不存在'
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

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


    # 删除迭代
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            sprint_id = data.get('id')

            if TestcaseSuite.objects.filter(sprint_id=sprint_id, is_delete=0).exclude(parent_id=-1).exists():
                result['msg'] =  '删除失败，请先删除迭代关联产品的测试套件'
                result['success'] =  True
                return Response(result, status.HTTP_200_OK)

            if SprintTestplan.objects.filter(sprint_id=sprint_id, is_delete=0).exists():
                result['msg'] =  '删除失败，请先删除迭代关联的测试计划'
                result['success'] =  True
                return Response(result, status.HTTP_200_OK)

            with transaction.atomic():
                Sprint.objects.filter(id=sprint_id).update(is_delete=True)

                # 逻辑删除同迭代关联的迭代测试套件
                TestcaseSuite.objects.filter(sprint_id=sprint_id, is_delete=0).update(is_delete=True)
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SprintTestplansAPIView(APIView):
    '''
    获取迭代关联的测试计划
    '''

    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            fields = params.get('fields')
            query_filters = params.get('filters')
            sort = params.get('sort')
            sprint_id = params.get('sprintId')
            if fields:
                fields = fields.split(',')
            else:
                fields = ['id', 'name']
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            filters = {'is_delete':0, 'sprint_id':sprint_id}
            if query_filters:
                query_filters = json.loads(query_filters)
                filters.update(query_filters)

            rows = SprintTestplan.objects.filter(**filters).order_by(*sort_list).values(*fields)
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = rows
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SprintProjectsVersionsAPIView(APIView):
    '''
      获取迭代关联的项目及项目版本
      '''

    def get(self, request, format=None):
        try:
            result = {}
            data = request.GET
            sprint_id = data.get('sprintId')
            sql =  'SELECT tb_project_version.id AS id, tb_project_version.name AS version_name, tb_project.id AS project_id, tb_project.name AS project_name ' \
                       'FROM tb_project_version JOIN tb_project ON tb_project_version.project_id=tb_project.id ' \
                       'WHERE tb_project_version.is_delete=0 ' \
                       'AND tb_project_version.sprint_id = %s ' \
                       'ORDER BY tb_project.id DESC, tb_project_version.id DESC ' % sprint_id

            query_rows = ProjectVersion.objects.raw(sql)
            project_dict = {}
            project_version_options = []
            for item in query_rows:
                item.__dict__.pop('_state')
                item = item.__dict__
                project_version_options.append({'id': item['id'], 'name': item['version_name'], 'project':{'id':item['project_id'], 'name':item['project_name']}})
                project_id = item.get('project_id')
                if project_id not in project_dict:
                    project_dict[project_id] = {'id': project_id, 'name': item['project_name'], 'versions':[{'id':item['id'], 'name': item['version_name']}]}
                else:
                    project_dict[project_id]['versions'].append({'id':item['id'], 'name': item['version_name']})
            project_options = [project_dict[item] for item in project_dict]

            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = {'projectVersionOptions':project_version_options, 'projectOptions':project_options }
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
