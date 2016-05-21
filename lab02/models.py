from django.db import models


class Camera(models.Model):
  name = models.CharField(max_length=64)
  year_created = models.DateField()
  version = models.IntegerField()


class Location(models.Model):
  name = models.CharField(max_length=64)
  lat = models.FloatField(max_length=10)
  lng = models.FloatField(max_length=10)
  accessible = models.BooleanField()


class Photographer(models.Model):
  name = models.CharField(max_length=64)
  level = models.IntegerField()
  email = models.EmailField(unique=True)

  cameras = models.ManyToManyField(Camera)
  locations = models.ManyToManyField(Location)


class Photo(models.Model):
  name = models.CharField(max_length=64)
  aperture = models.FloatField()
  iso = models.IntegerField()
  shot_time = models.DateTimeField()

  camera = models.ForeignKey(Camera)
  location = models.ForeignKey(Location)
  photographer = models.ForeignKey(Photographer)
