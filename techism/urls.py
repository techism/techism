from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from techism.rss.feeds import UpcommingEventsRssFeed, UpcommingEventsAtomFeed, UpcommingEventsTagsRssFeed, UpcommingEventsTagsAtomFeed
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
   
    # api
    (r'^api/events/(?P<year>\d{4})/$', 'techism.api.views.events'),
    (r'^api/events/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'techism.api.views.events'),
    (r'^api/events/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'techism.api.views.events'),
    (r'^api/events/$', 'techism.api.views.create'),
    (r'^api/csp/$', 'techism.api.views.csp_reporting'),

    # static pages
    (r'^impressum/$', TemplateView.as_view(template_name='impressum.html')),
    (r'^about/$', TemplateView.as_view(template_name='about.html')),
    
    # iCal
    (r'^feed.ics$', 'techism.ical.views.ical'),
    (r'^ical/tags/(?P<tag_name>.+)/feed.ics$', 'techism.ical.views.ical_tag'),
    (r'^ical/(?P<event_id>.+).ics$', 'techism.ical.views.ical_single_event'),
    
    # Atom
    (r'^feeds/atom/upcomming_events$', UpcommingEventsAtomFeed()),
    (r'^feeds/atom/tags/(?P<tag_name>.+)/upcomming_events$', UpcommingEventsTagsAtomFeed()),
    
    # RSS
    (r'^feeds/rss/upcomming_events$', UpcommingEventsRssFeed()),
    (r'^feeds/rss/tags/(?P<tag_name>.+)/upcomming_events$', UpcommingEventsTagsRssFeed()),
    
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    
    # Login
    (r'^accounts/login/$', TemplateView.as_view(template_name='accounts/login.html' )),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('social_auth.urls')),
    
    #Sitemap
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
)
