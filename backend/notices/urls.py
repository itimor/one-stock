# -*- coding: utf-8 -*-
# author: itimor


from rest_framework import routers
from notices.views import NoticeViewSet, EmailBotViewSet, TelegramBotViewSet, MessageToViewSet

router = routers.DefaultRouter()

router.register(r'notice', NoticeViewSet)
router.register(r'email', EmailBotViewSet)
router.register(r'telegram', TelegramBotViewSet)
router.register(r'to', MessageToViewSet)

urlpatterns = [
]

urlpatterns += router.urls
