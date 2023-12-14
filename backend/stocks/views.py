# -*- coding: utf-8 -*-
# author: timor

from stocks.serializers import *
from common.views import ModelViewSet, JsonResponse
from common import status
from rest_framework.decorators import action
from collections import Counter, OrderedDict
from datetime import datetime, timedelta


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    search_fields = ['code', 'name', 'industry']
    filter_fields = ['code', 'name']
    ordering_fields = ['code']


class StockChangeViewSet(ModelViewSet):
    queryset = StockChange.objects.all()
    serializer_class = StockChangeSerializer
    search_fields = ['code', 'name', 'industry']
    filter_fields = ['code', 'name', 'date']
    ordering_fields = ['time', 'pct_chg', 'hand']


class StockDailyViewSet(ModelViewSet):
    queryset = StockDaily.objects.all()
    serializer_class = StockDailySerializer
    search_fields = ['code', 'name']
    filter_fields = ['code', 'name', 'date', 'pct_chg']
    ordering_fields = ['pct_chg', 'volume', 'amount']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            self.serializer_class.Meta.depth = 1
        else:
            self.serializer_class.Meta.depth = 0
        return self.serializer_class

    @action(methods=['post'], url_path='is_first_zt', detail=False)
    def checkstock(self, request, *args, **kwargs):
        date = request.data['date']
        print(date)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        try:
            today = StockDaily.objects.filter(date__gte=start_date).order_by('-date').first().date
        except Exception as e:
            print(e)
            return JsonResponse({'results': [], 'msg': f'{date} 没找到当日行情', 'code': status.HTTP_200_OK})
        print(today)
        daily = StockDaily.objects.filter(date=date, is_first_zt=1)
        code_list = [i.code for i in daily]
        today_daily = StockDaily.objects.filter(code__in=code_list, date=today, return_0__gt=0).order_by('-pct_chg')
        serializer = StockDailySerializer(today_daily, many=True)
        return JsonResponse({'results': serializer.data, 'code': status.HTTP_200_OK})

    @action(methods=['post'], url_path='stockinfo', detail=False)
    def stockinfo(self, request, *args, **kwargs):
        code = request.data['code']
        date = request.data['date']
        daily = StockDaily.objects.filter(code=code, date__lt=date).order_by('-date').first()
        daily_data = StockDailySerializer(daily).data
        return JsonResponse(OrderedDict([
            ('results', daily_data)
        ], code=status.HTTP_200_OK))
