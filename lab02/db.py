import datetime
from django.http import HttpResponse
import MySQLdb as mdb
import time

from .fake_models import *

mdb_args = ('localhost', 'root', '***REMOVED***', 'lab02db')


def create_tables(request):
  create_camera(request)
  create_location(request)
  create_photographer(request)
  create_photographer_camera(request)
  create_photographer_location(request)
  create_photo(request)
  return HttpResponse('Tables created')


def drop_tables(request):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS `lab02db`.`Photo`')
    cur.execute('DROP TABLE IF EXISTS `lab02db`.`PhotographerCamera`')
    cur.execute('DROP TABLE IF EXISTS `lab02db`.`PhotographerLocation`')
    cur.execute('DROP TABLE IF EXISTS `lab02db`.`Photographer`')
    cur.execute('DROP TABLE IF EXISTS `lab02db`.`Camera`')
    cur.execute('DROP TABLE IF EXISTS `lab02db`.`Location`')
  return HttpResponse('Tables dropped')


def create_camera(request):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS `lab02db`.`Camera`')
    cur.execute(
      """
      CREATE TABLE IF NOT EXISTS `lab02db`.`Camera` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(255) NOT NULL,
        `year_created` DATE NULL,
        `version` INT NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE INDEX `name_UNIQUE` (`name` ASC))
      ENGINE = InnoDB
      """)
  return HttpResponse('Camera created')


def create_photographer(request):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS `lab02db`.`Photographer`')
    cur.execute(
      """
      CREATE TABLE IF NOT EXISTS `lab02db`.`Photographer` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(255) NULL,
        `level` INT ZEROFILL NOT NULL,
        `email` VARCHAR(255) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE INDEX `email_UNIQUE` (`email` ASC))
      ENGINE = InnoDB
      """)
  return HttpResponse('Photographer created')


def create_location(request):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS `lab02db`.`Location`')
    cur.execute(
      """
      CREATE TABLE IF NOT EXISTS `lab02db`.`Location` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(255) NULL,
        `lat` FLOAT(10,6) NOT NULL,
        `lng` FLOAT(10,6) NOT NULL,
        `accessible` TINYINT(1) NOT NULL,
        PRIMARY KEY (`id`))
      ENGINE = InnoDB
      """)
  return HttpResponse('Location created')


def create_photographer_camera(request):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS `lab02db`.`PhotographerCamera`')
    cur.execute(
      """
      CREATE TABLE IF NOT EXISTS `lab02db`.`PhotographerCamera` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `camera_id` INT NOT NULL,
        `photographer_id` INT NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE INDEX `pair_UNIQUE` (`camera_id`,`photographer_id`),
        CONSTRAINT `fk_PhotographerCamera_Camera`
          FOREIGN KEY (`camera_id`)
          REFERENCES `lab02db`.`Camera` (`id`)
          ON DELETE CASCADE
          ON UPDATE CASCADE,
        CONSTRAINT `fk_PhotographerCamera_Photographer`
          FOREIGN KEY (`photographer_id`)
          REFERENCES `lab02db`.`Photographer` (`id`)
          ON DELETE CASCADE
          ON UPDATE CASCADE)
      ENGINE = InnoDB
      """)
  return HttpResponse('PhotographerCamera created')


def create_photographer_location(request):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS `lab02db`.`PhotographerLocation`')
    cur.execute(
      """
      CREATE TABLE IF NOT EXISTS `lab02db`.`PhotographerLocation` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `photographer_id` INT NOT NULL,
        `location_id` INT NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE INDEX `pair_UNIQUE` (`photographer_id`, `location_id`),
        CONSTRAINT `fk_PhotographerLocation_Photographer`
          FOREIGN KEY (`photographer_id`)
          REFERENCES `lab02db`.`Photographer` (`id`)
          ON DELETE CASCADE
          ON UPDATE CASCADE,
        CONSTRAINT `fk_PhotographerLocation_Location`
          FOREIGN KEY (`location_id`)
          REFERENCES `lab02db`.`Location` (`id`)
          ON DELETE CASCADE
          ON UPDATE CASCADE)
      ENGINE = InnoDB
      """)
  return HttpResponse('PhotographerLocation created')


def create_photo(request):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS `lab02db`.`Photo`')
    cur.execute(
      """
      CREATE TABLE IF NOT EXISTS `lab02db`.`Photo` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `camera_id` INT NULL,
        `location_id` INT NULL,
        `photographer_id` INT NOT NULL,
        `name` VARCHAR(45) NULL,
        `aperture` FLOAT NULL,
        `iso` INT NULL,
        `shot_time` DATETIME NOT NULL,
        PRIMARY KEY (`id`),
        INDEX `fk_Photo_Camera_idx` (`camera_id` ASC),
        INDEX `fk_Photo_Location_idx` (`location_id` ASC),
        INDEX `fk_Photo_Photographer_idx` (`photographer_id` ASC),
        CONSTRAINT `fk_Photo_Camera`
          FOREIGN KEY (`camera_id`)
          REFERENCES `lab02db`.`Camera` (`id`)
          ON DELETE SET NULL
          ON UPDATE CASCADE,
        CONSTRAINT `fk_Photo_Location`
          FOREIGN KEY (`location_id`)
          REFERENCES `lab02db`.`Location` (`id`)
          ON DELETE SET NULL
          ON UPDATE CASCADE,
        CONSTRAINT `fk_Photo_Photographer`
          FOREIGN KEY (`photographer_id`)
          REFERENCES `lab02db`.`Photographer` (`id`)
          ON DELETE CASCADE
          ON UPDATE CASCADE)
      ENGINE = MyISAM
      """)
  return HttpResponse('Photo created')


def initiate_insert_into_tables(request):
  initiate_insert_into_camera(request)
  initiate_insert_into_location(request)
  initiate_insert_into_photographer(request)
  initiate_insert_into_photographer_camera(request)
  initiate_insert_into_photographer_location(request)
  return HttpResponse('Tables loaded')


def initiate_insert_into_camera(request):
  with open('/Users/infm/Coding/study/s4/db/lab02/input/camera.csv') as f:
    content = f.readlines()
    result = insert_into_camera(request, content)
  if result == 'OK':
    return HttpResponse(map(lambda s: s + '\n', content))
  return HttpResponse(result)


def insert_into_camera(request, lines):
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
    result = insert_into_location(request, content)
  if result == 'OK':
    return HttpResponse(map(lambda s: s + '\n', content))
  return HttpResponse(result)


def insert_into_location(request, lines):
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
    result = insert_into_photographer(request, content)
  if result == 'OK':
    return HttpResponse(map(lambda s: s + '\n', content))
  return HttpResponse(result)


def insert_into_photographer(request, lines):
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
    result = insert_into_photographer_camera(request, content)
  if result == 'OK':
    return HttpResponse(map(lambda s: s + '\n', content))
  return HttpResponse(result)


def insert_into_photographer_camera(request, lines):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    for line in lines:
      cur.execute('INSERT INTO PhotographerCamera(photographer_id, camera_id)'
                  'VALUES(%s)' % line)
    result = 'OK'
  return result


def initiate_insert_into_photographer_location(request):
  with open(
      '/Users/infm/Coding/study/s4/db/lab02/input/photographer_location.csv') as f:
    content = f.readlines()
    result = insert_into_photographer_location(request, content)
  if result == 'OK':
    return HttpResponse(map(lambda s: s + '\n', content))
  return HttpResponse(result)


def insert_into_photographer_location(request, lines):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    for line in lines:
      cur.execute(
        'INSERT INTO PhotographerLocation(photographer_id, location_id)'
        'VALUES(%s)' % line)
    result = 'OK'
  return result


def get_photo_sql_args(args_dict):
  columns = ['camera_id', 'location_id', 'photographer_id', 'name',
             'aperture', 'iso', 'shot_time']
  existing_columns = {unicode(col): args_dict[col]
                      for col in columns if args_dict[col]}
  return (','.join(existing_columns.keys()),
          ','.join(map(
            lambda v: '\'' + v + '\'' if isinstance(v, basestring)
            else v.strftime('\'%Y-%m-%d %H:%M:%S\'')
            if isinstance(v, datetime.datetime)
            else str(v), existing_columns.values())))


def insert_into_photo_single(d):
  con = mdb.connect(*mdb_args)
  attributes, values = get_photo_sql_args(d)
  with con:
    cur = con.cursor()
    cur.execute('INSERT INTO Photo(%s) VALUES(%s)' % (attributes, values))


def edit_photo_single(d):
  con = mdb.connect(*mdb_args)
  attributes, values = get_photo_sql_args(d)
  attributes, values = attributes.split(','), values.split(',')
  update_arg = ','.join([attr + '=' + val
                         for attr, val in zip(attributes, values)])
  with con:
    cur = con.cursor()
    cur.execute(
      'UPDATE Photo SET %s WHERE id = %d' % (update_arg, d['id']))


def delete_photo_by_id(photo_id):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('DELETE FROM Photo WHERE id = %d' % photo_id)


def select_all_camera(request):
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


def select_distinct_camera():
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('SELECT DISTINCT id, name FROM Camera')
    rows = cur.fetchall()
  return ((None, 'None'),) + rows


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


def select_distinct_location():
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('SELECT DISTINCT id, name FROM Location')
    rows = cur.fetchall()
  return ((None, 'None'),) + rows


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


def select_distinct_photographer():
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('SELECT DISTINCT id, name FROM Photographer')
    rows = cur.fetchall()
  return rows


def select_all_photographer_location(request):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute(
      'SELECT ph.name, loc.name FROM PhotographerLocation AS ph_loc '
      'LEFT JOIN Photographer AS ph ON ph_loc.photographer_id = ph.id '
      'LEFT JOIN Location AS loc ON ph_loc.location_id = loc.id')
    rows = cur.fetchall()
  return HttpResponse(map(lambda row: str(row) + '\n', rows))


def select_all_photographer_camera(request):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('SELECT ph.name, cam.name FROM PhotographerCamera AS ph_cam '
                'LEFT JOIN Photographer AS ph ON ph_cam.photographer_id = ph.id '
                'LEFT JOIN Camera AS cam ON ph_cam.camera_id = cam.id')
    rows = cur.fetchall()
  return HttpResponse(map(lambda row: str(row) + '\n', rows))


def select_all_photo(request):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute(
      'SELECT photo.id AS id, '
      'photo.name AS name, '
      'ph.name AS photographer_name, '
      'cam.name AS camera_name, '
      'loc.name AS location_name, '
      'photo.aperture, photo.iso, photo.shot_time '
      'FROM `lab02db`.`Photo` AS photo '
      'LEFT JOIN `lab02db`.`Photographer` AS ph ON photo.photographer_id = ph.id '
      'LEFT JOIN `lab02db`.`Camera` AS cam ON photo.camera_id = cam.id '
      'LEFT JOIN `lab02db`.`Location` AS loc ON photo.location_id = loc.id')
    rows = cur.fetchall()
  return map(lambda row: Photo(*row), rows)


def select_filter_photo(args):
  con = mdb.connect(*mdb_args)
  name = args['name']
  if not name:
    return select_all_photo(None)
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


def select_photo_by_id(p_id):
  """
  :param p_id: id of a Photo item to fetch.
  :return: !! dictionary !!
  """
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('SELECT photo.id AS id, '
                'photo.name AS name, '
                'ph.name AS photographer_name, '
                'cam.name AS camera_name, '
                'loc.name AS location_name, '
                'photo.aperture, '
                'photo.iso, '
                'photo.shot_time, '
                'ph.id AS photographer_id, '
                'cam.id AS camera_id, '
                'loc.id AS location_id '
                'FROM `lab02db`.`Photo` AS photo '
                'LEFT JOIN `lab02db`.`Photographer` AS ph ON photo.photographer_id = ph.id '
                'LEFT JOIN `lab02db`.`Camera` AS cam ON photo.camera_id = cam.id '
                'LEFT JOIN `lab02db`.`Location` AS loc ON photo.location_id = loc.id '
                'WHERE photo.id = %d ' % p_id)
    row = cur.fetchall()[0]
  return Photo(*row)
