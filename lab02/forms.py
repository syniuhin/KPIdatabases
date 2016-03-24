import datetime
from django import forms

from .db import select_distinct_camera, select_distinct_location, \
  select_distinct_photographer


class PhotoForm(forms.Form):
  photo_name = forms.CharField(label='Photo name', max_length=255,
                               required=False)
  photographer_id = forms.ChoiceField(label='Photographer id',
                                      choices=select_distinct_photographer)
  camera_id = forms.ChoiceField(label='Camera id', required=False,
                                choices=select_distinct_camera)
  location_id = forms.ChoiceField(label='Location id', required=False,
                                  choices=select_distinct_location)
  aperture = forms.FloatField(label='Aperture', required=False)
  iso = forms.IntegerField(label='ISO', required=False)
  shot_time = forms.DateTimeField(label='Shot time',
                                  initial=datetime.datetime.now)
