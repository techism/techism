from django.db import models
from django.contrib.auth.models import User
from techism import utils
from django.utils.encoding import iri_to_uri

class Location(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name;
    
class OrganizationTag (models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name;

class Organization (models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(OrganizationTag)
    
    def __unicode__(self):
        return self.title;

class EventTag (models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name;

class Event(models.Model):
    title = models.CharField(max_length=200)
    date_time_begin = models.DateTimeField()
    date_time_end = models.DateTimeField(blank=True, null=True)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    published = models.BooleanField()
    canceled = models.BooleanField()
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)
    tags = models.ManyToManyField(EventTag)
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        value = utils.slugify(self.title)
        return ("techism.events.views.details", [iri_to_uri("%s-%s" % (value, self.id))])
    
    def get_number_of_days(self):
        if self.date_time_end is None: 
            return 0;
        else:
            delta = self.date_time_end - self.date_time_begin
            return delta.days
        
    
class ChangeType:
    CREATED = 'C'
    UPDATED = 'U'
    CANCELLED = 'D'
    
    Choices = (
        ('C', 'Created'),
        ('U', 'Updated'),
        ('D', 'Canceled'),
    )

class EventChangeLog(models.Model):
    event = models.ForeignKey(Event)
    event_title = models.CharField(max_length=200)
    change_type = models.CharField(max_length=1, choices=ChangeType.Choices)
    date_time = models.DateTimeField(auto_now_add=True)

class Setting(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    value = models.CharField(max_length=500)
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)

class TweetedEvent(models.Model):
    event = models.ForeignKey(Event)
    tweet = models.CharField(max_length=200)
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)
