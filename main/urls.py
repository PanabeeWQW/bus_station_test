from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name = 'home'),
    path('', include('django.contrib.auth.urls')),
    path('', include('users.urls')),
    path('catalog/', catalog, name='catalog'),
    path('bus_detail/<int:bus_id>/', bus_detail, name='bus_detail'),
]