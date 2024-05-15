from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('customer_register', customer_register.as_view(), name = 'customer_register'),
    path('driver_register', driver_register.as_view(), name = 'driver_register')
]