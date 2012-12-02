#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.utils import timezone
from techism.events import event_service
from datetime import timedelta

def get_short_term_events():
    today_local = timezone.localtime(timezone.now())
    three_days = today_local + timedelta(days=3)
    event_list = event_service.get_upcomming_published_events_query_set().filter(date_time_begin__gte=today_local).filter (date_time_begin__lte=three_days).order_by('date_time_begin')
    
    return event_list
