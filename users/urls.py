from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('', login, name='login'),
    path('naver/login/', naver_login, name='naver_login'),  # 네이버 로그인 버튼 클릭 시 호출
    path('naver/callback/', naver_callback, name='naver_callback'),  # 네이버에서 리디렉션
    path('logout/', logout_view, name='logout_view'),
]