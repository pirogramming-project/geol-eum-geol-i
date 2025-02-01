from django.urls import path
from .views import *

app_name = 'record'

urlpatterns = [
    path("", record_page, name="record_page"), # 버튼페이지
    path("history/<str:date>/", record_history, name="record_history"),
    path("save_walk_record/", save_walk_record, name="save_walk_record"),  
    path('main_page/', main_view, name='main'),
    path('start/', record_start, name='record_start'),
    path('stop/', record_stop, name='record_stop'),
    path('daily/', daily_record, name='daily_record'),
]