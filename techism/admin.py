#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism.models import Event, EventChangeLog, Location, Organization
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['published', 'archived']
    list_display = ['title', 'date_time_begin', 'date_time_end', 'location', 'user', 'archived', 'published']
    
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'url']
    
admin.site.register(Event, EventAdmin)
admin.site.register(Organization, OrganizationAdmin)