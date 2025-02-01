from django import forms
from .models import Detail

class RecordUpdateTestForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = ["image", "memo"]
        
        