from django import forms
from .models import Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$')

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password1", "password2"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "middle_name", "last_name", "phone", "address", "email", "city", "amount"]