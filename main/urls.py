from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('summoner/get', views.get_summoner, name='get_summoner'),
    path('summoner/name=<str:name>', views.summoner, name='summoner')
]