from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from .form import *
from users.models import *
from main.models import Order, Bus, TripReview


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
    reviews = TripReview.objects.filter(order__in=orders)
    reviews_dict = {review.order.id: review for review in reviews}

    context = {
        'orders': orders,
        'customer': customer,
        'form': form,
        'reviews_dict': reviews_dict,
    }
    return render(request, 'personal_data/personal_user_account.html', context)


def handle_driver_account(request, driver):
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=driver)
        status_form = UpdateDriverStatusForm(request.POST, instance=driver)
        if status_form.is_valid():
            status_form.save()
            return redirect('personal_account')
    else:
        status_form = UpdateDriverStatusForm(instance=driver)

    # Получение всех автобусов, закрепленных за водителем
    buses = Bus.objects.filter(driver=driver)

    # Получение всех заказов, связанных с автобусами водителя
    orders = Order.objects.filter(bus__driver=driver) if driver.status == 'online' else None

    context = {
        'driver': driver,
        'status_form': status_form,
        'orders': orders,
        'buses': buses,
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


@staff_member_required
def review_drivers(request):
    drivers = Driver.objects.all()
    return render(request, 'main/admin/review_drivers.html', {'drivers': drivers})


@staff_member_required
def approve_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    driver.approval_status = 'approved'
    driver.is_approved = True
    driver.save()
    return redirect('review_drivers')


@staff_member_required
def reject_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason')
        driver.approval_status = 'rejected'
        driver.is_approved = False
        driver.rejection_reason = rejection_reason
        driver.save()
        # Отправка уведомления водителю об отклонении заявки
        # можно использовать систему уведомлений или отправку email
        return redirect('review_drivers')
    else:
        return render(request, 'main/admin/reject_driver.html', {'driver': driver})

@login_required
def attach_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    driver = get_object_or_404(Driver, user=request.user)

    if driver.approval_status != 'approved':
        messages.error(request, "Ваш статус не одобрен для выполнения этого действия")
        return redirect('catalog')

    if bus.driver is None and driver:
        bus.driver = driver
        bus.save()
        messages.success(request, "Автобус успешно закреплен")
        return redirect('personal_account')
    else:
        messages.error(request, "Не удалось закрепить автобус")
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


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        cancel_reason = request.POST.get('cancel_reason')
        if order.status != 'cancelled':
            order.status = 'cancelled'
            order.cancel_reason = cancel_reason
            order.is_active = False
            order.cancelled_by = 'customer'
            order.save()
            bus = order.bus
            if not bus.check_availability():
                bus.is_available = True
                bus.save()
        return redirect('personal_account')
    else:
        return HttpResponseBadRequest("Invalid request method")
