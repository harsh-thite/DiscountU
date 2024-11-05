# student_offers/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile  # Assuming UserProfile model is defined in models.py

class DiscountSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search Discounts')

class CustomAuthenticationForm(AuthenticationForm):
    # No Meta class needed for AuthenticationForm
    pass

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['interests']  # Replace 'interests' with actual fields in UserProfile
