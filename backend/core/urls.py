# -*- coding: utf-8 -*-
# author: timor

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from rest_framework.documentation import include_docs_urls
from core import settings

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              [
                  # 工具管理
                  url(r'api/tool/', include(('tools.urls', 'tools'), namespace="tools")),
                  # 系统管理
                  url(r'api/sys/', include(('systems.urls', 'systems'), namespace="systems")),
                  # 通知管理
                  url(r'api/notice/', include(('notices.urls', 'notices'), namespace="notices")),
                  # 股票管理
                  url(r'api/stock/', include(('stocks.urls', 'stocks'), namespace="stocks")),
              ]

if settings.APP_ENV == 'mac':
    urlpatterns += [
        # api文档
        url(r'^docs/', include_docs_urls(title='X Document')),
        # 静态模板
        url(r'', TemplateView.as_view(template_name="index.html")),
    ]
else:
    from django.contrib import admin

    urlpatterns += [
        # 管理后台
        url(r'^admin/', admin.site.urls),
    ]
