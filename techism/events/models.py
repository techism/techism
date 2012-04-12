from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name;
    
    
class Organization (models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
        
    def __unicode__(self):
        return self.title;


class Event(models.Model):
    title = models.CharField(max_length=200)
    date_time_begin = models.DateTimeField()
    date_time_end = models.DateTimeField(blank=True, null=True)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)
    archived = models.BooleanField()
    published = models.BooleanField()
    canceled = models.BooleanField()
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)
    
    def __unicode__(self):
        return self.title
          
