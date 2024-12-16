from django import forms
from .models import WasteListing
from .models import Profile
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class WasteListingForm(forms.ModelForm):
    class Meta:
        model = WasteListing
        fields = ['waste_type', 'description', 'quantity', 'location', 'availability_date']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user','user_type', 'organization_name', 'location']
        widgets = {
            'user': forms.HiddenInput(),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'organization_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }