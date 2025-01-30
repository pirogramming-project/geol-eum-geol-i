from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'user_id', 'nickname', 'password1', 'password2']

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        if CustomUser.objects.filter(user_id=user_id).exists():
            raise forms.ValidationError("This user ID is already taken.")
        return user_id
