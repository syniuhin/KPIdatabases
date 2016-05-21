from django.conf.urls import url

from . import db, views
from .views import *

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^init/$', db.initiate_insert_into_tables, name="db_init"),

  url(r'^camera/list/filter/$', FilterCameraListView.as_view(),
      name='camera_list_filter'),

  url(r'^photographer/list/filter/$', FilterPhotographerListView.as_view(),
      name='photographer_list_filter'),

  url(r'^location/list/filter/$', FilterLocationListView.as_view(),
      name='location_list_filter'),

  url(r'^photo/clicked/?$', views.on_click_photo, name='on_click_photo'),
  url(r'^photo/create/$', views.PhotoController.create, name='new_photo'),
  url(r'^photo/edit/(?P<photo_id>[0-9]+)/$', views.PhotoController.update,
      name='edit_photo'),
  url(r'^photo/delete/(?P<photo_id>[0-9]+)/$', views.PhotoController.delete,
      name='delete_photo'),
  url(r'^photo/list/?$', PhotoListView.as_view(), name='photo_list'),
  url(r'^photo/list/filter/?$', FilterPhotoListView.as_view(),
      name='photo_list_filter'),
]
