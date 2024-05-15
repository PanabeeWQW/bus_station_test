from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name = 'home'),
    path('', include('django.contrib.auth.urls')),
    path('', include('users.urls'))
]