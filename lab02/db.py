from django.http import HttpResponseRedirect

from models import *


def initiate_insert_into_tables(request):
  insert_into_camera()
  insert_into_location()
  insert_into_photographer()
  insert_into_photographer_camera()
  insert_into_photographer_location()
  return HttpResponseRedirect('/')


def insert_into_camera():
  Camera.objects.all().delete()
  with open('/Users/infm/Coding/study/s4/db/lab02/input/camera.csv') as f:
    content = f.readlines()
    colnames = ['name', 'year_created', 'version']
    for line in content:
      Camera.objects.create(**dict(zip(colnames, line.rstrip().split(','))))


def insert_into_location():
  Location.objects.all().delete()
  with open('/Users/infm/Coding/study/s4/db/lab02/input/location.csv') as f:
    content = f.readlines()
    colnames = ['name', 'lat', 'lng', 'accessible']
    for line in content:
      Location.objects.create(**dict(zip(colnames, line.rstrip().split('&'))))


def insert_into_photographer():
  Photographer.objects.all().delete()
  with open('/Users/infm/Coding/study/s4/db/lab02/input/photographer.csv') as f:
    content = f.readlines()
    colnames = ['name', 'level', 'email']
    for line in content:
      Photographer.objects.create(
        **dict(zip(colnames, line.rstrip().split(','))))


def insert_into_photographer_camera():
  with open(
      '/Users/infm/Coding/study/s4/db/lab02/input/photographer_camera.csv') as f:
    content = f.readlines()
    for line in content:
      photographer_email, camera_name, camera_version = line.rstrip().split(',')
      Photographer.objects.get(email=photographer_email).cameras.add(
        Camera.objects.get(name=camera_name, version=int(camera_version)))


def insert_into_photographer_location():
  with open(
      '/Users/infm/Coding/study/s4/db/lab02/input/photographer_location.csv') as f:
    content = f.readlines()
    for line in content:
      photographer_email, location_name = line.rstrip().split('&')
      print '\"' + location_name + '\"'
      Photographer.objects.get(email=photographer_email).locations.add(
        Location.objects.get(name=location_name))
