#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pytz
from pytz import timezone
import reversion

utc = pytz.utc
cet = timezone('Europe/Berlin')

def cet_to_utc (cet_datetime):
    if cet_datetime == None:
        return None
    localized = cet.localize(cet_datetime)
    utc_datetime = localized.astimezone(utc)
    return utc_datetime

def utc_to_cet (utc_datetime):
    if utc_datetime == None:
        return None
    localized = utc.localize(utc_datetime)
    cet_datetime = localized.astimezone(cet)
    return cet_datetime

def localize_to_utc (datetime):
    if datetime == None:
        return None
    if datetime.tzinfo == None:
        localized = utc.localize(datetime)
        return localized
    else:
        utc_datetime = datetime.astimezone(utc)
        return utc_datetime

def slugify(value):
    import re
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = re.sub('[-\s]+', '-', value)
    return value

def get_canceled_and_cancel_prefix(event):
    if event.canceled:
        return (True,  "[Abgesagt] ")
    return (False, "")

def get_changed_and_change_prefix(event, from_date):
    current_version = None
    previous_version = None
    
    version_list = reversion.get_for_object(event)
    for version in version_list:
        # 1st element is the current version
        if not current_version:
            current_version = version
        
        # find compare version
        previous_version = version
        if version.revision.date_created < from_date:
            break
    
    if current_version and previous_version:
        if current_version.field_dict['canceled'] == True:
            return (True, "[Abgesagt] ")
        if current_version.field_dict['date_time_begin'] != previous_version.field_dict['date_time_begin']:
            return (True, "[Update][Datum] ")
        if current_version.field_dict['location'] and previous_version.field_dict['location'] and current_version.field_dict['location'] != previous_version.field_dict['location']:
            return (True, "[Update][Ort] ")
    
    return (False, "")

def cache(cache_timeout, viewfunc):
    def _cache_controller(request, *args, **kwargs):
        from django.utils.cache import patch_cache_control, patch_response_headers
        response = viewfunc(request, *args, **kwargs)
        if not response.has_header('Cache-Control'):
            patch_response_headers(response, cache_timeout=cache_timeout)
        patch_cache_control(response, public=True, must_revalidate=True)
        return response
    return _cache_controller

