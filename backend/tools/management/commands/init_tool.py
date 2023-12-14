# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        topmenu = Menu.objects.get(name='top', code='top')
        self.stdout.write(self.style.SUCCESS('############ 初始化工具菜单 ###########'))
        toolmenu = Menu.objects.create(name='工具管理', code='tool', curl='/tool', icon='tool', sequence=2, type=1,
                                       parent=topmenu)
        Menu.objects.create(name='审计日志', code='audit', curl='/audit', icon='audit', sequence=10, type=2,
                            parent=toolmenu)
        Menu.objects.create(name='测试页面', code='test', curl='/test', icon='list', sequence=20, type=2,
                            parent=toolmenu)

        self.stdout.write(self.style.SUCCESS('初始化完成'))
