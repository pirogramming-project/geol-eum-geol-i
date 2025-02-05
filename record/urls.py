from django.urls import path
from .views import *

app_name = 'record'

urlpatterns = [
    path("", record_page, name="record_page"), # 버튼페이지
    path("history/<str:date>/", record_history, name="record_history"),
    path("save_walk_record/", save_walk_record, name="save_walk_record"),  
    path('main_page/', main_view, name='main'),
    path('stop/', record_stop, name='record_stop'),
    path('daily/', daily_record, name='daily_record'),
    path('daily/', daily_record, name='daily_record'),
    path("check/<str:date>/", check_record, name="check_record"), # 기록 존재 여부 확인 페이지(김규일)
    path('ranking/', ranking_view, name='ranking'), # 랭킹 페이지 (김선주)
]