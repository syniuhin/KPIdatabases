from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic.list import ListView
from django.utils import timezone

from .forms import PhotoForm
from .db import insert_into_photo_single, select_all_photo


def index(request):
  return HttpResponse('Hey!')


def new_photo(request):
  if request.method == 'POST':
    # create a form instance and populate it with data from the request:
    form = PhotoForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
      # process the data in form.cleaned_data as required
      insert_into_photo_single(form.cleaned_data)
      # redirect to a new URL:
      return HttpResponseRedirect('/lab02/photo/list/all/')
  else:
    form = PhotoForm()

  return render(request, 'lab02/photo_form.html', {'form': form})


class PhotoListView(ListView):
  template_name = 'lab02/photo_list.html'

  def get_context_data(self, **kwargs):
    context = super(PhotoListView, self).get_context_data(**kwargs)
    context['now'] = timezone.now()
    return context

  def get_queryset(self):
    return select_all_photo(None)
