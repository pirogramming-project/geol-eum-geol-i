from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # 사용자 목록에 표시할 필드 설정
    list_display = ('email', 'user_id', 'nickname', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')  # 필터링 옵션
    ordering = ('date_joined',)  # 정렬 기준
    search_fields = ('email', 'user_id', 'nickname')  # 검색 필드

    # 사용자 상세 화면에서 편집할 필드 설정
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('user_id', 'nickname')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    # 사용자 생성 화면에서 입력할 필드 설정
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_id', 'nickname', 'is_staff', 'is_active'),
        }),
    )

# CustomUser 모델 등록
admin.site.register(CustomUser, CustomUserAdmin)
