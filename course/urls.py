from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    # path('', login_view, name='login'),
    # path('', calendar_view, name='calender'),
    path('', course_list, name='course_list'),
    path('calender', calendar_view, name='calender_view'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)