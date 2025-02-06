from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'nickname', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken.")
        return email
    

# 마이페이지 프로필 수정
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nickname', 'profile_image_file']

    def clean_nickname(self):
        """
        닉네임을 한글 기준 8자로 제한.
        """
        nickname = self.cleaned_data.get("nickname")
        if len(nickname) > 8:
            raise ValidationError("닉네임: 최대 8자")
        return nickname

