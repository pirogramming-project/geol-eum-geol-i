from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, user_id, email, password=None, nickname=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not user_id:
            raise ValueError('The User ID field must be set')
        if not nickname:
            raise ValueError('The Nickname field must be set')

        email = self.normalize_email(email)
        user = self.model(user_id=user_id, email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, email, password=None, nickname=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(user_id, email, password, nickname, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=False, null=False)
    nickname = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email', 'nickname']

    def __str__(self):
        return self.user_id
