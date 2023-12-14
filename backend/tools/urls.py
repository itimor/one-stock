# -*- coding: utf-8 -*-
# author: itimor

from django.conf.urls import url
from tools.views import UploadViewSet, FileUploadViewSet, RequestEventViewSet, SimpleViewSet, NetseaseMusic, DogecloudVideo
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'upload', UploadViewSet)
router.register(r'fileupload', FileUploadViewSet)
router.register(r'audit', RequestEventViewSet)
router.register('simple', SimpleViewSet)

urlpatterns = [
    url(r'^netseasemusic/', NetseaseMusic.as_view()),
    url(r'^dogecloud/', DogecloudVideo.as_view()),
]

urlpatterns += router.urls
