#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from techism.events import event_service
from techism.events.forms import EventForm, EventCancelForm
from techism.models import Event, EventTag, Location
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.utils import html
import json
from geopy import distance

def index(request):
    event_list = event_service.get_upcomming_published_events_query_set().order_by('date_time_begin').prefetch_related('tags').select_related('location')
    tags = event_service.get_current_tags()
    return render_to_response(
        'events/index.html',
        {
            'event_list': event_list,
            'tags': tags,
            'hostname': request.get_host()
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

def tag(request, tag_name):
    tag = get_object_or_404(EventTag, name=tag_name)
    event_list = event_service.get_upcomming_published_events_query_set().filter(tags=tag).order_by('date_time_begin')
    tags = event_service.get_current_tags()
    return render_to_response(
        'events/index.html', 
        {
            'event_list': event_list, 
            'tags': tags, 
            'tag_name': tag_name
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
    
    if form.cleaned_data['location']:
        # existing location
        existing_location = form.cleaned_data['location']
        name_equal = existing_location.name == form.cleaned_data['location_name']
        street_equal = existing_location.street == form.cleaned_data['location_street']
        city_equal = existing_location.city == form.cleaned_data['location_city']
        distance_in_meters = distance.distance((existing_location.latitude, existing_location.longitude),
                      (form.cleaned_data['location_latitude'], form.cleaned_data['location_longitude'])).meters
        if (name_equal and street_equal and city_equal and distance_in_meters < 300):
            # existing location and submitted fields are equal/similar: update
            # existing_location.name=form.cleaned_data['location_name']
            # existing_location.street=form.cleaned_data['location_street']
            # existing_location.city=form.cleaned_data['location_city']
            existing_location.latitude = form.cleaned_data['location_latitude']
            existing_location.longitude = form.cleaned_data['location_longitude']
            existing_location.save()
            return existing_location
        else:
            # existing location and submitted fields differ: create new location
            location = __create_location(form)
            return location
    else:
        # no existing location: create new location
        if form.cleaned_data['location_name']:
            location = __create_location(form)
            return location
        else:
            return None


def __create_location(form):
    "Creates a new Location from the submitted EventForm"
    location = Location()
    location.name=form.cleaned_data['location_name']
    location.street=form.cleaned_data['location_street']
    location.city=form.cleaned_data['location_city']
    location.latitude=form.cleaned_data['location_latitude']
    location.longitude=form.cleaned_data['location_longitude']
    location.save()
    return location


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
    return HttpResponse(__get_locations_as_json())


def __get_locations_as_json():
    location_list = Location.objects.all()
    locations = []
    for location in location_list:
        loc = dict()
        loc['id'] = html.escape(location.id)
        loc['name'] = html.escape(location.name)
        loc['street'] = html.escape(location.street)
        loc['city'] = html.escape(location.city)
        loc['latitude'] = html.escape(location.latitude)
        loc['longitude'] = html.escape(location.longitude)
        locations.append(loc)
    locations_as_json = json.dumps(locations)
    return locations_as_json

