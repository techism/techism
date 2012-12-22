#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from techism.organizations import organization_service
from techism.models import Organization, OrganizationTag

def index(request):
    list = organization_service.get_all()
    return render_to_response(
        'organizations/index.html',
        {'organization_list': list}, 
        context_instance=RequestContext(request))


def tag(request, tag_name):
    tag = get_object_or_404(OrganizationTag, name=tag_name)
    list = organization_service.get_by_tag(tag)
    tags = organization_service.get_current_tags()
    return render_to_response(
        'organizations/index.html', 
        {
            'organization_list': list, 
            'tags': tags, 
            'tag_name': tag_name
        }, 
        context_instance=RequestContext(request))
