# -*- coding: utf-8 -*-
# author: itimor


from rest_framework import routers
from stocks.views import StockViewSet, StockDailyViewSet, StockChangeViewSet

router = routers.DefaultRouter()

router.register(r'stocks', StockViewSet)
router.register(r'stockdaily', StockDailyViewSet)
router.register(r'stockchange', StockChangeViewSet)

urlpatterns = [
]

urlpatterns += router.urls
