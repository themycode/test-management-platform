#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = '赖富玉'


import urllib.request
import json
import platform
import logging

python_version = platform.python_version()
if python_version < '3.5':
    from html.parser import HTMLParser
else:
    from html import unescape

logger = logging.getLogger('mylogger')

class HttpRequest:
    '''http请求动作类'''

    @staticmethod
    def urlencode_request(method, url, input_params, http, parse_type='urlencode', safe='&=', charset='utf-8'): # 针对请求体为url编码的：b'id=1318&password=e10adc3949ba59abbe56e057f20f883e'
        '''parse_type：解析方式，支持 urlencode, quote, quote_plus'''
        try:
            if parse_type == 'urlencode':
                logger.info('编码方式为：%s' % parse_type)
                if type(input_params) == type({'key':'value'}): # 如果参数为字典
                    input_params = urllib.parse.urlencode(input_params)
                else:
                    return [False, '解析方式采用urlencode,但是参数不是json格式']
            elif parse_type in ['quote', 'quote_plus']:
                if type(input_params) == type({'key':'value'}):
                    # 只解析第一层键值
                    temp_input_params = ''
                    for key, value in input_params.items():
                        temp_input_params += "&%s=%s" % (key, value)
                    temp_input_params = temp_input_params[1:] # 去掉最左侧的 &
                    input_params = temp_input_params
                if safe == None and parse_type == 'quote': # 不指定安全字符
                    logger.info('编码方式为：%s' % parse_type)
                    input_params = urllib.parse.quote(input_params)
                elif safe == None and parse_type == 'quote_plus':
                    logger.info('编码方式为：%s' % parse_type)
                    input_params = urllib.parse.quote_plus(input_params, safe=safe)
                elif safe and parse_type == 'quote': # 指定安全字符
                    logger.info( '编码方式为：%s，编码解析安全字符串为：%s' % (parse_type, safe))
                    input_params = urllib.parse.quote(input_params, safe=safe)
                elif safe and parse_type == 'quote_plus':
                    logger.info( '编码方式为：%s，编码解析安全字符串为：%s' % (parse_type, safe))
                    input_params = urllib.parse.quote_plus(input_params, safe=safe)
            else:
                return [False, '不支持的编码方式：%s' % parse_type]
        except Exception as e:
            msg = '%s' % e
            logger.error(msg)

        if method == 'post':
            msg = '正在发起POST请求...'
            logger.info(msg)
            input_params = input_params.encode('utf-8')
            response = http.post(url, input_params)
        elif method == 'get':
            msg = '正在发起GET请求...'
            logger.info(msg)
            response = http.get(url, input_params)

        if response[0]:
            encoding = None
            header = response[2]
            body = response[1]
            for item in header:
                if 'Content-Type' in item:
                    content_type = item[1]
                    index = content_type.find('charset=')
                    if index != -1:
                        encoding = content_type[index + len('charset='):]
                    break
            if not encoding:
                logger.info('未检测到服务器返回body编码, 使用函数参数指定编码%s对body进行解码' % charset)
                encoding = charset
            else:
                logger.info('检测到服务器返回内容编码为：%s, 正在对服务器返回body进行解码' % encoding)
            if encoding:
                encoding = encoding.lower()
                if  encoding in ('gb2312', 'windows-1252',  'iso-8859-1'):
                    body = response[1].decode('gbk')  # decode函数对获取的字节数据进行解码
                elif encoding in ('utf-8', 'utf-8-sig', 'iso-8859-2'):
                    body = response[1].decode('utf-8')
                elif encoding == 'ascii':
                    logger.info(json.loads(response[1].decode('utf-8')))
                    body = response[1].decode('ascii')

            if python_version < '3.5':
                 parser = HTMLParser()
                 body = parser.unescape(body) # 处理html实体
            else:
                 body = unescape(body)

            code = response[3]
            msg = '服务器返回结果"响应体(body)": %s' % body
            logger.info(msg)
            msg = '服务器返回结果"请求头(headers)": %s' % header
            logger.info(msg)
            msg = '服务器返回结果"状态码(code)": %s' % code
            logger.info(msg)
            return [True, body, header, code]
        else:
            reason = response[1]
            logger.error('请求结果失败：%s' % reason)
            return [False, reason]

    @staticmethod
    def json_request(method, url, input_params, http, charset='utf-8'):  # 针对请求体为json格式的（类型：字符串）
        method = method.lower()
        if method == 'post':
            logger.info('正在发起POST请求...')
            input_params = input_params.encode('utf-8')
            response = http.post(url, input_params)
        elif method == 'get':
            msg = '正在发起GET请求...'
            logger.info(msg)
            input_params = json.loads(input_params)
            input_params = urllib.parse.urlencode(input_params)
            response = http.get(url, input_params)

        if response[0]:
            encoding = None
            header = response[2]
            body = response[1]
            for item in header:
                if 'Content-Type' in item:
                    content_type = item[1]
                    index = content_type.find('charset=')
                    if index != -1:
                        encoding = content_type[index + len('charset='):]
                    break
            if not encoding:
                logger.info('未检测到服务器返回body编码, 使用函数参数指定编码%s对body进行解码' % charset)
                encoding = charset
            else:
                logger.info('检测到服务器返回内容编码为：%s, 正在对服务器返回body进行解码' % encoding)
            if encoding:
                encoding = encoding.lower()
                if  encoding in ('gb2312', 'windows-1252',  'iso-8859-1'):
                    body = response[1].decode('gbk')  # decode函数对获取的字节数据进行解码
                elif encoding in ('utf-8', 'utf-8-sig', 'iso-8859-2'):
                    body = response[1].decode('utf-8')
                elif encoding == 'ascii':
                    logger.info(json.loads(response[1].decode('utf-8')))
                    body = response[1].decode('ascii')

            if python_version < '3.5':
                 parser = HTMLParser()
                 body = parser.unescape(body) # 处理html实体
            else:
                 body = unescape(body)

            code = response[3]
            msg = '服务器返回结果"响应体(body)": %s' % body
            logger.info(msg)
            msg = '服务器返回结果"请求头(headers)": %s' % header
            logger.info(msg)
            msg = '服务器返回结果"状态码(code)": %s' % code
            logger.info(msg)
            return [True, body, header, code]
        else:
            reason = response[1]
            logger.error('请求结果失败：%s' % reason)
            return [False, reason]

    @staticmethod
    def xml_request(method, url, input_params, http, charset='utf-8'): # 针对请求体为webservice xml格式的
        method = method.lower()
        if method == 'post':
            msg = '正在发起POST请求...'
            logger.info(msg)
            input_params = input_params.encode('utf-8')
            response = http.post(url, input_params)
        elif method == 'get':
            msg = '正在发起GET请求...'
            logger.info(msg)
            input_params = urllib.parse.urlencode(input_params)
            response = http.get(url, input_params)

        if response[0]:
            encoding = None
            header = response[2]
            body = response[1]
            for item in header:
                if 'Content-Type' in item:
                    content_type = item[1]
                    index = content_type.find('charset=')
                    if index != -1:
                        encoding = content_type[index + len('charset='):]
                    break
            if not encoding:
                logger.info('未检测到服务器返回body编码, 使用函数参数指定编码%s对body进行解码' % charset)
                encoding = charset
            else:
                logger.info('检测到服务器返回内容编码为：%s, 正在对服务器返回body进行解码' % encoding)
            if encoding:
                encoding = encoding.lower()
                if  encoding in ('gb2312', 'windows-1252',  'iso-8859-1'):
                    body = response[1].decode('gbk')  # decode函数对获取的字节数据进行解码
                elif encoding in ('utf-8', 'utf-8-sig', 'iso-8859-2'):
                    body = response[1].decode('utf-8')
                elif encoding == 'ascii':
                    logger.info(json.loads(response[1].decode('utf-8')))
                    body = response[1].decode('ascii')

            if python_version < '3.5':
                 parser = HTMLParser()
                 body = parser.unescape(body) # 处理html实体
            else:
                 body = unescape(body)

            code = response[2]
            msg = '服务器返回结果"响应体(body)": %s' % body
            logger.info(msg)
            msg = '服务器返回结果"请求头(headers)": %s' % header
            logger.info(msg)
            msg = '服务器返回结果"状态码(code)": %s' % code
            logger.info(msg)
            return [True, body, header, code]
        else:
            reason = response[1]
            logger.error('请求结果失败：%s' % reason)
            return [False, reason]

