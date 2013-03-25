#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils import html
from techism import utils
from techism.events import event_service
from techism.models import EventTag
from datetime import timedelta
from django.utils import timezone


class UpcommingEventsRssFeed(Feed):
    title = "Techism"
    link = "/events/"
    description = "Techism - Events, Projekte, User Groups in München"

    def items(self):
        today = timezone.now() + timedelta(days=0)
        seven_days = timezone.now() + timedelta(days=7)
        event_list = event_service.get_upcomming_published_events_query_set().filter(date_time_begin__gte=today).filter(date_time_begin__lte=seven_days).order_by('date_time_begin', 'id')
        return event_list

    def item_title(self, item):
        first_publish_date = item.date_time_begin - timedelta(days=7)
        _, prefix = utils.get_changed_and_change_prefix(item, first_publish_date)
        
        date_time_begin_localtime = timezone.localtime(item.date_time_begin)
        if item.get_number_of_days() > 1:
            date_time_end_localtime = timezone.localtime(item.date_time_end)
            dateString = date_time_begin_localtime.strftime("%d.%m.%Y") + "-" + date_time_end_localtime.strftime("%d.%m.%Y")
        else:
            dateString = date_time_begin_localtime.strftime("%d.%m.%Y %H:%M")
        title = prefix + item.title + " - " + dateString
        # escape title (html tags)
        return html.escape(title)

    def item_description(self, item):
        # escape description (html tags)
        description = html.escape(item.description)
        # add html linebreaks
        description = html.linebreaks(description)
        return description
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def author_name(self):
        return "Techism"
    
    def item_pubdate(self, item):
        return item.date_time_modified


class UpcommingEventsTagsRssFeed(UpcommingEventsRssFeed):

    def get_object(self, request, tag_name):
        try:
            tag = EventTag.objects.get(name=tag_name)
            return tag
        except EventTag.DoesNotExist: 
            return None

    def items(self, obj):
        if (obj):
            print obj
            today = timezone.now() + timedelta(days=0)
            seven_days = timezone.now() + timedelta(days=7)
            event_list = event_service.get_upcomming_published_events_query_set()
            event_list = event_list.filter(date_time_begin__gte=today).filter(date_time_begin__lte=seven_days)
            event_list = event_list.filter (tags=obj)
            event_list.order_by('date_time_begin', 'id')
        else:
            event_list = ()
        return event_list


class UpcommingEventsAtomFeed(UpcommingEventsRssFeed):
    feed_type = Atom1Feed


class UpcommingEventsTagsAtomFeed(UpcommingEventsTagsRssFeed):
    feed_type = Atom1Feed