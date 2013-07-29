from django.core.management.base import BaseCommand
from django.conf import settings
from techism.models import Event
import csv
import pytz
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        dirname = os.path.join(settings.STATIC_ROOT, 'export')
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        
        filename = os.path.join(dirname, 'techism-events.csv')
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            
            headers = [
                'title',
                'date_time_begin',
                'date_time_end',
                'url',
                'location_name',
                'location_lat',
                'location_lng',
                'tags',
            ]
            writer.writerow(headers)
            
            events = Event.objects.filter(published=True).order_by('date_time_begin', 'id').prefetch_related('tags').prefetch_related('location').all().iterator()
            for event in events:
                row = [
                    event.title.encode('utf-8'),
                    event.date_time_begin.astimezone(pytz.timezone('Europe/Berlin')).strftime('%Y-%m-%dT%H:%M:%S') if event.date_time_begin else '',
                    event.date_time_end.astimezone(pytz.timezone('Europe/Berlin')).strftime('%Y-%m-%dT%H:%M:%S') if event.date_time_end else '',
                    event.url.encode('utf-8') if event.url else '',
                    event.location.name.encode('utf-8') if event.location else '',
                    event.location.latitude if event.location else '',
                    event.location.longitude if event.location else '',
                    '|'.join([tag.name.encode('utf-8') for tag in event.tags.all()]) if event.tags else ''
                ]
                writer.writerow(row)

