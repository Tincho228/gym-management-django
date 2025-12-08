from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Membership, Routine, Exercise, Instructor, UserProfile


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
class NewMembershipForm(forms.Form):
    duration_options = (
            ("30", "One Month"),
            ("90", "Three Months"),
            ("365", "One year"))
    
    plan_type = forms.ChoiceField(
        choices= Membership.PLAN_CHOICES,
        label="Select Membership Plan"
    )
    duration_days = forms.ChoiceField(
        choices = duration_options,
        label="Select Plan Duration"
        )
class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['name', 'description', 'instructor', 'duration_minutes', 'clients']
        widgets = {
            'clients': forms.CheckboxSelectMultiple()
        }


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['routine', 'name', 'description', 'repetitions']


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['user', 'specialty', 'bio']

class AdminUserForm(forms.ModelForm):
    """Form to edit basic User fields from the admin dashboard."""

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class AdminUserProfileForm(forms.ModelForm):
    """Form to edit UserProfile (phone, is_admin)."""

    class Meta:
        model = UserProfile
        fields = ["phone", "is_admin"]