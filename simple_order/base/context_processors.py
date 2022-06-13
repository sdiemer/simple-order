#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import reverse


def common(request):
    if request.user.is_authenticated:
        menu_list = [
            {'url': reverse('orders'), 'label': 'Commandes', 'icon': 'fa-list'},
            {'url': reverse('customers'), 'label': 'Clients', 'icon': 'fa-users'},
            {'url': reverse('products'), 'label': 'Produits', 'icon': 'fa-tags'},
            {'url': reverse('deliveries'), 'label': 'Livraisons', 'icon': 'fa-truck'},
        ]
        if request.user.is_superuser:
            menu_list.extend([
                {'url': '/admin/', 'label': 'Admin Django', 'icon': 'fa-cogs'},
            ])
    else:
        menu_list = []
    for entry in menu_list:
        if request.path[:len(entry['url'])] == entry['url']:
            entry['active'] = True

    return {
        'menu_list': menu_list,
        'site_title': settings.SO_SITE_TITLE,
    }
