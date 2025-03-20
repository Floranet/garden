# forms.py
from django import forms
from django.core.exceptions import ValidationError
import re
from .models import user_reg ,prof_reg # Import your model here

class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)  # To confirm the password

    class Meta:
        model = user_reg
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password', 'address']

    # Password validation
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not re.findall(r'\d', password):  # Check for at least one digit
            raise ValidationError('Password must contain at least one digit.')

        if not re.findall(r'[A-Z]', password):  # Check for at least one uppercase letter
            raise ValidationError('Password must contain at least one uppercase letter.')

        if len(password) < 8:  # Minimum length for password
            raise ValidationError('Password must be at least 8 characters long.')

        return password

    # Confirm password validation
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('The two password fields must match.')

        return confirm_password
