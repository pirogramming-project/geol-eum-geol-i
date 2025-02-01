from django.urls import path
from .views import *

app_name = 'record'

urlpatterns = [
    path('main_page/', main_view, name='main'),
    path('start/', record_start, name='record_start'),
    path('stop/', record_stop, name='record_stop'),
    path('daily/', daily_record, name='daily_record'),
]