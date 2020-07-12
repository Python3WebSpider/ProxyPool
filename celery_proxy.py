#!/usr/bin/env python
# coding:utf-8
from __future__ import absolute_import
from celery import Celery

# include添加模块名称 project.file
app = Celery("proxypool", include=["tasks.celery_scheduler"])
app.config_from_object("celery_config")

if __name__ == '__main__':
    app.start()
