#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import re

from django import forms as dj_forms

from simple_order.base import models

logger = logging.getLogger(__name__)


class DateInput(dj_forms.DateInput):
    input_type = 'date'


class CustomerForm(dj_forms.ModelForm):

    class Meta:
        model = models.Customer
        exclude = ('add_date', 'mod_date')


class ProductForm(dj_forms.ModelForm):

    class Meta:
        model = models.Product
        exclude = ('add_date', 'mod_date')


class DeliverySelectionForm(dj_forms.Form):
    date = dj_forms.ChoiceField(label='Livraison du', required=True, widget=dj_forms.Select(attrs={'onchange': 'this.form.submit()'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].choices = [
            (dlv.delivery_date.strftime('%Y-%m-%d'), dlv.delivery_date.strftime('%Y-%m-%d'))
            for dlv in models.Delivery.objects.all()
        ]


class DeliveryForm(dj_forms.ModelForm):

    class Meta:
        model = models.Delivery
        exclude = ('add_date', 'mod_date')
        widgets = {
            'delivery_date': DateInput()
        }


class OrderForm(dj_forms.ModelForm):

    class Meta:
        model = models.Order
        exclude = ('add_date', 'mod_date', 'products')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_ops = {}
        if self.instance.id:
            for op in self.instance.orderedproduct_set.all():
                current_ops[op.product_id] = op.quantity
        for product in models.Product.objects.filter(available=True):
            self.fields[f'product-{product.id}'] = dj_forms.IntegerField(label=product.label, required=True, initial=current_ops.get(product.id, 0), min_value=0)

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        if self.changed_data:
            for field in self.changed_data:
                mat = re.match(r'product-(\d+)', field)
                if mat:
                    product_id = int(mat.groups()[0])
                    new_quantity = self.cleaned_data[field]
                    if new_quantity == 0:
                        self.instance.orderedproduct_set.filter(product_id=product_id).delete()
                    else:
                        try:
                            op = self.instance.orderedproduct_set.get(product_id=product_id)
                        except models.OrderedProduct.DoesNotExist:
                            op = models.OrderedProduct(order=self.instance, product_id=product_id)
                        op.quantity = new_quantity
                        op.save()
        return result
