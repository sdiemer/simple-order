#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import re

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models as dj_models

logger = logging.getLogger('simple_order.base.models')


def phone_validator(val):
    if not re.match(r'\d{10}', val):
        raise ValidationError('Le numéro de téléphone est incorrect (10 chiffres sont attendus).')


class BaseModel(dj_models.Model):
    add_date = dj_models.DateTimeField('date d\'ajout', auto_now_add=True)
    mod_date = dj_models.DateTimeField('date de modification', auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'#{self.id}: {self.add_date}'


class Customer(BaseModel):
    name = dj_models.CharField('nom complet', max_length=300, unique=True)
    address = dj_models.TextField('adresse', blank=True)
    phone = dj_models.CharField('téléphone', max_length=10, blank=True, validators=[phone_validator])

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
        ordering = ['name', '-id']

    def __str__(self):
        return f'#{self.id}: {self.name}'

    def get_section_url(self):
        from django.urls import reverse
        return reverse('customers')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('customer', kwargs={'pk': self.pk})


class Product(BaseModel):
    label = dj_models.CharField('label', max_length=300, unique=True)
    price = dj_models.FloatField('prix', default=0)
    available = dj_models.BooleanField('disponible', blank=True, default=True)

    class Meta:
        verbose_name = 'produit'
        verbose_name_plural = 'produits'
        ordering = ['label', '-id']

    def __str__(self):
        return f'#{self.id}: {self.label} {"☑" if self.available else "☒"}'

    def get_section_url(self):
        from django.urls import reverse
        return reverse('products')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product', kwargs={'pk': self.pk})


class Delivery(BaseModel):
    delivery_date = dj_models.DateField('date de livraison', unique=True)

    class Meta:
        verbose_name = 'livraison'
        verbose_name_plural = 'livraisons'
        ordering = ['-delivery_date', '-id']

    def __str__(self):
        return f'#{self.id}: {self.delivery_date}'

    def get_section_url(self):
        from django.urls import reverse
        return reverse('deliveries')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('delivery', kwargs={'pk': self.pk})

    def total_price(self):
        total = 0
        for order in self.order_set.all():
            total += order.total_price()
        return round(total, 2)


class OrderManager(dj_models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('delivery').select_related('customer').prefetch_related('orderedproduct_set')


class Order(BaseModel):
    customer = dj_models.ForeignKey(Customer, verbose_name='client', on_delete=dj_models.CASCADE)
    products = dj_models.ManyToManyField(Product, verbose_name='produits commandés', through='OrderedProduct')
    delivery = dj_models.ForeignKey(Delivery, verbose_name='livraison', on_delete=dj_models.CASCADE)

    objects = OrderManager()

    class Meta:
        verbose_name = 'commande'
        verbose_name_plural = 'commandes'
        unique_together = ('customer', 'delivery')

    def get_section_url(self):
        from django.urls import reverse
        return reverse('orders')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('order', kwargs={'pk': self.pk})

    def total_price(self):
        total = 0
        for op in self.orderedproduct_set.all():
            total += op.quantity * op.product.price
        return round(total, 2)


class OrderedProductManager(dj_models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('product')


class OrderedProduct(BaseModel):
    order = dj_models.ForeignKey(Order, verbose_name='commande', on_delete=dj_models.CASCADE)
    product = dj_models.ForeignKey(Product, verbose_name='produit', on_delete=dj_models.CASCADE)
    quantity = dj_models.PositiveIntegerField('quantité', validators=[MinValueValidator(1)])

    objects = OrderedProductManager()

    class Meta:
        verbose_name = 'produits commandés'
        verbose_name_plural = 'produits commandés'
        unique_together = ('order', 'product')

    def total_price(self):
        return round(self.quantity * self.product.price, 2)
