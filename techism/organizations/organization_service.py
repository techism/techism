#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism.models import Organization

def get_all():
    return Organization.objects.all()