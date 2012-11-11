#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils import html
from techism.rss import feed_service
from techism.events import event_service
from datetime import timedelta
from django.utils import timezone


class UpcommingEventsRssFeed(Feed):
    title = "Techism"
    link = "/events/"
    description = "Techism - Events, Projekte, User Groups in München"

    def items(self):
        today = timezone.now() + timedelta(days=0)
        seven_days = timezone.now() + timedelta(days=7)
        event_list = event_service.get_upcomming_published_events_query_set().filter(date_time_begin__gte=today).filter(date_time_begin__lte=seven_days).order_by('date_time_begin')
        return event_list

    def item_title(self, item):
        prefix = feed_service.get_change_log_prefix(item)
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

class UpcommingEventsAtomFeed(UpcommingEventsRssFeed):
    feed_type = Atom1Feed