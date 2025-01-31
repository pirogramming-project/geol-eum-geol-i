from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('', login_view, name='login'),
    path('success/', success_view, name='success'),
    path('logout/', logout_view, name='logout_view'),
    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),  # 이메일 인증 URL
    path('password_reset/', password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('naver/login/', naver_login, name='naver_login'),  # 네이버 로그인 버튼 클릭 시 호출
    path('naver/callback/', naver_callback, name='naver_callback'),  # 네이버에서 리디렉션
    path('google/login/', google_login, name='google_login'),  # 네이버 로그인 버튼 클릭 시 호출
    path('google/callback/', google_callback, name='google_callback'),  # 네이버에서 리디렉션
]