from django.urls import path

from .views import index, parse, ModelList


urlpatterns = [
    path('', index, name='main_page'),
    path('second_variant/', ModelList.as_view(),),
    path('update/', parse),
    path('second_variant/update/', parse),
]