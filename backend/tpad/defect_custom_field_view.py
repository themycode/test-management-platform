#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = '赖富玉'

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backend.tpad.tpadTool import TpadDefectTool

import logging
import json

logger = logging.getLogger('mylogger')


class DefectCustomFieldAPIView(APIView):
    '''

    '''


    # 获取缺陷自定义字段配置
    def get(self, request, format=None):
        result = {}
        try:
            data = request.GET
            # project_id = data.get('project_id')
            custom_field = data.get('customField')
            project_id = settings.TPAD_PROJECT_ID
            params = "workspace_id=%s"  % project_id
            request_result = TpadDefectTool.get_custom_fields_settings(params)
            if request_result[0]:
                response_body = request_result[1]
                response_body= json.loads(response_body)
                info = response_body.get('info')
                if info != 'success':
                    result['success'] = False
                    result['msg'] = '获取TPAD缺陷所属产品自定义字段配置失败：%s' % info
                    return Response(result, status.HTTP_200_OK)

                # 获取指定自定义字段产品配置
                data = response_body.get('data')
                result['data'] = []
                for item in data:
                    item = item['CustomFieldConfig']
                    if item.get('custom_field') == custom_field:
                        options = item.get('options')
                        field_type = item.get('type').lower()
                        if options and field_type == 'select':
                            options = options.split('|')
                            for i in range(1, len(options)+1):
                                temp_dict = {'id':i, 'name':options[i-1]}
                                result['data'].append(temp_dict)
                        else:
                            result['data'] = options
                        break
            else:
                result['success'] = False
                result['msg'] = '获取TPAD缺陷所属产品自定义字段配置失败：%s' % request_result[1]
                return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)

            result['msg'] =  '获取TPAD缺陷所属产品自定义字段配置成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


