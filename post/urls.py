from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = 'post'

urlpatterns = [
    path('', together_main, name='together_main'),
    path('together_detail/<int:post_id>/', together_detail, name='together_detail'),
    path("together_post/", together_post, name="together_post"), 
    path('together_comment/<int:post_id>/', together_comment, name='together_comment'),
    path('together_delete/<int:post_id>/', together_delete, name='together_delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)