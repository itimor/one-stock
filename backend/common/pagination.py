# -*- coding: utf-8 -*-
# author: itimor

from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from common import status
from common.dispath import JsonResponse


def _positive_int(integer_string, strict=False, cutoff=None):
    """
    分页大小为零不分页
    """
    ret = int(integer_string)
    if ret < 0:
        raise ValueError()
    if (ret == 0) and strict:
        return None
    if cutoff:
        return min(ret, cutoff)
    return ret


class CustomPagination(PageNumberPagination):
    """
    配置分页规则
    """
    page_size = 20
    max_page_size = 1000
    page_size_query_param = 'limit'
    page_query_param = 'page'

    def get_next_params(self):
        if not self.page.has_next():
            return None
        page = self.page.next_page_number()
        params = {k: (v if len(v) > 1 else v[0]) for k, v in self.request.query_params.lists()}
        params['page'] = page
        return params

    def get_previous_params(self):
        if not self.page.has_previous():
            return None
        page = self.page.previous_page_number()
        params = {k: (v if len(v) > 1 else v[0]) for k, v in self.request.query_params.lists()}
        params['page'] = page
        return params

    def get_paginated_response(self, data):
        return JsonResponse(OrderedDict([
            # ('next', self.get_next_link()),
            # ('previous', self.get_previous_link()),
            # ('next_params', self.get_next_params()),
            # ('previous_params', self.get_previous_params()),
            # ('num_pages', self.page.number),
            ('count', self.page.paginator.count),
            ('results', data)
        ], code=status.HTTP_200_OK))

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                return _positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                return None
        return self.page_size
