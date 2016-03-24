import datetime
from django import forms


class PhotoForm(forms.Form):
  photo_name = forms.CharField(label='Photo name', max_length=255,
                               required=False)
  photographer_id = forms.IntegerField(label='Photographer id')
  camera_id = forms.IntegerField(label='Camera id', required=False)
  location_id = forms.IntegerField(label='Location id', required=False)
  aperture = forms.FloatField(label='Aperture', required=False)
  iso = forms.IntegerField(label='ISO', required=False)
  shot_time = forms.DateTimeField(label='Shot time',
                                  initial=datetime.datetime.now)
