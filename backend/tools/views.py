# -*- coding: utf-8 -*-
# author: timor

from rest_framework import viewsets, permissions
from common import status
from rest_framework.views import APIView
from tools.models import *
from tools.serializers import *
from common.views import ModelViewSet, FKModelViewSet, BulkModelViewSet, JsonResponse
from utils.index import get_163music
from utils.dogecloud_api import Dogecloud


class UploadViewSet(ModelViewSet):
    queryset = Upload.objects.all().order_by("-create_time")
    serializer_class = UploadSerializer
    filter_fields = ['type']


class FileUploadViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer


class RequestEventViewSet(ModelViewSet):
    queryset = RequestEvent.objects.all()
    serializer_class = RequestEventSerializer
    search_fields = ['uri', 'query_string', 'user', 'remote_ip']
    filter_fields = ['method']


class SimpleViewSet(BulkModelViewSet):
    queryset = SimpleModel.objects.all()
    serializer_class = SimpleSerializer
    permission_classes = [permissions.AllowAny]
    filter_fields = ['id', 'name']


class NetseaseMusic(APIView):
    def post(self, request, *args, **kwargs):
        data = get_163music()
        return JsonResponse({'results': data, 'code': status.HTTP_200_OK})


class DogecloudVideo(APIView):
    def post(self, request, *args, **kwargs):
        bucket = request.data['bucket']
        api_path = f'/oss/file/list.json?bucket={bucket}'
        dogecloud_api = Dogecloud(api_path, "")
        data = dogecloud_api.request_get()['data']['files']
        return JsonResponse({'results': data, 'code': status.HTTP_200_OK})
