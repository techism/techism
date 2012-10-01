#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import re
import datetime
import time

#Open file
in_file = open ('fixture_template.json', 'r')
text = in_file.read()

#Replace 'YESTERDAY'
p = re.compile ('TOMORROW')
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
tomorrow_str = time.strftime("%Y-%m-%dT19:00:00.000Z")
result = p.sub(tomorrow_str, text)


#Replace 'TOMORROW'


#Replace 'NEXTWEEK'


out_file = open('fixture.json', 'w')
out_file.write(result)
out_file.close()
