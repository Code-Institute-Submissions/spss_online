# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import valid_ipn_received
from django.utils import timezone
from signals import subscription_created


license_types = (
    ('1 year', '1'),
    ('2 years', '2'),
)


class Product(models.Model):
    code = models.CharField(max_length=20, default="")
    name = models.CharField(max_length=100, default="")
    osystem = models.CharField(max_length=10, default="")
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    license_type = models.CharField(max_length=50, choices=license_types, default='1')
    image = models.ImageField(upload_to="productimage/", blank=True, null=True)

    def __unicode__(self):
        return '%s (%s)' %(self.name, self.code)


class Purchase (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='purchases')
    product = models.ForeignKey(Product)
    license_end = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '%s - %s' %(self.product.name, self.user.email)




valid_ipn_received.connect(subscription_created)
# Paypal signal for cancel not working properly
# valid_ipn_received.connect(subscription_was_cancelled)