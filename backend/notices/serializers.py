# -*- coding: utf-8 -*-
# author: timor

from notices.models import *
from rest_framework import serializers


class EmailBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailBot
        fields = '__all__'


class TelegramBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramBot
        fields = '__all__'


class MessageToSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTo
        fields = '__all__'
