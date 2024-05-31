from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from users.models import User, Customer, Driver

class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    profile_photo = forms.ImageField(required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))

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
    phone_number = forms.CharField(required=True)
    driver_license = forms.CharField(max_length=50, required=True)
    experience_years = forms.IntegerField(min_value=0, required=True)
    profile_photo = forms.ImageField(required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'driver_license', 'experience_years', 'profile_photo', 'date_of_birth')

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
            driver_license=self.cleaned_data.get('driver_license'),
            experience_years=self.cleaned_data.get('experience_years'),
            profile_photo=self.cleaned_data.get('profile_photo'),
            date_of_birth=self.cleaned_data.get('date_of_birth')
        )
        return user
class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['profile_photo']

class UpdateDriverStatusForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['status']
