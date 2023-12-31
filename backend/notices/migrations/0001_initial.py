# Generated by Django 3.2.9 on 2021-12-02 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MessageTo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
                ('type', models.CharField(choices=[('email', 'email'), ('ding', 'ding'), ('telegram', 'telegram')], default=0, max_length=10, verbose_name='通知类型')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('to', models.CharField(max_length=20, verbose_name='接收者')),
            ],
            options={
                'verbose_name': '消息接收者',
                'verbose_name_plural': '消息接收者',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TelegramBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='名称')),
                ('uid', models.CharField(max_length=32, verbose_name='账号')),
                ('token', models.CharField(max_length=32, verbose_name='token')),
                ('chat_id', models.CharField(max_length=32, verbose_name='chat_id')),
                ('to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='notices.messageto', verbose_name='接收者')),
            ],
            options={
                'verbose_name': 'telegram机器人',
                'verbose_name_plural': 'telegram机器人',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='EmailBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='名称')),
                ('host', models.CharField(max_length=32, verbose_name='主机')),
                ('user', models.CharField(max_length=32, verbose_name='账号')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='notices.messageto', verbose_name='接收者')),
            ],
            options={
                'verbose_name': 'email机器人',
                'verbose_name_plural': 'email机器人',
                'ordering': ['id'],
            },
        ),
    ]
