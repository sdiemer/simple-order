#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django_web_utils.admin_utils import register_module

from . import models


register_module(models)
