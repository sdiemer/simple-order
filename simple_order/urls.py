#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Django
from django.conf import settings
from django.urls import include, re_path
from django.contrib import admin
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.static import serve


admin.autodiscover()

urlpatterns = [
    # Authentication
    re_path(r'^', include('django.contrib.auth.urls')),
    # Base app
    re_path(r'^', include('simple_order.base.urls')),
    # media serving
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': settings.DEBUG}, name='media'),
    # Django admin
    re_path(r'^admin/', admin.site.urls, name='admin'),
    re_path(r'^', RedirectView.as_view(url='/commandes/', permanent=False, query_string=True)),
]

# test pages
if settings.DEBUG:
    # 404 test page
    urlpatterns.append(re_path(r'^404/$', TemplateView.as_view(template_name='404.html'), name='test_404'))
    # 500 test page
    urlpatterns.append(re_path(r'^500/$', TemplateView.as_view(template_name='500.html'), name='test_500'))

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns.insert(0, re_path(r'^__debug__/', include(debug_toolbar.urls)))
