from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from techism.rss.feeds import UpcommingEventsRssFeed, UpcommingEventsAtomFeed

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'techism.events.views.index'),
    
    #events
    (r'^events/$', 'techism.events.views.index'),
    (r'^events/(?P<event_id>.+)/$', 'techism.events.views.details'),
    (r'^events/create/$', 'techism.events.views.create'),
    
    # orgs
    
    # static pages
    (r'^impressum/$', direct_to_template, { 'template': 'impressum.html' }),
    (r'^about/$', direct_to_template, { 'template': 'about.html' }),
    
    # iCal
    (r'^feed.ics$', 'techism.ical.views.ical'),
    (r'^ical/(?P<event_id>.+).ics$', 'techism.ical.views.ical_single_event'),

    # Atom
    (r'^feeds/atom/upcomming_events$', UpcommingEventsAtomFeed()),
    
    #RSS
    (r'^feeds/rss/upcomming_events$', UpcommingEventsRssFeed()),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
