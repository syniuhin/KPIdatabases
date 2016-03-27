from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, \
  HttpResponseBadRequest, Http404

from django.core.urlresolvers import reverse
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.utils import timezone

from .forms import *
from .db import *


def index(request):
  return HttpResponse('Hey!')


def on_click_photo(request):
  if request.method == 'POST':
    if 'editbtn' in request.POST:
      url = reverse('edit_photo', kwargs={'photo_id':
                                            request.POST['tableradio']})
      return HttpResponseRedirect(url)
    if 'deletebtn' in request.POST:
      url = reverse('delete_photo', kwargs={'photo_id':
                                              request.POST['tableradio']})
      return HttpResponseRedirect(url)
  return HttpResponseBadRequest()


def new_photo(request):
  if request.method == 'POST':
    form = PhotoForm(request.POST)
    if form.is_valid():
      insert_into_photo_single(form.cleaned_data)
      return HttpResponseRedirect('/lab02/photo/list/all/')
  else:
    form = PhotoForm()

  return render(request, 'lab02/photo_form.html', {'form': form})


def edit_photo(request, photo_id):
  photo_id = int(photo_id)
  if request.method == 'GET':
    photo = select_photo_by_id(photo_id)
    form = PhotoForm(photo.__dict__)
    return render(request, 'lab02/photo_form.html', {'form': form})
  elif request.method == 'POST':
    form = PhotoForm(request.POST)
    if form.is_valid():
      photo_dict = form.cleaned_data
      photo_dict.update({'id': photo_id})
      edit_photo_single(photo_dict)
      return HttpResponseRedirect('/lab02/photo/list/all/')


def delete_photo(request, photo_id):
  photo_id = int(photo_id)
  delete_photo_by_id(photo_id)
  return HttpResponseRedirect('/lab02/photo/list/all/')


class PhotoListView(ListView):
  template_name = 'lab02/photo_list.html'

  def get_context_data(self, **kwargs):
    context = super(PhotoListView, self).get_context_data(**kwargs)
    context['now'] = timezone.now()
    return context

  def get_queryset(self):
    return select_all_photo(None)


class FormListView(FormMixin, ListView):
  def get(self, request, *args, **kwargs):
    # From ProcessFormMixin
    form_class = self.get_form_class()
    self.form = self.get_form(form_class)

    # From BaseListView
    self.object_list = self.get_queryset()
    allow_empty = self.get_allow_empty()
    if not allow_empty and len(self.object_list) == 0:
      raise Http404(u"Empty list and '%(class_name)s.allow_empty' is False."
                    % {'class_name': self.__class__.__name__})

    context = self.get_context_data(object_list=self.object_list,
                                    form=self.form)
    return self.render_to_response(context)

  def post(self, request):
    # From ProcessFormMixin
    self.form = self.get_form_class()(request.POST)
    if (self.form.is_valid()):
      self.cleaned_data = self.form.cleaned_data

    # From BaseListView
    self.object_list = self.get_queryset()
    allow_empty = self.get_allow_empty()
    if not allow_empty and len(self.object_list) == 0:
      raise Http404(u"Empty list and '%(class_name)s.allow_empty' is False."
                    % {'class_name': self.__class__.__name__})

    context = self.get_context_data(object_list=self.object_list,
                                    form=self.form)
    return self.render_to_response(context)


class FilterCameraListView(FormListView):
  form_class = CameraAttributesForm
  template_name = 'lab02/camera_list_filtered.html'

  def get_context_data(self, **kwargs):
    context = super(FilterCameraListView, self).get_context_data(**kwargs)
    context['now'] = timezone.now()
    return context

  def get_queryset(self):
    if hasattr(self, 'cleaned_data'):
      return select_filter_camera(self.cleaned_data)
    return select_all_camera()


class FilterLocationListView(FormListView):
  form_class = LocationAttributesForm
  template_name = 'lab02/location_list_filtered.html'

  def get_context_data(self, **kwargs):
    context = super(FilterLocationListView, self).get_context_data(**kwargs)
    context['now'] = timezone.now()
    return context

  def get_queryset(self):
    if hasattr(self, 'cleaned_data'):
      return select_filter_location(self.cleaned_data)
    return select_all_location()
