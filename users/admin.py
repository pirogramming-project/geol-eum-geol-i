from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # 사용자 목록에 표시할 필드 설정
    list_display = ('email', 'nickname', 'profile_image_url', 'profile_image_file', 'is_active', 'is_staff', 'date_joined')  # ✅ user_id 제거
    list_filter = ('is_staff', 'is_active', 'date_joined')  # 필터링 옵션
    ordering = ('date_joined',)  # 정렬 기준
    search_fields = ('email', 'nickname')  # ✅ user_id 제거

    # 사용자 상세 화면에서 편집할 필드 설정
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('nickname', 'profile_image_url', 'profile_image_file')}),  # ✅ user_id 제거
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),  
    )

    readonly_fields = ('user_id', 'date_joined')  # ✅ user_id를 readonly 필드로 설정

    # 사용자 생성 화면에서 입력할 필드 설정
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'nickname', 'is_staff', 'is_active'),  # ✅ user_id 제거
        }),
    )

# CustomUser 모델 등록
admin.site.register(CustomUser, CustomUserAdmin)
