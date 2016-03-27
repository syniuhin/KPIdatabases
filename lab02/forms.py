import datetime
from django import forms

from .db import select_distinct_camera, select_distinct_location, \
  select_distinct_photographer


class PhotoForm(forms.Form):
  name = forms.CharField(label='Photo name', max_length=255,
                         required=False)
  photographer_id = forms.ChoiceField(label='Photographer',
                                      choices=select_distinct_photographer)
  camera_id = forms.ChoiceField(label='Camera', required=False,
                                choices=select_distinct_camera)
  location_id = forms.ChoiceField(label='Location', required=False,
                                  choices=select_distinct_location)
  aperture = forms.FloatField(label='Aperture', required=False)
  iso = forms.IntegerField(label='ISO', required=False)
  shot_time = forms.DateTimeField(label='Shot time',
                                  initial=datetime.datetime.now)


class CameraAttributesForm(forms.Form):
  date_created_from = forms.DateField(label='From', required=False)
  date_created_to = forms.DateField(label='To', required=False)
  version = forms.IntegerField(label='Version', required=False)


class LocationAttributesForm(forms.Form):
  accessible = forms.BooleanField(label='Accessible', required=False)
  lat = forms.FloatField(label='Latitude', required=False)
  lng = forms.FloatField(label='Longitude', required=False)