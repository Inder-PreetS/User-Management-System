from .models import Company
from django import forms

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'email', 'phoneNumber', 'dateOfBirth', 'address', 'images')

