#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from techism.events import event_service
from techism.events.forms import EventForm, EventCancelForm
from techism.models import Event, EventTag, Location
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.utils import html, timezone
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import datetime
import pytz


def index(request):
    event_list = event_service.get_event_query_set()
    tags = event_service.get_current_tags()
    page = __get_paginator_page(request, event_list)
    return __render_index_template(request, event_list, tags)


def year(request, year):
    event_list = event_service.get_all_event_query_set()
    event_list = event_list.filter(date_time_begin__year=year)
    tags = event_service.get_current_tags()
    return __render_index_template(request, event_list, tags)


def year_tags(request, year, tag_name):
    try:
        tag = EventTag.objects.get(name=tag_name)
        event_list = event_service.get_all_event_query_set()
        event_list = event_list.filter(date_time_begin__year=year)
        event_list = event_list.filter(tags=tag)
    except EventTag.DoesNotExist: 
        event_list = ()
    tags = event_service.get_current_tags()
    return __render_index_template(request, event_list, tags)


def year_month(request, year, month):
    event_list = event_service.get_all_event_query_set()
    event_list = event_list.filter(date_time_begin__year=year)
    event_list = event_list.filter(date_time_begin__month=month)
    tags = event_service.get_current_tags()
    return __render_index_template(request, event_list, tags)


def year_month_tags(request, year, month, tag_name):
    try:
        tag = EventTag.objects.get(name=tag_name)
        event_list = event_service.get_all_event_query_set()
        event_list = event_list.filter(date_time_begin__year=year)
        event_list = event_list.filter(date_time_begin__month=month)
        event_list = event_list.filter(tags=tag)
    except EventTag.DoesNotExist:
        event_list = ()
    tags = event_service.get_current_tags()
    return __render_index_template(request, event_list, tags)


def year_month_day(request, year, month, day):
    event_list = _get_event_query_set_for_year_month_day (year, month, day)
    tags = event_service.get_current_tags()
    return __render_index_template(request, event_list, tags)


def year_month_day_tags(request, year, month, day, tag_name):
    try:
        tag = EventTag.objects.get(name=tag_name)
        event_list = _get_event_query_set_for_year_month_day (year, month, day)
        event_list = event_list.filter(tags=tag)
    except EventTag.DoesNotExist:
        event_list = ()
    tags = event_service.get_current_tags()
    return __render_index_template(request, event_list, tags)


def _get_event_query_set_for_year_month_day (year, month, day):
    now = timezone.localtime(timezone.now())
    utc_offset = now.utcoffset()
    utc = pytz.UTC
    quest_date = datetime.datetime (int(year), int(month), int(day) )

    range_von = utc.localize(datetime.datetime.combine(quest_date,datetime.time.min) - utc_offset)
    range_bis = utc.localize(datetime.datetime.combine(quest_date,datetime.time.max) - utc_offset)

    event_list = event_service.get_all_event_query_set()
    event_list = event_list.filter(date_time_begin__range=(range_von, range_bis))
    return event_list


def tag(request, tag_name):
    try:
        tag = get_object_or_404(EventTag, name=tag_name)
        event_list = event_service.get_event_query_set()
        event_list = event_list.filter(tags=tag)
    except EventTag.DoesNotExist:
        event_list()
    page = __get_paginator_page(request, event_list)
    if page == -1:
        return HttpResponseNotFound()
    tags = event_service.get_current_tags()
    return render_to_response(
        'events/index.html', 
        {
            'event_list': page, 
            'tags': tags, 
            'tag_name': tag_name
        }, 
        context_instance=RequestContext(request))


def details(request, event_id):
    # the event_id may be the slugified, e.g. 'munichjs-meetup-286002'
    splitted_event_id = event_id.rsplit('-', 1)
    if len(splitted_event_id) > 1:
        event_id = splitted_event_id[1]
    
    tags = event_service.get_current_tags()
    event = get_object_or_404(Event, id=event_id)
    return render_to_response(
        'events/details.html',
        {
            'event': event,
            'tags': tags,
            'hostname': request.get_host()
        },
        context_instance=RequestContext(request))


def create(request, event_id=None):
    mode = 'CREATE'
    
    if request.method == 'POST':
        return __save_event(request, mode)
    
    form = EventForm()
    if event_id:
        event = Event.objects.get(id=event_id)
        form = __to_event_form(event)
    
    return render_to_response(
        'events/create.html',
        {
            'form': form,
            'mode': mode
        },
        context_instance=RequestContext(request))


def edit(request, event_id):
    mode = 'EDIT'
    
    event = Event.objects.get(id=event_id)
    if event.user != request.user and request.user.is_superuser == False:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        return __save_event(request, mode, event)
    
    form = __to_event_form(event)
    return render_to_response(
        'events/create.html',
        {
            'form': form,
            'mode': mode
        },
        context_instance=RequestContext(request))


def cancel(request, event_id):
    event = Event.objects.get(id=event_id)
    
    if event.user != request.user and request.user.is_superuser == False:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        return __cancel_event(request, event)
    
    return render_to_response(
        'events/cancel.html',
        {
            'form:': EventCancelForm(),
            'event': event
        },
        context_instance=RequestContext(request))


def __save_event(request, mode, old_event=None):
    form = EventForm(request.POST) 
    if form.is_valid(): 
        event= __create_or_update_event_with_location(form, request.user, old_event)
        # send mail
        if not event.published:
            event_service.send_event_review_mail(event)
        url = event.get_absolute_url()
        return HttpResponseRedirect(url)
    else:
        return render_to_response(
            'events/create.html',
            {
                'form': form, 
                'error': form.errors,
                'mode': mode
            },
            context_instance=RequestContext(request))


def __render_index_template (request, event_list, tags):
    page = __get_paginator_page(request, event_list)
    if page == -1:
        return HttpResponseNotFound()
    return render_to_response(
        'events/index.html',
        {
            'event_list': page,
            'tags': tags,
            'hostname': request.get_host()
        },
        context_instance=RequestContext(request))


def __create_or_update_event_with_location (form, user, event):
    "Creates or updates an Event from the submitted EventForm. If the given Event is None a new Event is created."
    if event == None:
        event = Event()
    
    event.title = form.cleaned_data['title']
    event.date_time_begin = form.cleaned_data['date_time_begin']
    event.date_time_end = form.cleaned_data['date_time_end']
    event.url = form.cleaned_data['url']
    event.description = form.cleaned_data['description']
    event.location = __get_and_update_or_create_location(form)
    
    # Only when a new event is created
    if event.id == None:
        # auto-publish for staff users
        event.published = user.is_staff
        # link event to user
        if user.is_authenticated():
            event.user = user
    
    # Event must be persisted before tags can be set (many-to-may relationship)
    if event.id == None:
        event.save()
    
    event.tags = form.cleaned_data['tags']
    event.save()
    
    return event


def __get_and_update_or_create_location(form):
    "Get, updates, or creates a Location from the submitted EventForm"
    
    return event_service.update_or_create_location(
        form.cleaned_data['location'],
        form.cleaned_data['location_name'],
        form.cleaned_data['location_street'],
        form.cleaned_data['location_city'],
        form.cleaned_data['location_latitude'],
        form.cleaned_data['location_longitude'])


def __to_event_form (event):
    "Converts an Event to an EventForm"
    data = {'title': event.title,
            'url': event.url,
            'description': event.description,
            'tags': list(event.tags.all()),
            'date_time_begin': event.date_time_begin,
            'date_time_end': event.date_time_end,
            'location': event.location.id if event.location else None,
            'location_name': event.location.name if event.location else None,
            'location_street': event.location.street if event.location else None,
            'location_city': event.location.city if event.location else None,
            'location_latitude': event.location.latitude if event.location else None,
            'location_longitude': event.location.longitude if event.location else None
            }
    form = EventForm(initial=data)
    return form;


def __cancel_event(request, event):
    form = EventCancelForm(request.POST) 
    if form.is_valid():
        event.canceled = True;
        event.save()
        url = event.get_absolute_url()
        return HttpResponseRedirect(url)
    else:
        return render_to_response(
        'events/cancel.html',
        {
            'form:': form,
            'error': form.errors,
            'event': event
        },
        context_instance=RequestContext(request))


def locations(request):
    return HttpResponse(event_service.get_locations_as_json(), content_type="application/json")


def __get_paginator_page(request, event_list):
    try:
        num = int(request.GET.get('page', '1'))
    except ValueError:
        num = 1
    
    paginator = Paginator(event_list, 8);
    try:
        page = paginator.page(num)
    except (EmptyPage, InvalidPage):
        page = -1
    
    return page

