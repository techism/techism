from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from techism.rss.feeds import UpcommingEventsRssFeed, UpcommingEventsAtomFeed

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'techism.events.views.index'),
    
    #events
    (r'^events/$', 'techism.events.views.index'),
    (r'^events/tags/(?P<tag_name>.+)/$', 'techism.events.views.tag'),
    (r'^events/edit/(?P<event_id>\d+)/$', 'techism.events.views.edit'),
    (r'^events/cancel/(?P<event_id>\d+)/$', 'techism.events.views.cancel'),
    (r'^events/create/(?P<event_id>\d+)/$', 'techism.events.views.create'),
    (r'^events/create/$', 'techism.events.views.create'),
    (r'^events/locations/$', 'techism.events.views.locations'),
    (r'^events/(?P<event_id>.+)/$', 'techism.events.views.details'),
    
    # orgs
    (r'^orgs/$', 'techism.organizations.views.index'),
    (r'^orgs/tags/(?P<tag_name>.+)/$', 'techism.organizations.views.tag'),
    
    # static pages
    (r'^impressum/$', direct_to_template, { 'template': 'impressum.html' }),
    (r'^about/$', direct_to_template, { 'template': 'about.html' }),
    
    # iCal
    (r'^feed.ics$', 'techism.ical.views.ical'),
    (r'^ical/(?P<event_id>.+).ics$', 'techism.ical.views.ical_single_event'),

    # Atom
    (r'^feeds/atom/upcomming_events$', UpcommingEventsAtomFeed()),
    
    # RSS
    (r'^feeds/rss/upcomming_events$', UpcommingEventsRssFeed()),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
    
    # Login
    (r'^accounts/login/$', direct_to_template, { 'template': 'accounts/login.html' }),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('social_auth.urls')),
)
