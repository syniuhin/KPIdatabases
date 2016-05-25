from django.http import HttpResponseRedirect
import MySQLdb as mdb

from models import *

mdb_args = ('localhost', 'root', '***REMOVED***', 'lab02db')


def initiate_insert_into_tables(request):
  insert_into_camera()
  insert_into_location()
  insert_into_photographer()
  # insert_into_photographer_camera()
  # insert_into_photographer_location()
  return HttpResponseRedirect('/')


def insert_into_camera():
  Camera.objects.all().delete()
  with open('/Users/infm/Coding/study/s4/db/lab02/input/camera.csv') as f:
    content = f.readlines()
    colnames = ['name', 'date_created', 'version']
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
      Photographer.objects.get(email=photographer_email).locations.add(
        Location.objects.get(name=location_name))


def create_photo_trigger():
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute("""
                CREATE TRIGGER ins_relations AFTER INSERT ON `lab02db`.`lab02_photo`
                FOR EACH ROW
                BEGIN
                  IF NEW.photographer_id IS NOT NULL THEN
                    SET @ph_cam = (SELECT id from lab02_photographer_cameras WHERE
                        photographer_id = NEW.photographer_id AND camera_id = NEW.camera_id);
                    IF @ph_cam IS NULL THEN
                      INSERT INTO `lab02db`.`lab02_photographer_cameras`(photographer_id,
                          camera_id) VALUES(NEW.photographer_id, NEW.camera_id);
                    END IF;
                      SET @ph_loc = (SELECT id from lab02_photographer_locations WHERE
                        photographer_id = NEW.photographer_id AND location_id = NEW.location_id);
                    IF @ph_loc IS NULL THEN
                      INSERT INTO `lab02db`.`lab02_photographer_locations`(photographer_id,
                          location_id) VALUES(NEW.photographer_id, NEW.location_id);
                    END IF;
                  END IF;
                END;
                """)


def drop_photo_trigger():
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('DROP TRIGGER IF EXISTS ins_relations;')


def is_trigger_enabled():
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute("""SHOW TRIGGERS LIKE 'lab02_photo';""")
    is_enabled = False if cur.fetchone() is None else True
  return is_enabled


def toggle_trigger():
  if is_trigger_enabled():
    drop_photo_trigger()
  else:
    create_photo_trigger()


def camera_usage(cam_id):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute('SELECT CAMERA_USAGE(%d);' % cam_id)
    return str(cur.fetchone()[0])


def change_event_schedule_interval(interval):
  con = mdb.connect(*mdb_args)
  with con:
    cur = con.cursor()
    cur.execute("""ALTER EVENT clear_photos
                        ON SCHEDULE %s
                          STARTS CURRENT_TIMESTAMP;""" % interval)
