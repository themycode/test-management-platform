#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = '赖富玉'

'''
自定义装饰器
'''

from django.db import close_old_connections

def close_old_database_connections(func):
    '''自定义decorator，用来装饰使用数据库操作函数'''
    def wrapper(*args, **kwargs):
        close_old_connections()
        return func(*args, **kwargs)

    return wrapper