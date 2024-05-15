from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    driver_license = models.CharField(max_length=50)
    experience_years = models.IntegerField(validators=[MinValueValidator(0)])
    profile_photo = models.ImageField(upload_to='driver_profile_photos/', null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'
class Customer(models.Model):
    profile_photo = models.ImageField(upload_to='user_profile_photos/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Арендатор'
        verbose_name_plural = 'Арендаторы'