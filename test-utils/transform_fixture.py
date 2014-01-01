#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re
import datetime
import pytz
from django.utils import timezone

def replace_day_hour(pattern, days_offset, hour, text):
    p = re.compile(pattern)
    today_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    today_local = today_utc.astimezone(pytz.timezone("Europe/Berlin"))
    date_local = today_local + datetime.timedelta(days=days_offset)
    date_local = date_local.replace(hour=hour, minute=0, second=0, microsecond=0)
    date_utc = date_local.astimezone(pytz.utc)
    str = date_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    result = p.sub(str, text)
    return result

def replace_month_day(pattern, months_offset, new_day, text):
    p = re.compile(pattern)
    today_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    today_local = today_utc.astimezone(pytz.timezone("Europe/Berlin"))
    year, month, day = today_local.timetuple()[:3]
    new_month = (month + months_offset - 1) % 12 + 1
    new_year = year - (new_month / 12)
    date_local = today_local.replace(year=new_year, month=new_month, day=new_day, hour=1, minute=0, second=0, microsecond=0)
    date_utc = date_local.astimezone(pytz.utc)
    str = date_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    result = p.sub(str, text)
    return result
    
#Open file
in_file = open ('fixture_template.json', 'r')
text = in_file.read()

#Replace 'NOW'
now_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
begin_utc = now_utc + datetime.timedelta(minutes=-2)
end_utc = now_utc + datetime.timedelta(minutes=2)
text = re.compile('NOW_BEGIN').sub(begin_utc.strftime("%Y-%m-%dT%H:%M:%SZ"), text)
text = re.compile('NOW_END').sub(end_utc.strftime("%Y-%m-%dT%H:%M:%SZ"), text)

#Replace 'YESTERDAY'
text = replace_day_hour('YESTERDAY_BEGIN', -1, 19, text)
text = replace_day_hour('YESTERDAY_END', -1, 22, text)

#Replace 'TOMORROW'
text = replace_day_hour('TOMORROW_BEGIN', 1, 19, text)
text = replace_day_hour('TOMORROW_END', 1, 22, text)

#Replace 'NEXTWEEK'
text = replace_day_hour('NEXTWEEK_BEGIN', 7, 19, text)
text = replace_day_hour('NEXTWEEK_END', 7, 22, text)

#Replace 'LASTMONTH'
text = replace_month_day('LASTMONTH_BEGIN', -1, 2, text)
text = replace_month_day('LASTMONTH_END', -1, 3, text)


out_file = open('fixture.json', 'w')
out_file.write(text)
out_file.close()



    