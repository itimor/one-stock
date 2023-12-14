# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = '创建普通账号'

    def add_arguments(self, parser):
        parser.add_argument('user', type=str)

    def handle(self, *args, **options):
        test_role = Role.objects.get(name='test', code='test')
        test_group = Group.objects.get(name='test', code='test')
        user = options['user']
        try:
            self.stdout.write(self.style.SUCCESS('############ 创建普通账号 ###########'))
            test_user = User.objects.create(username=user, password=make_password("123456"), group=test_group)
            test_user.roles.add(test_role)
            print(f'{user} 创建成功')
        except Exception as e:
            print(e)
            print(f'{user} 创建失败')

        self.stdout.write(self.style.SUCCESS('初始密码为 123456'))
