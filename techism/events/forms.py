#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django import forms
from techism.models import Location

class EventForm(forms.Form):
    title = forms.CharField(max_length=200, label=u'Titel')
    date_time_begin = forms.SplitDateTimeField(label=u'Beginn', input_date_formats= ['%d.%m.%Y'], widget=forms.SplitDateTimeWidget(date_format='%d.%m.%Y', time_format='%H:%M'))
    date_time_end = forms.SplitDateTimeField(label=u'Ende (falls festgelegt)', required=False, input_date_formats=['%d.%m.%Y'], widget=forms.SplitDateTimeWidget(date_format='%d.%m.%Y', time_format='%H:%M'))
    url = forms.URLField()
    description = forms.CharField(label= u'Beschreibung', widget=forms.Textarea, required=False)
    location = forms.ModelChoiceField (Location.objects.all().order_by('name'), required=False)
    tags = forms.CharField(max_length=200, label= u'Tags', required=True)
    
    location_name = forms.CharField(label= u'Name',max_length=200, required=False)
    location_street = forms.CharField(label= u'Stra\u00DFe & Hausnr.',max_length=200, required=False)
    location_city = forms.CharField(label= u'Ort', max_length=200,required=False)
    #latitude = forms.FloatField(required=False)
    #longitude = forms.FloatField(required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        self.clean_Location()
        self.clean_end_date()
        return cleaned_data 
    
    def clean_Location (self):
        cleaned_data = self.cleaned_data
        location_name = cleaned_data.get("location_name")
        location_street = cleaned_data.get("location_street")
        location_city = cleaned_data.get("location_city")
        
        if location_name or location_street or location_city:
            if not location_name:
                self._errors["location_name"] = self.error_class([u'Alle Location Felder müssen gefüllt sein.'])
                del cleaned_data["location_name"]
            if not location_street:
                self._errors["location_street"] = self.error_class([u'Alle Location Felder müssen gefüllt sein.'])
                del cleaned_data["location_street"]
            if not location_city:
                self._errors["location_city"] = self.error_class([u'Alle Location Felder müssen gefüllt sein.'])
                del cleaned_data["location_city"]
  
                
    def clean_end_date (self):
        cleaned_data = self.cleaned_data
        date_time_begin = cleaned_data.get("date_time_begin");
        date_time_end = cleaned_data.get("date_time_end")
        if (date_time_end!=None) and (date_time_begin!=None) and (date_time_end < date_time_begin):
            self._errors["date_time_end"] = self.error_class([u'Das Ende-Datum muss nach dem Beginn-Datum liegen.'])
            del cleaned_data["date_time_end"]