from django.contrib import admin
from .models import Course, Keyword, CourseKeyword

# Register your models here.
admin.site.register(Course)
admin.site.register(Keyword)
admin.site.register(CourseKeyword)