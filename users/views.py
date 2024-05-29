from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from .form import *
from users.models import User, Customer, Driver
from main.models import Order, AdditionalPoints, Bus


def register(request):
    return render(request, 'registration/register.html')


@login_required
def personal_account(request):
    user = request.user

    if user.is_superuser:
        return render(request, 'personal_data/personal_admin_account.html')

    if hasattr(user, 'customer'):
        return handle_customer_account(request, user.customer)

    if hasattr(user, 'driver'):
        return handle_driver_account(request, user.driver)

    raise Http404("Page not found")


def handle_customer_account(request, customer):
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('personal_account')
    else:
        form = ProfilePhotoForm(instance=customer)

    orders = Order.objects.filter(customer=customer)
    addpoint = AdditionalPoints.objects.all()

    context = {
        'addpoint': addpoint,
        'orders': orders,
        'customer': customer,
        'form': form,
    }
    return render(request, 'personal_data/personal_user_account.html', context)


def handle_driver_account(request, driver):
    if request.method == 'POST':
        status_form = UpdateDriverStatusForm(request.POST, instance=driver)
        if status_form.is_valid():
            status_form.save()
            return redirect('personal_account')
    else:
        status_form = UpdateDriverStatusForm(instance=driver)

    bus = Bus.objects.filter(driver=driver).first()
    orders = Order.objects.filter(driver=driver) if driver.status == 'online' else None

    context = {
        'driver': driver,
        'status_form': status_form,
        'orders': orders,
        'bus': bus,
    }
    return render(request, 'personal_data/personal_driver_account.html', context)


class CustomerRegister(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/customer_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('personal_account')


class DriverRegister(CreateView):
    model = User
    form_class = DriverSignUpForm
    template_name = 'registration/driver_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('personal_account')


@login_required
def attach_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    driver = get_object_or_404(Driver, user=request.user)

    if bus.driver is None and driver:
        bus.driver = driver
        bus.save()
        return redirect('personal_account')
    else:
        return redirect('catalog')

@login_required
def bus_dettach(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    driver = get_object_or_404(Driver, user=request.user)
    if bus.driver is not None and driver:
        bus.driver = None
        bus.save()
        return redirect('personal_account')
    else:
        return redirect('catalog')