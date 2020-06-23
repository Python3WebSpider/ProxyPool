#!/usr/bin/env python
#coding:utf-8

from kombu import Queue
from celery.schedules import crontab
from datetime import timedelta

DEFAULT_QUEUE = "proxypool"
CELERY_DEFAULT_QUEUE = DEFAULT_QUEUE
# 定义一个默认队列和默认测试队列
CELERY_QUEUES = (
    Queue(DEFAULT_QUEUE,    routing_key='%s.#' % DEFAULT_QUEUE),
    Queue('%s_test' % DEFAULT_QUEUE, routing_key='%s_test.#' % DEFAULT_QUEUE),
)
CELERY_DEFAULT_EXCHANGE = 'tasks'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = '%s.default' % DEFAULT_QUEUE

# 启动多个消费者
# celery_worker_concurrency = 4
celery_worker_max_tasks_per_child = 40

BROKER_URL = 'amqp://admin:admin@localhost/' # 使用RabbitMQ作为消息代理

CELERY_RESULT_BACKEND = "redis://@localhost:6379/1" # 把任务结果存在了Redis

CELERY_TASK_SERIALIZER = 'json' # 任务序列化和反序列化使用msgpack方案

CELERY_RESULT_SERIALIZER = 'json' # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显

CELERY_ACCEPT_CONTENT = ['json', 'msgpack'] # 指定接受的内容类型

CELERYBEAT_SCHEDULE = {
    # Executes every 100 seconds
    'run-getter-every-10-miniute': {
        'task': 'tasks.celery_scheduler.run_getter',
        'schedule': timedelta(seconds=10*60),
        'args': (),
    },
    'run-tester-every-2-miniute': {
        'task': 'tasks.celery_scheduler.run_tester',
        'schedule': timedelta(seconds=2*60),
        'args': (),
    }
}