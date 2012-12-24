#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from techism.events import event_service
from datetime import datetime


class EventIndexSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return ['/events/']
    
    def location(self, obj):
        return obj

    def lastmod(self, obj):
        return datetime.now()
    
    
class EventDetailsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return event_service.get_upcomming_published_events_query_set()

    def lastmod(self, obj):
        return obj.date_time_modified
    

class EventTagsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return event_service.get_current_tags()

    def location(self, obj):
        return '/events/tags/' + obj.name + '/'
