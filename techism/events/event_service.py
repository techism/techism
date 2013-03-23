#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism.models import EventTag
from techism.models import Event
from django.db.models import Count, Q
from django.utils import timezone
import datetime
from django.core.mail import mail_managers
from django.conf import settings

def get_current_tags():
    published = Q(event__published=True)
    not_or_recently_started = Q(event__date_time_begin__gte=timezone.now() - datetime.timedelta(hours=1))
    not_ended = Q(event__date_time_end__gte=timezone.now())
    return EventTag.objects.filter(published, (not_or_recently_started | not_ended)).annotate(num_tags=Count('name')).order_by('name')

def get_upcomming_published_events_query_set():
    published = Q(published=True)
    not_or_recently_started = Q(date_time_begin__gte=timezone.now() - datetime.timedelta(hours=1))
    not_ended = Q(date_time_end__gte=timezone.now())
    return Event.objects.filter(published, (not_or_recently_started | not_ended))

def get_all_published_events_query_set():
    published = Q(published=True)
    return Event.objects.filter(published)

def send_event_review_mail(event):
    subject = u'Neues Event - bitte prüfen'
    message_details = u'Titel: %s\n\nBeschreibung: %s\n\n' % (event.title, event.description)
    message_urls = u'Login-Url: %s\n\nEvent-Url: %s\n\n' % (settings.HTTPS_URL+"/accounts/login/", settings.HTTPS_URL+"/admin/techism/event/"+str(event.id)+"/")
    message = message_details + message_urls
    mail_managers(subject, message)
