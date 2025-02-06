from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

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
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image_file']
