#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.views.decorators.http import require_http_methods
import json
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from techism.events import event_service
from techism.events import json_service
import logging
from django.contrib.auth.decorators import permission_required

@require_http_methods(["POST"])
def csp_reporting(request):
  data = json.loads(request.body)
  values = data["csp-report"]
  logger = logging.getLogger(__name__)
  #TODO: validate
  logger.warning('[CSP-REPORT]' + str(values))
  return HttpResponse('')
	

@require_http_methods(["GET"])
def events(request, year, month = None, day = None):
  event_list = event_service.get_event_query_set()
  event_list = event_list.filter(date_time_begin__year=year)
  if month:
    event_list = event_list.filter(date_time_begin__month=month)
  if day:
    event_list = event_list.filter(date_time_begin__day=day)
  events_as_json = json_service.get_events_as_json(event_list)
  return HttpResponse(events_as_json, mimetype="application/json")


@require_http_methods(["POST"])
@permission_required('is_superuser')
def create(request):
  #TODO: validate
  print 'test'
  event = json_service.get_event_from_json(request.body)
  event.save()
  return HttpResponse('')
