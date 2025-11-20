from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'MyAccountName123'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Must contain at least 8 characters and a combination of letters and numbers'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm your password'
        })
