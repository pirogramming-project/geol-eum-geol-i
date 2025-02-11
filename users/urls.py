from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('', landing_view, name='landing'),
    path('main/', main_beforeLogin, name='main_beforeLogin'),
    path('login/', login_view, name='login'),
    path('success/', success_view, name='success'),
    path('logout/', logout_view, name='logout_view'),
    path('signup/', signup, name='signup'),
    path("delete_account/", delete_account, name="delete_account"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),  # 이메일 인증 URL
    path('password_reset/', password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('naver/login/', naver_login, name='naver_login'),  # 네이버 로그인 버튼 클릭 시 호출
    path('naver/callback/', naver_callback, name='naver_callback'),  # 네이버에서 리디렉션
    path('google/login/', google_login, name='google_login'),  # 네이버 로그인 버튼 클릭 시 호출
    path('google/callback/', google_callback, name='google_callback'),  # 네이버에서 리디렉션
    path('mypage/', mypage_view, name='mypage_view'),
    path('terms-of-service/', terms_of_service, name="terms-of-service"),
    path('privacy-policy/', privacy_policy, name="privacy_policy"),
    path('aboutus/', aboutus_view, name='aboutus_view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)