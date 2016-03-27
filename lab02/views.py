from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, \
  HttpResponseBadRequest

from django.core.urlresolvers import reverse
from django.views.generic.list import ListView
from django.utils import timezone

from .forms import PhotoForm
from .db import edit_photo_single, delete_photo_by_id, insert_into_photo_single, \
  select_all_photo, select_photo_by_id


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
    print photo.__dict__
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
