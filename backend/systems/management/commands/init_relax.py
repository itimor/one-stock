# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        topmenu = Menu.objects.get(name='top', code='top')
        self.stdout.write(self.style.SUCCESS('############ 初始化放松一下 ###########'))
        toolmenu = Menu.objects.create(name='放松一下', code='relax', curl='/relax', icon='relax', sequence=99, type=1,
                                       parent=topmenu)
        Menu.objects.create(name='王冰冰', code='bingbing', curl='/bingbing', icon='girl', sequence=10, type=2,
                            parent=toolmenu)

        self.stdout.write(self.style.SUCCESS('初始化完成'))
