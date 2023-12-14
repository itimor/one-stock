# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        topmenu = Menu.objects.get(name='top', code='top')
        self.stdout.write(self.style.SUCCESS('############ 初始化股票菜单 ###########'))
        stockmenu = Menu.objects.create(name='股票管理', code='stock', curl='/stock', icon='stock', sequence=4,
                                        type=1, parent=topmenu)
        Menu.objects.create(name='股票列表', code='stocks', curl='/stocks', icon='stocks', sequence=1, type=2,
                            parent=stockmenu)
        Menu.objects.create(name='股票行情', code='stockdaily', curl='/stockdaily', icon='list', sequence=2, type=2,
                            parent=stockmenu)
        Menu.objects.create(name='股票异动', code='stockchange', curl='/stockdaily', icon='stockdaily', sequence=3, type=2,
                            parent=stockmenu)
        Menu.objects.create(name='股票筛选', code='stockchangefilter', curl='/stockchangefilter', icon='stockchangefilter', sequence=4, type=2,
                            parent=stockmenu)
        self.stdout.write(self.style.SUCCESS('初始化完成'))
