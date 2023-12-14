# -*- coding: utf-8 -*-
# author: timor

from django.db import models
from common.models import BaseModel
from tools.filesize import convert_size
from tools.storage import PathAndRename
import os


class Upload(BaseModel):
    username = models.CharField('上传用户', max_length=20)
    file = models.FileField('上传文件', upload_to=PathAndRename("./"), blank=True)
    archive = models.CharField('文件归档', max_length=201, default=u'其他', null=True, blank=True)
    filename = models.CharField('文件名', max_length=201, null=True, blank=True)
    filepath = models.CharField('文件路径', max_length=201, null=True, blank=True)
    type = models.CharField('文件类型', max_length=100, null=True, blank=True)
    size = models.CharField('文件大小', max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        from re import sub
        self.size = '{}'.format(convert_size(self.file.size))
        filename = os.path.splitext(self.file.name)
        self.filename = '{}-{}{}'.format(sub('\W+', '', filename[0]), self.create_time, filename[1]).replace(' ', '_')
        self.filepath = '{}/{}'.format(self.archive, self.filename)
        super(Upload, self).save(*args, **kwargs)

    def __str__(self):
        return self.filepath

    class Meta:
        verbose_name = '文件上传'
        verbose_name_plural = verbose_name
        ordering = ['id']


class FileUpload(models.Model):
    file = models.FileField('上传文件', upload_to=("./tmp"), blank=True)

    class Meta:
        verbose_name = '文件上传'
        verbose_name_plural = verbose_name
        ordering = ['id']


class RequestEvent(BaseModel):
    uri = models.CharField('请求URI', max_length=255)
    method = models.CharField('请求方法', max_length=20)
    query_string = models.TextField('请求内容')
    user = models.CharField('用户', max_length=255, null=True)
    remote_ip = models.GenericIPAddressField('请求IP', max_length=50, null=True)

    class Meta:
        verbose_name = '请求事件'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class SimpleModel(models.Model):
    name = models.CharField('名称', max_length=255, unique=True)
