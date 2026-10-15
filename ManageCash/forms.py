from django import forms
from django.contrib.auth.models import User
from django.db.models import *
from .models import AddCash, Expense

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password do not match")
        return cleaned_data


class AddCashForm(forms.ModelForm):
    class Meta:
        model = AddCash
        fields = ['source', 'datetime', 'amount', 'description']
        widgets = {'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'})}

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'datetime']
        widgets = {'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'})}