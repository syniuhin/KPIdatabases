import datetime
from django.http import HttpResponse
import MySQLdb as mdb
import time

from .fake_models import Photo

mdb_args = ('localhost', 'root', '***REMOVED***', 'lab02db')


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
      ENGINE = InnoDB
      """)
  return HttpResponse('Photo created')


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


def insert_into_photo_single(d):
  con = mdb.connect(*mdb_args)
  columns = ['camera_id', 'location_id', 'photographer_id', 'photo_name',
             'aperture', 'iso', 'shot_time']
  existing_columns = {col: d[col] for col in columns if d[col]}
  with con:
    cur = con.cursor()
    cur.execute(
      'INSERT INTO Photo(%s) VALUES(%s)' %
      (','.join(existing_columns.keys()),
       ','.join(
         map(
           lambda v: '\'' + v + '\'' if type(v) is str
           else v.strftime('\'%Y-%m-%d %H:%M:%S\'') if type(v) is datetime.datetime
           else str(v),
           existing_columns.values()))))


def select_all_camera(request):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('SELECT * FROM Camera')
    rows = cur.fetchall()
  return HttpResponse(map(lambda row: str(row) + '\n', rows))


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
  return HttpResponse(map(lambda row: str(row) + '\n', rows))


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
  return HttpResponse(map(lambda row: str(row) + '\n', rows))


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
      'photo.name AS photo_name, '
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
