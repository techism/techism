#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django import forms
from techism.models import Location, EventTag
import re
from django.core.exceptions import ValidationError

class CommaSeparatedTagsWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        if isinstance(value, (list, tuple)):
            value = u', '.join([unicode(v) for v in value])
        return super(CommaSeparatedTagsWidget, self).render(name, value, attrs)
    
class CommaSeparatedTagsFormField(forms.CharField):
    widget = CommaSeparatedTagsWidget
    def clean(self, value):
        # validate non-empty value
        super(CommaSeparatedTagsFormField, self).validate(value)
        
        # split, strip, lower case, filter empty, filter duplicates, allowed characters
        tag_names = value.split(',')
        tag_names = [t.strip().lower() for t in tag_names]
        tag_names = filter(None, tag_names)
        tags = []
        r = re.compile('^[-_\. A-ZÄÖÜa-zäöüß0-9]+$')
        for tag_name in tag_names:
            if not r.match(tag_name):
                raise ValidationError('Unerlaubte Zeichen')
            tag,_ = EventTag.objects.get_or_create(name=tag_name)
            if not tag in tags:
                tags.append(tag)
        
        # validate non-empty tags
        super(CommaSeparatedTagsFormField, self).validate(tags)
        
        return tags
    
class EventForm(forms.Form):
    title = forms.CharField(max_length=200, label=u'Titel')
    url = forms.URLField()
    description = forms.CharField(label= u'Beschreibung', widget=forms.Textarea, required=False)

    date_time_begin = forms.SplitDateTimeField(label=u'Beginn', input_date_formats= ['%d.%m.%Y'], widget=forms.SplitDateTimeWidget(date_format='%d.%m.%Y', time_format='%H:%M'))
    date_time_end = forms.SplitDateTimeField(label=u'Ende (falls festgelegt)', required=False, input_date_formats=['%d.%m.%Y'], widget=forms.SplitDateTimeWidget(date_format='%d.%m.%Y', time_format='%H:%M'))
    
    tags = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
    
    location = forms.ModelChoiceField (Location.objects.all().order_by('name'), required=False, widget=forms.HiddenInput())
    location_name = forms.CharField(label= u'Name',max_length=200, required=False)
    location_street = forms.CharField(label= u'Stra\u00DFe & Hausnr.',max_length=200, required=False)
    location_city = forms.CharField(label= u'Ort', max_length=200,required=False)
    location_latitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    location_longitude = forms.FloatField(required=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = self.cleaned_data
        self.__clean_location()
        self.__clean_end_date()
        return cleaned_data 
    
    def __clean_location(self):
        cleaned_data = self.cleaned_data
        location_name = cleaned_data.get("location_name")
        location_street = cleaned_data.get("location_street")
        location_city = cleaned_data.get("location_city")
        location_latitude = cleaned_data.get("location_latitude")
        location_longitude = cleaned_data.get("location_longitude")
        
        if location_name or location_street or location_city or location_latitude or location_longitude:
            if not location_name:
                self._errors["location_name"] = self.error_class([u'Alle Felder des Veranstaltungsortes müssen gefüllt sein.'])
                del cleaned_data["location_name"]
            if not location_street:
                self._errors["location_street"] = self.error_class([u'Alle Felder des Veranstaltungsortes müssen gefüllt sein.'])
                del cleaned_data["location_street"]
            if not location_city:
                self._errors["location_city"] = self.error_class([u'Alle Felder des Veranstaltungsortes müssen gefüllt sein.'])
                del cleaned_data["location_city"]
            if not location_latitude or not location_longitude:
                self._errors["location"] = self.error_class([u'Koordinaten auf der Karte markieren.'])
                del cleaned_data["location_latitude"]
                del cleaned_data["location_longitude"]
  
                
    def __clean_end_date(self):
        cleaned_data = self.cleaned_data
        date_time_begin = cleaned_data.get("date_time_begin");
        date_time_end = cleaned_data.get("date_time_end")
        if (date_time_end!=None) and (date_time_begin!=None) and (date_time_end < date_time_begin):
            self._errors["date_time_end"] = self.error_class([u'Das Ende-Datum muss nach dem Beginn-Datum liegen.'])
            del cleaned_data["date_time_end"]


class EventCancelForm(forms.Form):
    pass

