from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from techism.rss.feeds import UpcommingEventsRssFeed, UpcommingEventsAtomFeed
from techism.sitemaps import TechismSitemap
from techism.events.sitemaps import EventIndexSitemap,EventDetailsSitemap,EventTagsSitemap
from techism.organizations.sitemaps import OrgIndexSitemap,OrgTagsSitemap
from django.contrib import admin


ONE_HOUR = 60 * 60
THREE_HOURS = ONE_HOUR * 3
ONE_DAY = ONE_HOUR * 24
ONE_YEAR = ONE_DAY * 365

admin.autodiscover()

sitemaps = {
    'techism': TechismSitemap,
    'event_index': EventIndexSitemap,
    'event_details': EventDetailsSitemap,
    'event_tags': EventTagsSitemap,
    'organizations_index': OrgIndexSitemap,
    'organizations_tags': OrgTagsSitemap,
}

urlpatterns = patterns('',
    (r'^$', 'techism.events.views.index'),
    
    #events
    (r'^events/$', 'techism.events.views.index'),

    (r'^events/(?P<year>\d{4})/$', 'techism.events.views.year'),
    (r'^events/(?P<year>\d{4})/tags/$', 'techism.events.views.year'),
    (r'^events/(?P<year>\d{4})/tags/(?P<tag_name>.+)/$', 'techism.events.views.year_tags'),
    (r'^events/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'techism.events.views.year_month'),
    (r'^events/(?P<year>\d{4})/(?P<month>\d{1,2})/tags/$', 'techism.events.views.year_month'),
    (r'^events/(?P<year>\d{4})/(?P<month>\d{1,2})/tags/(?P<tag_name>.+)/$', 'techism.events.views.year_month_tags'),
    (r'^events/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'techism.events.views.year_month_day'),
    (r'^events/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/tags/$', 'techism.events.views.year_month_day'),
    (r'^events/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/tags/(?P<tag_name>.+)/$', 'techism.events.views.year_month_day_tags'),
    
    (r'^events/tags/(?P<tag_name>.+)/$', 'techism.events.views.tag'),
    (r'^events/edit/(?P<event_id>\d+)/$', 'techism.events.views.edit'),
    (r'^events/cancel/(?P<event_id>\d+)/$', 'techism.events.views.cancel'),
    (r'^events/create/(?P<event_id>\d+)/$', 'techism.events.views.create'),
    (r'^events/create/$', 'techism.events.views.create'),
    (r'^events/locations/$', 'techism.events.views.locations'),
    (r'^events/[-_0-9a-zA-Z]*?(?P<event_id>\d+)/$', 'techism.events.views.details'),
    
    # orgs
    (r'^orgs/$', 'techism.organizations.views.index'),
    (r'^orgs/tags/(?P<tag_name>.+)/$', 'techism.organizations.views.tag'),
    
    # static pages
    (r'^impressum/$', direct_to_template, { 'template': 'impressum.html' }),
    (r'^about/$', direct_to_template, { 'template': 'about.html' }),
    
    # iCal
    (r'^feed.ics$', 'techism.ical.views.ical'),
    (r'^ical/tags/(?P<tag_name>.+)/feed.ics$', 'techism.ical.views.ical_tag'),
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
    
    #Sitemap
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
)
