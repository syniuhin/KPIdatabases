from django import forms

from .models import *


class PhotoForm(forms.ModelForm):
  class Meta:
    model = Photo
    exclude = []


class PhotoSearchForm(forms.Form):
  name = forms.CharField(label='Search', max_length=255,
                         required=False)


class CameraAttributesForm(forms.Form):
  date_created_from = forms.DateField(label='From', required=False)
  date_created_to = forms.DateField(label='To', required=False)
  version = forms.IntegerField(label='Version', required=False)


class LocationAttributesForm(forms.Form):
  lat_from = forms.FloatField(label='Latitude from', required=False)
  lng_from = forms.FloatField(label='Longitude from', required=False)
  lat_to = forms.FloatField(label='Latitude to', required=False)
  lng_to = forms.FloatField(label='Longitude to', required=False)
  accessible = forms.BooleanField(label='Accessible', required=False)


class PhotographerAttributesForm(forms.Form):
  photographer_id = forms.ModelChoiceField(label="Photographer", required=False,
                                           queryset=Photographer.objects.all())
  level_from = forms.IntegerField(label='Level from', required=False)
  level_to = forms.IntegerField(label='Level to', required=False)
