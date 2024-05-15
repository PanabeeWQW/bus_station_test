from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from users.models import User, Customer, Driver


class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        customer.first_name = self.cleaned_data.get('first_name')
        customer.last_name = self.cleaned_data.get('last_name')
        customer.phone_number = self.cleaned_data.get('phone_number')
        customer.save()
        return user


class DriverSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employee = True
        user.is_stuff = True
        user.save()
        employee = Driver.objects.create(user=user)
        employee.first_name = self.cleaned_data.get('first_name')
        employee.last_name = self.cleaned_data.get('last_name')
        employee.phone_number = self.cleaned_data.get('phone_number')
        employee.save()
        return user
