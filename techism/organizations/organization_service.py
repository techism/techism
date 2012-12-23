#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism.models import Organization, OrganizationTag
from django.db.models import Count

def get_all():
    return Organization.objects.all()


def get_by_tag(tag):
    organization_list = __get_organization_query_set()
    event_list = organization_list.filter(tags=tag)
    return event_list

def get_tags():
    return OrganizationTag.objects.filter(organization__title__isnull=False).annotate(num_tags=Count('name')).order_by('name').iterator()


def __get_organization_query_set():
    organization_query_set = get_all()
    organization_query_set = organization_query_set.prefetch_related('tags')
    return organization_query_set