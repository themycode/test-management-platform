#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import os
import shortuuid

import logging

from django.http import FileResponse
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.models import BaseTestcase
from backend.models import SprintTestcase
from backend.models import TestcaseAttachment
from backend.models import SprintTestplanTestcaseAttachment
from backend.serializers import TestcaseAttachmentSerializer
from backend.serializers import TestplanTestcaseAttachmentSerializer
from backend.utils import utils

logger = logging.getLogger('mylogger')

class TestcaseAttachmentListAPIView(APIView):
    '''
    测试视图-测试用例管理，测试用例附件列表
    '''

    def get(self, request, format=None):
        '''查询列表数据'''

        result = {}
        try:
            params =  request.GET
            case_guid = params.get('caseGuid')
            testplanId = params.get('testplanId')
            case_type = params.get('caseType').lower()
            sort = params.get('sort')
            if sort:
                sort_list = sort.split(',')
            else:
                sort_list = ['-create_time']

            filters = {'is_delete':0, 'case_guid':case_guid}

            try:
                if case_type != 'testplan':
                    attachments = TestcaseAttachment.objects.filter(**filters).order_by(*sort_list)
                else:
                    filters['testplan_id'] = testplanId
                    attachments = SprintTestplanTestcaseAttachment.objects.filter(**filters).order_by(*sort_list)

                if attachments:
                    attachments = TestcaseAttachmentSerializer(attachments, many=True).data
                else:
                    attachments = []
            except Exception as e:
                result['msg'] =  '获取失败：%s' % e
                result['success'] =  False
                result['data'] = []
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result['msg'] =  '获取成功'
            result['success'] =  True
            result['data']=attachments
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestcaseAttachmentAPIView(APIView):
    '''
    测试视图-测试用例管理，新增，删除测试用例附件
    '''

    # 同步生成附件
    @staticmethod
    def sync_create_attatchment(case_guid, time_str, suffix, data, file, type, direction=None):
        file_name = shortuuid.uuid() + time_str + suffix
        file_relative_path = '/testcase/attachments/'+ time_str
        file_absolute_path = settings.MEDIA_ROOT.rstrip('/') + file_relative_path
        file_relative_path += '/' + file_name
        data['file_path'] = file_relative_path

        file_absolute_path = file_absolute_path + '/' + file_name
        file_handler = open(file_absolute_path, 'wb')    # 打开特定的文件进行二进制的写操作
        try:
            for chunk in file.chunks():      # 分块写入文件
                file_handler.write(chunk)
        finally:
            file_handler.close()

        try:
            # 记录到数据库
            if type == 'sprint':
                obj = SprintTestcase.objects.filter(guid=case_guid).first()
                if obj:
                    data['case_guid'] = obj.guid
                    serializer = TestcaseAttachmentSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    # 同步生成基线用例的附件
                    guid_for_created = shortuuid.uuid()
                    data['guid'] = guid_for_created
                    data['attachment_guid'] = serializer.data.get('guid')
                    TestcaseAttachmentAPIView.sync_create_attatchment(case_guid, time_str, suffix, data, file, 'base')

            elif type == 'base':
                if direction == 'testplan_to_base':
                    obj = BaseTestcase.objects.filter(guid=case_guid).first()
                else:
                    obj = BaseTestcase.objects.filter(sprint_testcase_guid=case_guid).first()
                if obj:
                    data['sprint_case_guid'] = case_guid
                    data['case_guid'] = obj.guid
                    serializer = TestcaseAttachmentSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
        except Exception as e:
            raise  Exception('%s' % e)

    @staticmethod
    def delete_attachment(attachment):
        # 删除附件
        file_absoulte_path = settings.MEDIA_ROOT.rstrip('/') + attachment.file_path # attachment.file_path 都以 / 打头
        if os.path.exists(file_absoulte_path) and os.path.isfile(file_absoulte_path):
            os.remove(file_absoulte_path)
        attachment.delete()


    # 上传附件
    def post(self, request, format=None):
        result = {}
        try:
            files = request.FILES
            file = files.get('file')

            if not file:
                result['msg'] =  '上传失败，未获取到文件'
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            data = request.POST
            guid = shortuuid.uuid()
            data['guid'] = guid
            case_guid = data.get('case_guid')
            case_type = data.get('case_type').lower()
            detail_case_type = data.get('detail_case_type')
            file_name = file.name
            data['name'] = file_name
            data['creater_id'] = request.user.id
            data['is_delete'] = False
            create_time = timezone.now()
            data['create_time'] = create_time

            time_str = create_time.strftime('%Y%m%d')
            name, suffix = os.path.splitext(file_name)
            file_name = shortuuid.uuid() + time_str + suffix
            file_relative_path = '/testcase/attachments/'+ time_str
            file_absolute_path = settings.MEDIA_ROOT.rstrip('/') + file_relative_path
            if not os.path.exists(file_absolute_path):# 路径不存在
                if not utils.mkdirs_in_batch(file_absolute_path):
                    result['msg'] =  '批量创建路径(%s)对应的目录失败' % file_absolute_path
                    result['success'] =  False
                    return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
            file_relative_path += '/' + file_name
            data['file_path'] = file_relative_path

            file_absolute_path = file_absolute_path + '/' + file_name
            file_handler = open(file_absolute_path, 'wb')    # 打开特定的文件进行二进制的写操作

            try:
                for chunk in file.chunks():      # 分块写入文件
                    file_handler.write(chunk)
            finally:
                file_handler.close()
            # 记录到数据库
            try:
                if case_type != 'testplan':
                    serializer = TestcaseAttachmentSerializer(data=data)
                else:
                    serializer = TestplanTestcaseAttachmentSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                result_data = serializer.data
            except Exception as e:
                result['msg'] =  '上传失败：%s' % e
                result['success'] =  False
                return Response(result, status.HTTP_400_BAD_REQUEST)

            guid_for_created = shortuuid.uuid()
            data['guid'] = guid_for_created
            if case_type == 'sprint':
                data['attachment_guid'] = guid
                TestcaseAttachmentAPIView.sync_create_attatchment(case_guid, time_str, suffix, data, file, 'base')
            elif case_type == 'testplan':
                serializer.instance.attachment_guid = guid_for_created
                serializer.instance.save()

                if detail_case_type == 'sprint':
                    # 同步为关联的迭代用例上传附件
                    TestcaseAttachmentAPIView.sync_create_attatchment(case_guid, time_str, suffix, data, file, detail_case_type)
                elif detail_case_type == 'base':
                    # 同步为关联的基线用例上传附件
                    TestcaseAttachmentAPIView.sync_create_attatchment(case_guid, time_str, suffix, data, file, detail_case_type, 'testplan_to_base')
                else:
                    # 细分类型不存在
                    pass

            result['msg'] =  '上传成功'
            result['success'] =  True
            result['data'] =  result_data
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 删除附件
    def delete(self, request, format=None):
        result = {}
        try:
            data = request.data
            attachment_id = data.get('attachment_id')
            guid = data.get('guid') # 附件自身的guid
            case_type = data.get('case_type').lower()
            case_guid = data.get('case_guid')
            if case_type != 'testplan':
                obj = TestcaseAttachment.objects.filter(id=attachment_id).first()
            else:
                obj = SprintTestplanTestcaseAttachment.objects.filter(id=attachment_id).first()
            with transaction.atomic():
                if obj:
                    obj_attachment_guid = obj.attachment_guid
                    TestcaseAttachmentAPIView.delete_attachment(obj)

                if case_type == 'sprint':
                    attachment = TestcaseAttachment.objects.filter(attachment_guid=guid).first()
                    # 同步删除基线对应附件
                    if attachment:
                        TestcaseAttachmentAPIView.delete_attachment(attachment)
                elif case_type == 'testplan':
                    # 同步删除关联测试用例的对应附件
                    attachment = TestcaseAttachment.objects.filter(guid=obj_attachment_guid).first()
                    if attachment:
                        TestcaseAttachmentAPIView.delete_attachment(attachment)

                        # 同步删除以上被删除附件所关联的测试用例附件
                        attachment = TestcaseAttachment.objects.filter(attachment_guid=obj_attachment_guid).first()
                        if attachment:
                            TestcaseAttachmentAPIView.delete_attachment(attachment)

            result['msg'] =  '删除成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 下载附件
    def get(self, request, format=None):
        result = {}
        try:
            data = request.GET
            attachment_id = data.get('attachmentId')
            obj = TestcaseAttachment.objects.filter(id=attachment_id).first()
            if obj:
                file_absoulte_path = settings.MEDIA_ROOT.rstrip('/') +  obj.file_path # obj.file_path都以 / 打头
                if os.path.exists(file_absoulte_path) and os.path.isfile(file_absoulte_path):
                    file = open(file_absoulte_path, 'rb')
                    file_response = FileResponse(file)
                    file_response['Content-Type']='application/octet-stream'
                    file_response['Content-Disposition']='attachment;filename={}'.format(obj.name) # 不知道为啥，前端获取不到请求头Content-Disposition
                    return file_response
                else:
                    result['msg'] =  '请求失败,资源不存在'
                    result['success'] =  False
            else:
                result['msg'] =  '请求失败,资源不存在'
                result['success'] =  False
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)



