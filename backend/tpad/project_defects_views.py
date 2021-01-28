#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = '赖富玉'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.tpad.tpadTool import TpadDefectTool

import logging

logger = logging.getLogger('mylogger')

class TapdProjectOnlineDefectsAPIView(APIView):
    '''
    批量获取tpad 线上问题
    '''


    def get(self, request, format=None):
        result = {}

        try:
            TpadDefectTool.sync_tpad_project_online_defects()
            result['msg'] =  '同步TPAD缺陷成功'
            result['success'] =  True
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result['msg'] =  '%s' % e
            result['success'] =  False
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)





