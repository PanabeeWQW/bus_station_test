from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from users.form import CustomerSignUpForm, DriverSignUpForm
from users.models import User, Customer, Driver
from django.shortcuts import get_object_or_404


def register(request):
    return render(request, 'registration/register.html')

def personal_account(request):
    customer = None
    driver = None
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        pass
    try:
        driver = Driver.objects.get(user=request.user)
    except Driver.DoesNotExist:
        pass

    context = {
        'customer': customer,
        'driver': driver,
    }
    if customer is not None:
        return render(request, 'personal_data/personal_user_account.html', context)
    if driver is not None:
        return render(request, 'personal_data/personal_driver_account.html', context)
    if User is not None:
        return render(request, 'personal_data/personal_admin_account.html', context)


class customer_register(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/customer_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class driver_register(CreateView):
    model = User
    form_class = DriverSignUpForm
    template_name = 'registration/driver_register.html'
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')