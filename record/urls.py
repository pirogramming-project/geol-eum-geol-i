from django.urls import path
from .views import *

app_name = 'record'

urlpatterns = [
    path("", record_page, name="record_page"),
    path("save_walk_record/", save_walk_record, name="save_walk_record"),  
]