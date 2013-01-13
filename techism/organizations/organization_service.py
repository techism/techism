#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism.models import Organization, OrganizationTag
from django.db.models import Count

def get_all():
    return __get_organization_query_set_with_tags()


def get_by_tag(tag):
    organization_list = __get_organization_query_set_with_tags()
    organization_list = organization_list.filter(tags=tag)
    return organization_list

def get_tags():
    return OrganizationTag.objects.filter(organization__title__isnull=False).annotate(num_tags=Count('name')).order_by('name').all()


def __get_organization_query_set_with_tags():
    organization_query_set = Organization.objects
    organization_query_set = organization_query_set.prefetch_related('tags')
    return organization_query_set