class Photo:
  def __init__(self, photo_id, name, photographer_name, camera_name,
               location_name, aperture, iso, shot_time, photographer_id=None,
               camera_id=None, location_id=None):
    self.id = photo_id
    self.name = name
    if photographer_id:
      self.photographer_id = photographer_id
    self.photographer_name = photographer_name
    if camera_id:
      self.camera_id = camera_id
    self.camera_name = camera_name
    if location_id:
      self.location_id = location_id
    self.location_name = location_name
    self.aperture = aperture
    self.iso = iso
    self.shot_time = shot_time


class Camera:
  def __init__(self, cam_id, name, year_created, version):
    self.id = cam_id
    self.name = name
    self.year_created = year_created
    self.version = version


class Location:
  def __init__(self, loc_id, name, lat, lng, accessible):
    self.id = loc_id
    self.name = name
    self.lat = lat
    self.lng = lng
    self.accessible = accessible


class Photographer:
  def __init__(self, ph_id, name, level, email):
    self.id = ph_id
    self.name = name
    self.level = level
    self.email = email
