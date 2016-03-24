class Photo:
  def __init__(self, photo_id, photo_name, photographer_name, camera_name,
               location_name, aperture, iso, shot_time):
    self.id = photo_id
    self.photo_name = photo_name
    self.photographer_name = photographer_name
    self.camera_name = camera_name
    self.location_name = location_name
    self.aperture = aperture
    self.iso = iso
    self.shot_time = shot_time
