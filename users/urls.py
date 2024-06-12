from django.urls import path
from .views import register, CustomerRegister, DriverRegister, personal_account, attach_bus, bus_dettach, cancel_order, review_drivers, approve_driver, reject_driver

urlpatterns = [
    path('register/', register, name='register'),
    path('customer_register/', CustomerRegister.as_view(), name='customer_register'),
    path('driver_register/', DriverRegister.as_view(), name='driver_register'),
    path('personal_account/', personal_account, name='personal_account'),
    path('attach_bus/<int:bus_id>/', attach_bus, name='attach_bus'),
    path('bus_dettach/<int:bus_id>/', bus_dettach, name='bus_dettach'),
    path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order'),
    path('review_drivers/', review_drivers, name='review_drivers'),
    path('approve_driver/<int:driver_id>/', approve_driver, name='approve_driver'),
    path('reject_driver/<int:driver_id>/', reject_driver, name='reject_driver'),
]
