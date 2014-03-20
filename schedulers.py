#coding=utf-8
'''任务调度models'''
from datetime import datetime
from mongoengine import (Document, IntField, StringField, DateTimeField,
                         connect, ListField, BooleanField)

from conf import HOST, PORT, DATABASE

connect(DATABASE, host=HOST, port=PORT)


class Task(Document):
    type = StringField(max_length=60, required=True) # 任务类型
    last_run_at = DateTimeField(default=datetime.now(), required=True) # 上一次任务的执行时间
    interval = IntField(default=3600, required=True) # 任务间隔,单位秒


class Message(Document):
    '''MQ存放在mongodb中的格式'''
    task = StringField(max_length=60, required=True) # 任务类型
    payload = ListField(StringField(max_length=20), unique=True) # 函数执行的参数
    state = IntField(default=0, required=True) # 任务状态, 0 未执行, 1 运行中, 2 已完成, 3 失败
    error = StringField(default='', required=True) # 失败日志
    inprocess = BooleanField(default=False, required=True) # 是否在处理中

    meta = {
        'indexes': [('state', 'task', 'inprocess'), ('payload')],
    }
