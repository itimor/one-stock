# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        topmenu = Menu.objects.get(name='top', code='top')
        self.stdout.write(self.style.SUCCESS('############ 初始化通知菜单 ###########'))
        noticemenu = Menu.objects.create(name='通知管理', code='notice', curl='/notice', icon='notice', sequence=3,
                                         type=1, parent=topmenu)
        Menu.objects.create(name='配置email', code='email', curl='/email', icon='email', sequence=10, type=2,
                            parent=noticemenu)
        Menu.objects.create(name='配置telegram', code='telegram', curl='/telegram', icon='telegram', sequence=30,
                            type=2, parent=noticemenu)
        Menu.objects.create(name='配置接收人', code='to', curl='/to', icon='to', sequence=40, type=2,
                            parent=noticemenu)

        self.stdout.write(self.style.SUCCESS('初始化完成'))
