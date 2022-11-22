#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from simple_order.base import models, forms

logger = logging.getLogger(__name__)


def _process_form(request, form_class, instance):
    if request.method == 'DELETE' and instance:
        logger.info(f'User {request.user} deleted {instance}.')
        instance.delete()
        return HttpResponseRedirect(request.path.rsplit('/', 1)[0])

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if not form.is_valid():
            messages.error(request, 'Le formulaire est incorrect. Veuillez corriger les erreurs et le renvoyer.')
        else:
            new_instance = form.save()
            if instance:
                logger.info(f'User {request.user} has modified {new_instance}.')
            else:
                logger.info(f'User {request.user} has added {new_instance}.')
            if form.has_changed():
                messages.success(request, 'Modifications sauvegardées.')
            else:
                messages.info(request, 'Aucune modfication n\'a été faite.')
            return HttpResponseRedirect(new_instance.get_section_url())
    else:
        form = form_class(instance=instance)
    return form


def get_ip(request):
    return HttpResponse(request.META.get('REMOTE_ADDR', '0.0.0.0'), content_type='text/plain; charset=utf-8')


@login_required
def customers(request):
    customers = models.Customer.objects.all()

    return render(request, 'base/customers.html', {
        'customers': customers,
    })


@login_required
def customer(request, pk=None):
    customer = get_object_or_404(models.Customer, id=pk) if pk else None

    form = _process_form(request, forms.CustomerForm, customer)
    if isinstance(form, HttpResponseRedirect):
        return form

    return render(request, 'base/customer.html', {
        'customer': customer,
        'form': form,
    })


@login_required
def products(request):
    products = models.Product.objects.all()

    return render(request, 'base/products.html', {
        'products': products,
    })


@login_required
def product(request, pk=None):
    product = get_object_or_404(models.Product, id=pk) if pk else None

    form = _process_form(request, forms.ProductForm, product)
    if isinstance(form, HttpResponseRedirect):
        return form

    return render(request, 'base/product.html', {
        'product': product,
        'form': form,
    })


@login_required
def deliveries(request):
    deliveries = models.Delivery.objects.all()

    return render(request, 'base/deliveries.html', {
        'deliveries': deliveries,
    })


@login_required
def delivery(request, pk=None):
    delivery = get_object_or_404(models.Delivery, id=pk) if pk else None

    form = _process_form(request, forms.DeliveryForm, delivery)
    if isinstance(form, HttpResponseRedirect):
        return form

    return render(request, 'base/delivery.html', {
        'delivery': delivery,
        'form': form,
    })


def delivery_summary(request, pk):
    delivery = get_object_or_404(models.Delivery, id=pk)

    ordered = {}
    total = 0
    for label, price, quantity in models.OrderedProduct.objects.filter(order__delivery=delivery).order_by('product__label').values_list('product__label', 'product__price', 'quantity'):
        amount = quantity * price
        if label not in ordered:
            ordered[label] = {'label': label, 'price': price, 'quantity': quantity, 'total': amount}
        else:
            ordered[label]['quantity'] += quantity
            ordered[label]['total'] += amount
        total += amount
    for order in ordered.values():
        order['total'] = round(order['total'], 2)

    return render(request, 'base/delivery_summary.html', {
        'delivery': delivery,
        'ordered': ordered,
        'total': round(total, 2),
    })


def delivery_details(request, pk):
    delivery = get_object_or_404(models.Delivery, id=pk) if pk else None

    orders = delivery.order_set.all()

    return render(request, 'base/delivery_details.html', {
        'delivery': delivery,
        'orders': orders,
    })


@login_required
def orders(request):
    deliveries = models.Delivery.objects.all()

    if deliveries:
        delivery = deliveries[0]
        if request.GET.get('date'):
            try:
                dlv_date = datetime.datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
            except Exception as e:
                logger.debug(f'Date conversion failed in {request.path}: {e}')
            else:
                for dlv in deliveries:
                    if dlv.delivery_date == dlv_date:
                        delivery = dlv
                        break
        orders = delivery.order_set.all()
    else:
        delivery = None
        orders = []

    delivery_form = forms.DeliverySelectionForm(initial={'date': delivery.delivery_date.strftime('%Y-%m-%d') if delivery else None})

    return render(request, 'base/orders.html', {
        'delivery': delivery,
        'delivery_form': delivery_form,
        'orders': orders,
    })


@login_required
def order(request, pk=None):
    order = get_object_or_404(models.Order, id=pk) if pk else None

    form = _process_form(request, forms.OrderForm, order)
    if isinstance(form, HttpResponseRedirect):
        return form

    return render(request, 'base/order.html', {
        'order': order,
        'form': form,
    })


@login_required
def order_invoice(request, pk):
    order = get_object_or_404(models.Order, id=pk)

    return render(request, 'base/order_invoice.html', {
        'order': order,
        'owner_name': settings.SO_OWNER_NAME,
        'owner_address': settings.SO_OWNER_ADDRESS,
    })
