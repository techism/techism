#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism.models import Event, EventTag, Location, Organization, OrganizationTag, Setting, TweetedEvent
from django.contrib import admin
import reversion


class EventInline(admin.TabularInline):
    model = Event
    fields = ['title', 'date_time_begin', 'date_time_end', 'url', 'tags', 'published']
    readonly_fields = fields
    ordering = ['-date_time_begin']
    can_delete = False
    max_num = 0
    
class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'street', 'city', 'latitude', 'longitude', 'historized_since']
    ordering = ['historized_since', 'name']
    inlines = [
        EventInline,
    ]

class EventAdmin(reversion.VersionAdmin):
    search_fields = ['title']
    list_filter = ['published']
    list_display = ['title', 'date_time_begin', 'date_time_end', 'location', 'user', 'published']
    date_hierarchy = 'date_time_begin'
    filter_horizontal = ['tags']
    raw_id_fields = ['location', 'user', 'organization']

class EventTagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']
    
class EventChangeLogAdmin(admin.ModelAdmin):
    list_filter = ['change_type']
    list_display = ['event', 'event_title', 'change_type', 'date_time']

class TweetedEventAdmin(admin.ModelAdmin):
    list_display = ['event', 'tweet', 'date_time_created']
    
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'url']

class OrganizationTagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']

class SettingAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']
    
    
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventTag, EventTagAdmin)
admin.site.register(TweetedEvent, TweetedEventAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationTag, OrganizationTagAdmin)
admin.site.register(Setting, SettingAdmin)

