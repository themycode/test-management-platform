#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from backend.models import Product
from backend.models import Sprint
from backend.models import Project
from backend.serializers import ProductSerializer
from backend.serializers import TestcaseSuite
from backend.serializers import TestcaseSuiteSerializer

import json
import logging


logger = logging.getLogger('mylogger')

class ProductListAPIView(APIView):
    '''
    产品视图-产品管理
    '''

    # 查询列表数据
    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            page_size = int(params.get('pageSize'))
            page_no = int(params.get('pageNo'))
            name = params.get('name')
            product_status = params.get('status')
            product_owner = params.get('productOwner')
            sort = params.get('sort')
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            startIndex = (page_no - 1) * page_size
            endIndex = startIndex + page_size
            filters = {'is_delete':0}
            if name:
                filters['name__startswith'] = name
            if product_status:
                filters['status'] = product_status
            if product_owner:
                filters['product_owner__startswith'] = product_owner
            rows = Product.objects.filter(**filters).order_by(*sort_list)[startIndex:endIndex]
            rows = ProductSerializer(rows, many=True).data
            total = Product.objects.filter(**filters).count()

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

            temp_product_id_list = []
            testsuites = TestcaseSuite.objects.filter(product_id__in=row_ids, is_delete=0).exclude(parent_id=-1)
            if testsuites.exists():
                temp_product_id_list = list(testsuites.values_list('product_id',flat=True))

            if temp_product_id_list:
                result['msg'] =  '删除失败,请先删除产品(id：%s)关联的测试套件' % str(temp_product_id_list)
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            with transaction.atomic():
                Product.objects.filter(id__in=row_ids).update(is_delete=1)
                TestcaseSuite.objects.filter(product_id__in=row_ids, is_delete=0).update(is_delete=1)
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '删除失败：%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductAPIView(APIView):
    '''
    产品视图-产品管理，新增，修改，删除产品
    '''

    # 新增产品
    def post(self, request, format=None):
        result = {}

        try:
            data = request.data
            product_name = data.get('name').strip()
            code = data.get('code').strip()
            if not code:
                code = product_name
            data['code'] = code
            data['name'] = product_name
            data['creater_id'] = request.user.id
            data['updater_id'] = data['creater_id']
            data['creater_name'] = request.user.name
            data['updater_name'] = data['creater_name']
            data['is_delete'] = False

            testcase_suite_data = {}
            testcase_suite_data['name'] = data.get('name')
            testcase_suite_data['type'] = 'base'
            testcase_suite_data['sprint_id'] = -1
            testcase_suite_data['parent_id'] = -1
            testcase_suite_data['creater_id'] = data['creater_id']
            testcase_suite_data['updater_id'] = data['creater_id']
            testcase_suite_data['is_delete'] = False
            testcase_suite_data['all_upper_node_ids'] = '-1'

            if Product.objects.filter(name=product_name, is_delete=0).exists():
                result['msg'] =  '新增失败，产品名称已存在'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            if Product.objects.filter(code=code, is_delete=0).exists():
                result['msg'] =  '新增失败，产品编码已存在'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            try:
                with transaction.atomic():
                    serializer = ProductSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    # 新增产品对应的 基线根 测试套件
                    testcase_suite_data['product_id'] = serializer.data.get('id')
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

    # 修改产品
    def patch(self, request, format=None):
        result = {}
        try:
            data = request.data
            data['updater_id'] = request.user.id
            data['updater_name'] = request.user.name
            product_name = data.get('name').strip()
            data['name'] =  product_name
            code = data.get('code').strip()
            data['code'] = code
            if not code:
                code = product_name
            product_id = data.get('id')

            if Product.objects.exclude(id=product_id).filter(name=product_name, is_delete=0).exists():
                result['msg'] =  '修改失败，产品名称已存在'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            if Product.objects.exclude(id=product_id).filter(code=code, is_delete=0).exists():
                result['msg'] =  '修改失败，产品编号已存在'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            obj = Product.objects.filter(id=product_id).first()

            del data['id']
            if obj:
                try:
                    with transaction.atomic():
                        serializer = ProductSerializer(obj, data=data, partial=True)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()

                        # 同步更新对应产品的基线套件名称
                        TestcaseSuite.objects.filter(product_id=serializer.data.get('id'), parent_id=-1, sprint_id=-1, all_upper_node_ids='-1').update(name=product_name)
                except Exception as e:
                    result['msg'] =  '修改失败：%s!' % e
                    result['success'] =  False
                    return Response(result, status.HTTP_400_BAD_REQUEST)
            else:
                result['msg'] = '修改失败,产品不存在'
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

    # 删除产品
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            product_id = data.get('productId')

            if TestcaseSuite.objects.filter(product_id=product_id, is_delete=0).exclude(parent_id=-1).exists():
                result['msg'] =  '删除失败，请先删除该产品关联的测试套件'
                result['success'] =  False
                return Response(result, status.HTTP_200_OK)

            with transaction.atomic():
                obj = Product.objects.filter(id=product_id).first()
                if obj:
                    obj.is_delete = 1
                    obj.save()
                    # 删除关联的测试套件
                    TestcaseSuite.objects.filter(product_id=product_id, is_delete=0).update(is_delete=1)
            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductsDetailsAPIView(APIView):
    '''
    按指定字段批量获取产品信息，不提供字段则默认查询 id,name
    '''

    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            fields = params.get('fields')
            sort = params.get('sort')
            exclusive_filters = params.get('exclusion')
            if fields:
                fields = fields.split(',')
            else:
                fields = ['id', 'name']
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            filters = {'is_delete':0}
            if exclusive_filters:
                exclusive_filters = json.loads(exclusive_filters)
                rows = Product.objects.filter(**filters).exclude(**exclusive_filters).order_by(*sort_list).values(*fields)
            else:
                rows = Product.objects.filter(**filters).order_by(*sort_list).values(*fields)
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = rows
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProductProjectsDetailsAPIView(APIView):
    '''按指定字段获取某个产品关联的项目信息'''

    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            product_id = params.get('productId')
            # 获取产品关联的项目
            fields = params.get('fields')
            sort = params.get('sort')
            if fields:
                fields = fields.split(',')
            else:
                fields = ['id', 'name']

            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            filters = {'is_delete':0, 'product_id': product_id}
            projects = Project.objects.filter(**filters).order_by(*sort_list).values(*fields)

            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = projects
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            logger.error('%s' % e)
            result['msg'] =  '获取产品关联的项目信息出错：%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductSprintsDetailsAPIView(APIView):
    '''按指定字段获取某个产品关联的迭代信息'''

    def get(self, request, format=None):
        result = {}
        try:
            params =  request.GET
            product_id = params.get('productId')
            fields = params.get('fields')
            sort = params.get('sort')
            exclusive_filters = params.get('exclusion')
            if fields:
                fields = fields.split(',')
            else:
                fields = ['id', 'name']
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-id']

            filters = {'is_delete':0, 'product_id': product_id}
            if exclusive_filters:
                exclusive_filters = json.loads(exclusive_filters)
                rows = Sprint.objects.filter(**filters).exclude(**exclusive_filters).order_by(*sort_list).values(*fields)
            else:
                rows = Sprint.objects.filter(**filters).order_by(*sort_list).values(*fields)
            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data'] = rows
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            logger.error('%s' % e)
            result['msg'] =  '获取产品关联的迭代信息出错：%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



