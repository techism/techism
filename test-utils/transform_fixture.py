#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import re
import datetime
import pytz

def replace_date(pattern, days_offset, text):
    p = re.compile(pattern)
    today = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    date = today + datetime.timedelta(days=days_offset)
    str = date.strftime("%Y-%m-%d")
    result = p.sub(str, text)
    return result
    
#Open file
in_file = open ('fixture_template.json', 'r')
text = in_file.read()

#Replace 'YESTERDAY'
text = replace_date('YESTERDAY', -1, text)

#Replace 'TOMORROW'
text = replace_date('TOMORROW', 1, text)

#Replace 'NEXTWEEK'
text = replace_date('NEXTWEEK', 7, text)


out_file = open('fixture.json', 'w')
out_file.write(text)
out_file.close()



    