import MySQLdb as mdb
from django.http import HttpResponse, HttpResponseRedirect

from models import *

mdb_args = ('localhost', 'root', '***REMOVED***', 'lab02db')


def initiate_insert_into_tables(request):
  initiate_insert_into_camera()
  initiate_insert_into_location()
  initiate_insert_into_photographer()
  # initiate_insert_into_photographer_camera()
  # initiate_insert_into_photographer_location()
  return HttpResponseRedirect('/')


def initiate_insert_into_camera():
  Camera.objects.all().delete()
  with open('/Users/infm/Coding/study/s4/db/lab02/input/camera.csv') as f:
    content = f.readlines()
    colnames = ['name', 'year_created', 'version']
    for line in content:
      Camera.objects.create(**dict(zip(colnames, line.split(','))))
  return HttpResponseRedirect('/camera/list/filter')


def initiate_insert_into_location():
  Location.objects.all().delete()
  with open('/Users/infm/Coding/study/s4/db/lab02/input/location.csv') as f:
    content = f.readlines()
    colnames = ['name', 'lat', 'lng', 'accessible']
    for line in content:
      Location.objects.create(**dict(zip(colnames, line.split('&'))))
  return HttpResponseRedirect('/location/list/filter')


def initiate_insert_into_photographer():
  Photographer.objects.all().delete()
  with open('/Users/infm/Coding/study/s4/db/lab02/input/photographer.csv') as f:
    content = f.readlines()
    colnames = ['name', 'level', 'email']
    for line in content:
      Photographer.objects.create(**dict(zip(colnames, line.split(','))))
  return HttpResponseRedirect('/photographer/list/filter')


def initiate_insert_into_photographer_camera():
  with open(
      '/Users/infm/Coding/study/s4/db/lab02/input/photographer_camera.csv') as f:
    content = f.readlines()
    result = insert_into_photographer_camera(content)
  if result == 'OK':
    return HttpResponse(map(lambda s: s + '\n', content))
  return HttpResponse(result)


def insert_into_photographer_camera(lines):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    for line in lines:
      cur.execute(
        'INSERT INTO `lab02db`.`lab02_photographer_cameras`(photographer_id, camera_id)'
        'VALUES(%s)' % line)
    result = 'OK'
  return result


def initiate_insert_into_photographer_location():
  with open(
      '/Users/infm/Coding/study/s4/db/lab02/input/photographer_location.csv') as f:
    content = f.readlines()
    result = insert_into_photographer_location(content)
  if result == 'OK':
    return HttpResponse(map(lambda s: s + '\n', content))
  return HttpResponse(result)


def insert_into_photographer_location(lines):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    for line in lines:
      cur.execute(
        'INSERT INTO `lab02db`.`lab02_photographer_locations(photographer_id, location_id)`'
        'VALUES(%s)' % line)
    result = 'OK'
  return result
