from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name = 'home'),
    path('', include('django.contrib.auth.urls')),
    path('', include('users.urls')),
    path('about/', about_us, name = 'about'),
    path('support/', support, name = 'support'),
    path('reviews/', reviews, name = 'reviews'),
    path('service/', service, name = 'service'),
    path('contact/', contact_us, name = 'contact'),
    path('license/', license_agreement, name = 'license'),
    path('catalog/', catalog, name='catalog'),
    path('bus_detail/<int:bus_id>/', bus_detail, name='bus_detail'),
    path('order_with_driver/<int:bus_id>/', order_with_driver, name='order_with_driver'),
    path('handle_order/<int:order_id>/', handle_order, name='handle_order'),
    path('carsharing/<int:bus_id>/', carsharing, name='carsharing'),
]