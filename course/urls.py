from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = 'course'

urlpatterns = [
    path('', course_list, name='course_list'),
    path("calendar/", calendar_view, name="calendar_view"),
    path("calendar/<int:year>/<int:month>/", calendar_view, name="calendar_view"),
    path("record/calendar/<int:year>/<int:month>/", calendar_data, name="calendar_data"),
    path("recommend/", course_form_view, name="course_form"),  # 추천 장소 등록 페이지
    path("submit-course/", submit_course, name="submit_course"),  # 데이터 저장 API
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('selectKeyWords/', select_keywords_view, name='select_keywords'),
    path('delete/<int:course_id>/', course_delete, name='course_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)