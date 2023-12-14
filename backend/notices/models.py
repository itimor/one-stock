# -*- coding: utf-8 -*-
# author: timor

from django.db import models
from common.models import BaseModel

notice_type = {
    'email': 'email',
    'ding': 'ding',
    'telegram': 'telegram',
}


class MessageTo(BaseModel):
    type = models.CharField(max_length=10, choices=tuple(notice_type.items()), default=0, verbose_name='通知类型')
    name = models.CharField('名称', max_length=20)
    to = models.CharField('接收者', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "消息接收者"
        verbose_name_plural = verbose_name
        ordering = ['id']


class EmailBot(BaseModel):
    name = models.CharField('名称', max_length=20, unique=True)
    host = models.CharField('主机', max_length=32)
    user = models.CharField('账号', max_length=32)
    password = models.CharField('密码', max_length=32)
    to = models.ForeignKey(MessageTo, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='接收者')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "email机器人"
        verbose_name_plural = verbose_name
        ordering = ['id']


class TelegramBot(BaseModel):
    name = models.CharField('名称', max_length=20, unique=True)
    uid = models.CharField('账号', max_length=32)
    token = models.CharField('token', max_length=32)
    chat_id = models.CharField('chat_id', max_length=32)
    to = models.ForeignKey(MessageTo, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='接收者')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "telegram机器人"
        verbose_name_plural = verbose_name
        ordering = ['id']
