from django.db import models
from django.contrib.auth.models import User
from techism import utils
from django.utils.encoding import iri_to_uri
import reversion

class Location(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    historized_since = models.DateTimeField(db_index=True, blank=True, null=True)
    
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
    image = models.ImageField(upload_to="images", blank=True)
    
    def __unicode__(self):
        return self.title;

class EventTag (models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name;

class Event(models.Model):
    title = models.CharField(max_length=200)
    date_time_begin = models.DateTimeField(db_index=True)
    date_time_end = models.DateTimeField(db_index=True, blank=True, null=True)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    published = models.BooleanField(db_index=True)
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
    
    def save(self, *args, **kwargs):
        with reversion.create_revision():
            super(Event, self).save(*args, **kwargs)

class Setting(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    value = models.CharField(max_length=500)
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)

class TweetedEvent(models.Model):
    TWEET_TYPE = (
        ('S', u'Short Term'),
        ('L', u'Long Term'),
    )
    event = models.ForeignKey(Event)
    tweet = models.CharField(max_length=500)
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=1, choices=TWEET_TYPE)

reversion.register(Event)
