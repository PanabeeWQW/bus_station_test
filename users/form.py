from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from users.models import User, Customer, Driver
from django.core.exceptions import ValidationError
from datetime import date

def validate_age(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18 or age > 100:
        raise ValidationError('Вы должны быть старше 18 лет и младше 100 лет.')

class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    profile_photo = forms.ImageField(required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}), validators=[validate_age])

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'profile_photo', 'date_of_birth', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(
            user=user,
            phone_number=self.cleaned_data.get('phone_number'),
            profile_photo=self.cleaned_data.get('profile_photo'),
            date_of_birth=self.cleaned_data.get('date_of_birth'),
        )
        return user


class DriverSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    resume = forms.FileField(required=True)
    phone_number = forms.CharField(required=True)
    driver_license = forms.CharField(max_length=50, required=True)
    experience_years = forms.IntegerField(min_value=0, required=True)
    profile_photo = forms.ImageField(required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}), validators=[validate_age])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'driver_license', 'experience_years', 'profile_photo', 'date_of_birth', 'resume')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employee = True
        user.save()
        driver = Driver.objects.create(
            user=user,
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            phone_number=self.cleaned_data.get('phone_number'),
            resume=self.cleaned_data.get('resume'),
            driver_license=self.cleaned_data.get('driver_license'),
            experience_years=self.cleaned_data.get('experience_years'),
            profile_photo=self.cleaned_data.get('profile_photo'),
            date_of_birth=self.cleaned_data.get('date_of_birth'),
            is_approved = False
        )
        return user