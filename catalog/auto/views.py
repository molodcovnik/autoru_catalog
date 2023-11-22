from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from django.urls import reverse_lazy
from django.views.generic import ListView

from .models import Mark, Model
from django.conf import settings
from .forms import ModelFilterForm
from .filters import ModelFilterSet


class ModelList(ListView):
    queryset = Model.objects.all()
    template_name = 'auto/index.html'
    context_object_name = 'models'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ModelFilterSet(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context

def index(request):
    name = request.GET.get('name')
    models = Model.objects.all()
    if name:
        models = models.filter(mark__name__icontains=name)
    context = {
        'form': ModelFilterForm(),
        'models': models
    }
    return render(request, "auto/index.html", context)


def download(filename=None):
    url = 'https://auto-export.s3.yandex.net/auto/price-list/catalog/cars.xml'
    r = requests.get(url)
    r.raise_for_status()
    current_dir = os.path.join(settings.BASE_DIR, 'media')

    if filename is None:
        filename = os.path.basename(urlparse(url).path)
    with open(os.path.join(current_dir, filename), "w") as file:
        file.write(r.text)

    print('file downloaded')


def clear_db():
    marks = Mark.objects.all()
    marks.delete()
    models = Model.objects.all()
    models.delete()
    print('db clear')


def parse(request):
    print('parse')
    clear_db()
    current_dir = os.path.join(settings.BASE_DIR, 'media')
    file_path = os.path.join(current_dir, 'cars.xml')

    if os.path.exists(file_path):
        os.remove(file_path)
        download()
    else:
        download()

    print(file_path)

    xmlData = None

    with open(file_path, 'r') as xmlFile:
        xmlData = xmlFile.read()

    xmlDecoded = xmlData

    xmlSoup = BeautifulSoup(xmlData, 'xml')

    marks = xmlSoup.find_all('mark')

    for mark in marks:
        mark_instance, created = Mark.objects.get_or_create(name=mark.get('name'))
        for model in mark.find_all('folder'):
            model_instance, created = Model.objects.get_or_create(name=model.get('name').partition(',')[0], mark=mark_instance)
            # print(f'{mark.get('name')}--{model.get('name').partition(',')[0]}')


    return HttpResponseRedirect(reverse_lazy('main_page'))