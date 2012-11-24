#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import re
import datetime
import pytz

def replace_date(pattern, days_offset, hour, text):
    p = re.compile(pattern)
    today_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    today_local = today_utc.astimezone(pytz.timezone("Europe/Berlin"))
    date_local = today_local + datetime.timedelta(days=days_offset)
    date_local = date_local.replace(hour=hour, minute=0, second=0, microsecond=0)
    date_utc = date_local.astimezone(pytz.utc)
    str = date_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    result = p.sub(str, text)
    return result
    
#Open file
in_file = open ('fixture_template.json', 'r')
text = in_file.read()

#Replace 'YESTERDAY'
text = replace_date('YESTERDAY_BEGIN', -1, 19, text)
text = replace_date('YESTERDAY_END', -1, 22, text)

#Replace 'TOMORROW'
text = replace_date('TOMORROW_BEGIN', 1, 19, text)
text = replace_date('TOMORROW_END', 1, 22, text)

#Replace 'NEXTWEEK'
text = replace_date('NEXTWEEK_BEGIN', 7, 19, text)
text = replace_date('NEXTWEEK_END', 7, 22, text)


out_file = open('fixture.json', 'w')
out_file.write(text)
out_file.close()



    