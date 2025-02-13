import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, nickname=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not nickname:
            raise ValueError('The Nickname field must be set')

        email = self.normalize_email(email)
        extra_fields.setdefault('user_id', str(uuid.uuid4())[:8])

        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, nickname=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, nickname, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=100, unique=True, editable=False, default=str(uuid.uuid4())[:8])
    email = models.EmailField(unique=True, blank=False, null=False)
    nickname = models.CharField(max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # 소셜 로그인용 프로필 이미지 URL
    profile_image_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True
    )

    # 직접 업로드하는 프로필 이미지 파일
    profile_image_file = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email

    @property
    def profile_image(self):
        """
        프로필 이미지 우선순위:
        1. 업로드된 이미지 파일
        2. 소셜 로그인 프로필 URL
        3. 기본 이미지
        """
        if self.profile_image_file:
            return self.profile_image_file.url
        elif self.profile_image_url:
            return self.profile_image_url
        return f"{settings.STATIC_URL}defaultimage/default-image.jpg"
    def clean(self):
        """
        닉네임을 한글 기준 8자로 제한.
        """
        super().clean()
        self.clean_nickname()

    def clean_nickname(self):
        """
        닉네임이 한글 기준 8자를 초과하면 오류 발생.
        """
        if len(self.nickname) > 8:
            raise ValidationError("닉네임은 한글 기준 최대 8자까지만 가능합니다.")
        

    def save(self, *args, **kwargs):
        """
        새로운 프로필 이미지가 업로드될 경우, 기존 이미지 파일을 자동 삭제.
        """
        try:
            old_user = CustomUser.objects.get(id=self.id)
            old_image = old_user.profile_image_file
        except CustomUser.DoesNotExist:
            old_image = None

        super().save(*args, **kwargs)

        # 기존 이미지 삭제 (새로운 이미지가 업로드되었고, 기존 이미지와 다를 경우)
        if old_image and self.profile_image_file and old_image != self.profile_image_file:
            if default_storage.exists(old_image.path):
                default_storage.delete(old_image.path)