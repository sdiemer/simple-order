#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Django
from django.urls import re_path
# simple_order
from simple_order.base import views


urlpatterns = [
    re_path(r'^get_ip/$', views.get_ip, name='get_ip'),
    re_path(r'^clients/$', views.customers, name='customers'),
    re_path(r'^clients/ajouter/$', views.customer, name='customer_add'),
    re_path(r'^clients/(?P<pk>\d+)/$', views.customer, name='customer'),
    re_path(r'^produits/$', views.products, name='products'),
    re_path(r'^produits/ajouter/$', views.product, name='product_add'),
    re_path(r'^produits/(?P<pk>\d+)/$', views.product, name='product'),
    re_path(r'^livraisons/$', views.deliveries, name='deliveries'),
    re_path(r'^livraisons/ajouter/$', views.delivery, name='delivery_add'),
    re_path(r'^livraisons/(?P<pk>\d+)/$', views.delivery, name='delivery'),
    re_path(r'^livraisons/(?P<pk>\d+)/recapitulatif/$', views.delivery_summary, name='delivery_summary'),
    re_path(r'^livraisons/(?P<pk>\d+)/details/$', views.delivery_details, name='delivery_details'),
    re_path(r'^commandes/$', views.orders, name='orders'),
    re_path(r'^commandes/ajouter/$', views.order, name='order_add'),
    re_path(r'^commandes/(?P<pk>\d+)/$', views.order, name='order'),
    re_path(r'^commandes/(?P<pk>\d+)/facture/$', views.order_invoice, name='order_invoice'),
]
