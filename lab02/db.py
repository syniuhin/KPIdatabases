import MySQLdb as mdb
from django.http import HttpResponse, HttpResponseRedirect

from models import *

mdb_args = ('localhost', 'root', '***REMOVED***', 'lab02db')


def initiate_insert_into_tables(request):
  initiate_insert_into_camera(request)
  # initiate_insert_into_location(request)
  # initiate_insert_into_photographer(request)
  # initiate_insert_into_photographer_camera(request)
  # initiate_insert_into_photographer_location(request)
  return HttpResponseRedirect('/')


def initiate_insert_into_camera(request):
  with open('/Users/infm/Coding/study/s4/db/lab02/input/camera.csv') as f:
    content = f.readlines()
    colnames = ['name', 'year_created', 'version']
    for line in content:
      Camera.objects.create(**dict(zip(colnames, line.split(','))))
  return HttpResponseRedirect('/camera/list/filter')


def insert_into_camera(lines):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    for line in lines:
      cur.execute('INSERT INTO Camera(name, year_created, version)'
                  'VALUES(%s)' % line)
    result = 'OK'
  return result


def initiate_insert_into_location(request):
  with open('/Users/infm/Coding/study/s4/db/lab02/input/location.csv') as f:
    content = f.readlines()
    result = insert_into_location(content)
  if result == 'OK':
    return HttpResponse(map(lambda s: s + '\n', content))
  return HttpResponse(result)


def insert_into_location(lines):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    for line in lines:
      cur.execute('INSERT INTO Location(name, lat, lng, `accessible`)'
                  'VALUES(%s)' % line)
    result = 'OK'
  return result


def initiate_insert_into_photographer(request):
  with open('/Users/infm/Coding/study/s4/db/lab02/input/photographer.csv') as f:
    content = f.readlines()
    result = insert_into_photographer(content)
  if result == 'OK':
    return HttpResponse(map(lambda s: s + '\n', content))
  return HttpResponse(result)


def insert_into_photographer(lines):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    for line in lines:
      cur.execute('INSERT INTO Photographer(`name`, `level`, email)'
                  'VALUES(%s)' % line)
    result = 'OK'
  return result


def initiate_insert_into_photographer_camera(request):
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


def initiate_insert_into_photographer_location(request):
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


def select_all_camera():
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('SELECT * FROM Camera')
    rows = cur.fetchall()
  return map(lambda row: Camera(*row), rows)


def select_filter_camera(args_dict):
  where = []
  if 'date_created_from' in args_dict and args_dict['date_created_from']:
    where.append('year_created >= \'%s\'' % args_dict['date_created_from'])
  if 'date_created_to' in args_dict and args_dict['date_created_to']:
    where.append('year_created <= \'%s\'' % args_dict['date_created_to'])
  if 'version' in args_dict and args_dict['version']:
    where.append('version = %d' % args_dict['version'])
  if len(where) == 0:
    return select_all_camera(None)
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('SELECT * FROM Camera WHERE %s' % ' AND '.join(where))
    rows = cur.fetchall()
  return map(lambda row: Camera(*row), rows)


def select_all_location(request):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('SELECT * FROM Location')
    rows = cur.fetchall()
  return map(lambda row: Location(*row), rows)


def select_filter_location(args_dict):
  where = []
  if args_dict['lat']:
    where.append('(lat BETWEEN %f AND %f)' %
                 (args_dict['lat'] - .01, args_dict['lat'] + .01))
  if args_dict['lng']:
    where.append('(lng BETWEEN %f AND %f)' %
                 (args_dict['lng'] - .01, args_dict['lng'] + .01))
  if args_dict['accessible']:
    where.append('(`accessible` = %r)' % args_dict['accessible'])
  else:
    where.append('(`accessible` = False)')
  if len(where) == 0:
    return select_all_location(None)
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('SELECT * FROM Location WHERE %s' % ' AND '.join(where))
    rows = cur.fetchall()
  return map(lambda row: Location(*row), rows)


def select_all_photographer(request):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('SELECT * FROM Photographer')
    rows = cur.fetchall()
  return map(lambda row: Photographer(*row), rows)


def select_filter_photographer(args_dict):
  where = []
  if args_dict['photographer_id']:
    where.append('id = %s' % args_dict['photographer_id'])
  if 'level_from' in args_dict and args_dict['level_from']:
    where.append('level >= %d' % args_dict['level_from'])
  if 'level_to' in args_dict and args_dict['level_to']:
    where.append('level <= %d' % args_dict['level_to'])
  if len(where) == 0:
    return select_all_photographer(None)
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('SELECT * FROM Photographer WHERE %s' % ' AND '.join(where))
    rows = cur.fetchall()
  return map(lambda row: Photographer(*row), rows)


def select_filter_photo(args):
  con = mdb.connect(*mdb_args)
  name = args['name']
  with con:
    cur = con.cursor()
    cur.execute('SELECT photo.id AS id, '
                'photo.name AS name, '
                'ph.name AS photographer_name, '
                'cam.name AS camera_name, '
                'loc.name AS location_name, '
                'photo.aperture, photo.iso, photo.shot_time '
                'FROM `lab02db`.`Photo` AS photo '
                'LEFT JOIN `lab02db`.`Photographer` AS ph ON photo.photographer_id = ph.id '
                'LEFT JOIN `lab02db`.`Camera` AS cam ON photo.camera_id = cam.id '
                'LEFT JOIN `lab02db`.`Location` AS loc ON photo.location_id = loc.id '
                'WHERE MATCH(photo.name) '
                'AGAINST (\'%s\' IN BOOLEAN MODE)' % name)
    rows = cur.fetchall()
  return map(lambda row: Photo(*row), rows)
