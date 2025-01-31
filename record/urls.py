from django.urls import path
from .views import *

app_name = 'record'

urlpatterns = [
    path('main_page/', main_view, name='main'),
]