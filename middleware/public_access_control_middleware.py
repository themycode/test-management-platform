#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'


from django.utils.deprecation import MiddlewareMixin

from backend.views import LogoutView

class PublicAccessControlMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass

    def process_response(self, request, response):
        response['Access-Control-Max-Age'] = 86400

        if response.status_code == 401:
            if hasattr(response, 'status_text'):
                if response.status_text == 'Unauthorized':
                    # detail = str(response.data.get('detail'))
                    # if detail in ['TokenExpired', 'InvalidToken', 'TokenUserDisabledOrDeleted']:
                    #     LogoutView.logout_user(request)
                    LogoutView.logout_user(request)
        return response


