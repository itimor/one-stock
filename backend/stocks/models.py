# -*- coding: utf-8 -*-
# author: timor

from django.db import models


class Stock(models.Model):
    name = models.CharField('股票简称', max_length=8, unique=True)
    code = models.CharField('股票代码', max_length=8, unique=True)
    area = models.CharField('地域', max_length=8)
    industry = models.CharField('所属行业', max_length=8)
    market = models.CharField('市场类型', max_length=8)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "股票信息"
        verbose_name_plural = verbose_name
        ordering = ['id']


class StockDaily(models.Model):
    code = models.CharField('股票代码', max_length=10)
    name = models.CharField('股票简称', max_length=10)
    industry = models.CharField('所属行业', max_length=8)
    date = models.DateField(auto_created=True)
    open = models.FloatField('开盘价')
    close = models.FloatField('收盘价')
    low = models.FloatField('最高价')
    high = models.FloatField('最低价')
    pct_chg = models.FloatField('涨跌幅')
    return_0 = models.FloatField('实际涨跌幅')
    pre_close = models.FloatField('昨天收盘价')
    volume = models.FloatField('成交量')
    amount = models.FloatField('成交额')
    turn = models.FloatField('换手率')
    market = models.FloatField('流通市值')
    is_zt = models.BooleanField('涨停', default=False)
    is_first_zt = models.BooleanField('首板', default=False)
    is_second_zt = models.BooleanField('二连板', default=False)
    is_suo = models.BooleanField('缩量', default=False)
    is_bei = models.BooleanField('倍量', default=False)
    is_fang = models.BooleanField('放量', default=False)
    ma10 = models.FloatField('ma10')
    ma20 = models.FloatField('ma20')
    ma30 = models.FloatField('ma30')
    is_ma10_x = models.BooleanField('is_ma10_x', default=False)
    is_ma20_x = models.BooleanField('is_ma20_x', default=False)
    is_ma30_x = models.BooleanField('is_ma30_x', default=False)

    class Meta:
        verbose_name = "当日行情"
        verbose_name_plural = verbose_name
        ordering = ['id']


symbol_map = {'666': '六六大顺',
              '8201': '火箭发射',
              '8202': '快速反弹',
              '8193': '大笔买入',
              '4': '封涨停板',
              '32': '打开跌停板',
              '64': '有大买盘',
              '8207': '竞价上涨',
              '8209': '高开5日线',
              '8211': '向上缺口',
              '8213': '60日新高',
              '8215': '60日大幅上涨',
              '8204': '加速下跌',
              '8203': '高台跳水',
              '8194': '大笔卖出',
              '8': '封跌停板',
              '16': '打开涨停板',
              '128': '有大卖盘',
              '8208': '竞价下跌',
              '8210': '低开5日线',
              '8212': '向下缺口',
              '8214': '60日新低',
              '8216': '60日大幅下跌'
              }


class StockChange(models.Model):
    code = models.CharField('股票代码', max_length=10)
    name = models.CharField('股票简称', max_length=10)
    industry = models.CharField('所属行业', max_length=8)
    date = models.DateField(auto_created=True)
    tm = models.CharField('数字时间', max_length=10)
    time = models.TimeField('时间', max_length=10)
    type = models.CharField(max_length=10, choices=tuple(symbol_map.items()), verbose_name='类型')
    info = models.FloatField('原始数据')
    pct_chg = models.FloatField('幅度')
    hand = models.FloatField('手数')
    close = models.FloatField('收盘价')
    market = models.FloatField('流通市值')

    class Meta:
        verbose_name = "盘口异动"
        verbose_name_plural = verbose_name
        ordering = ['id']
