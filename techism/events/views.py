#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return render_to_response('events/index.html', {}, context_instance=RequestContext(request))
