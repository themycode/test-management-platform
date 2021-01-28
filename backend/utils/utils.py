#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = '赖富玉'

import os
import pdfkit
import logging

from django.conf import settings

logger = logging.getLogger('mylogger')

# 批量创建目录
def mkdirs_in_batch(path):
    try:
        path = os.path.normpath(path)  # 去掉路径最右侧的 \\ 、/
        path = path.replace('\\', '/') # 将所有的\\转为/，避免出现转义字符串
        head, tail = os.path.split(path)
        if not os.path.isdir(path) and os.path.isfile(path):  # 如果path指向的是文件，则分解文件所在目录
            head, tail = os.path.split(head)

        if tail == '': # head为根目录，形如 / 、D:
            return True

        new_dir_path = ''  # 存放反转后的目录路径
        root = ''  # 存放根目录
        while tail:
            new_dir_path = new_dir_path + tail + '/'
            head, tail = os.path.split(head)
            root = head
        else:
            new_dir_path = root + new_dir_path

            # 批量创建目录
            new_dir_path = os.path.normpath(new_dir_path)
            head, tail = os.path.split(new_dir_path)
            temp = ''
            while tail:
                temp = temp + '/' + tail
                dir_path = root + temp
                if not os.path.isdir(dir_path):
                    os.mkdir(dir_path)
                head, tail = os.path.split(head)
        return True
    except Exception as e:
        logger.error('批量创建目录出错：%s' % e)
        return False


def string_hump_to_underline(src_string):
    '''
     字符串 驼峰式转下划线分割式
     例子：MyExamp -> my_examp
    '''

    for char in src_string[0:]:
        if ord(char) != ord(char.lower()): # 大写字母
            src_string = src_string.replace(char, '_' + char.lower())

    src_string = src_string.lstrip('_')
    return src_string


def html_str_to_pdf_file(html_str, file_name):
    '''由html字符串生成pdf'''

    try:
        config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF)
        file_dir = settings.MEDIA_ROOT.rstrip('/') + '/sprint/testreport'
        if not os.path.exists(file_dir):# 路径不存在
            if not mkdirs_in_batch(file_dir):
                return [False,'生成报告失败：批量创建路径(%s)对应的目录失败' % file_dir]

        options = {'dpi': 300, 'image-dpi':600,  'page-size':'A3',  'encoding':'UTF-8', 'page-width':'1903px'}
        pdfkit.from_string(html_str, '%s/%s' % (file_dir, file_name), configuration=config, options=options)
        file_absolute_path =  '%s/%s' % (file_dir, file_name)
        return [True, file_absolute_path]
    except Exception as e:
        msg = '生成迭代测试报告出错：%s' % e
        logger.error(msg)
        return [False, msg]
