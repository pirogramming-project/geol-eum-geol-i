from django.urls import path
from .views import *

app_name = 'record'

urlpatterns = [
    path("", record_page, name="record_page"), # 걸음기록 시작 페이지
    path('ready/', ready_record, name='ready'), # 걸음기록 카운트다운 페이지
    path('stop/', record_stop, name='record_stop'), # 걸음기록 종료 페이지
    path("history/<str:date>/", record_history, name="record_history"), # 오늘걸음 페이지
    path("save_walk_record/", save_walk_record, name="save_walk_record"), # 걸음기록 저장
    path('delete/<int:pk>/', record_delete, name='record_delete'), # 걸음기록 삭제
    path('main_page/', main_view, name='main'), # 랜딩페이지 -> 메인
    path("check/<str:date>/", check_record, name="check_record"), # 기록 존재 여부 확인 페이지(김규일)
    path('ranking/', ranking_view, name='ranking'), # 랭킹 페이지 (김선주)
]