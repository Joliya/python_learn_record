# -*- encoding: utf-8 -*-
"""
文件注释
"""

from __future__ import absolute_import, unicode_literals


# celery启动文件
from celery import Celery

# 为celery使用django配置文件进行设置
import os

# 创建celery实例
celery_app = Celery('celery_tasks')
celery_app.config_from_object('celery_tasks.config')
celery_app.autodiscover_tasks(['celery_tasks.demo'])
