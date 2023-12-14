# -*- coding: utf-8 -*-
# author: timor

from stocks.models import *
from rest_framework import serializers


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class StockDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockDaily
        fields = '__all__'


class StockChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockChange
        fields = '__all__'
