from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', course_list, name='course_list'),
    path('calendar/', calendar_view, name='calendar_view'),
    path("recommend/", course_form_view, name="course_form"),  # 코스 추천 페이지
    path("submit-course/", submit_course, name="submit_course"),  # 데이터 저장 API
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)