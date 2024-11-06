# student_offers/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Discount  # Corrected import for Discount

class DiscountSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search Discounts')

class CustomAuthenticationForm(AuthenticationForm):
    pass

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['interests']  # Adjust based on your actual fields in UserProfile

class DiscountSubmissionForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['title', 'description', 'website_url', 'company_name', 'discount_type',
                  'discount_percentage', 'discount_amount', 'category', 'tags', 'requirements',
                  'how_to_redeem', 'promo_code', 'valid_from', 'valid_until']
