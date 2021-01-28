#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import logging
from backend.tpad.tpadTool import TpadDefectTool
logger = logging.getLogger('mylogger')


'''
定时任务模块
'''


import socket

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 47500))
except socket.error:
    logger.warn( "scheduler already started")
else:
    from apscheduler.schedulers.background import BackgroundScheduler
    from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
    try:
        pass
        # # 实例化调度器
        # scheduler = BackgroundScheduler()
        # # 调度器使用DjangoJobStore()
        # scheduler.add_jobstore(DjangoJobStore(), "default")

        # 每天凌晨2点同步tapd缺陷
        # @register_job(scheduler, 'cron', day='*', hour='2', minute='0', second='0')
        # def sync_tpad_defects():
            # TpadDefectTool.sync_tpad_project_online_defects()
        # register_events(scheduler)
        # scheduler.start()
    except Exception as e:
        logger.error('开启后台定时任务失败：%s' % e)
        # 有错误就停止定时器
        # scheduler.shutdown()