#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from techism.organizations import organization_service
from techism.models import Organization, OrganizationTag
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def index(request):
    list = organization_service.get_all()
    tags = organization_service.get_tags()
    page = __get_paginator_page(request, list)
    if page == -1:
        return HttpResponseNotFound()
    return render_to_response(
        'organizations/index.html',
        {
         'organization_list': page,
         'tags': tags
        }, 
        context_instance=RequestContext(request))


def tag(request, tag_name):
    tag = get_object_or_404(OrganizationTag, name=tag_name)
    list = organization_service.get_by_tag(tag)
    tags = organization_service.get_tags()
    return render_to_response(
        'organizations/index.html', 
        {
            'organization_list': list, 
            'tags': tags, 
            'tag_name': tag_name
        }, 
        context_instance=RequestContext(request))

    
def __get_paginator_page(request, organization_list):
    try:
        num = int(request.GET.get('page', '1'))
    except ValueError:
        num = 1
    
    paginator = Paginator(organization_list, 8);
    try:
        page = paginator.page(num)
    except (EmptyPage, InvalidPage):
        page = -1
    
    return page

