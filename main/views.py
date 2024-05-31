from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import datetime
from .forms import CancelOrderForm
from .models import *


def index(request):
    return render(request, 'main/index.html')

def about_us(request):
    return render(request, 'main/about/about_us.html')

def contact_us(request):
    return render(request, 'main/contacts/contacts.html')

def support(request):
    return render(request, 'main/support/support.html')

def reviews(request):
    return render(request, 'main/reviews/reviews.html')

def service(request):
    return render(request, 'main/about/service.html')

def license_agreement(request):
    return render(request, 'main/about/license_agreement.html')

def catalog(request):
    categories = Bus_Category.objects.all()
    brands = Bus_Brand.objects.all()
    selected_category_id = request.GET.get('category')
    selected_brand_id = request.GET.get('brand')

    buses = Bus.objects.all()

    if selected_category_id:
        buses = buses.filter(category_id=selected_category_id)

    if selected_brand_id:
        buses = buses.filter(brand_id=selected_brand_id)

    return render(request, 'main/catalog/catalog.html', {'categories': categories, 'brands': brands, 'buses': buses})

def bus_detail(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    order = Order.objects.filter(bus=bus).last()
    context = {'bus': bus, 'order': order}
    return render(request, 'main/bus_detail/bus_detail.html', context)

def order_with_driver(request, bus_id):
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M')

        start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        if start_date <= timezone.now() or end_date <= timezone.now() or start_date >= end_date:
            return HttpResponseBadRequest("Выберите корректные даты для заказа.")

        start_point = request.POST.get('start_point')
        end_point = request.POST.get('end_point')
        payment_method = request.POST.get('payment_method')

        bus = get_object_or_404(Bus, id=bus_id)

        if not Order.objects.filter(bus=bus, start_date__lte=end_date, end_date__gte=start_date, is_active=True, status='confirmed').exists():
            order = Order.objects.create(
                customer=request.user.customer,
                bus=bus,
                driver_needed=True,
                start_date=start_date,
                end_date=end_date,
                start_point=start_point,
                end_point=end_point,
                payment_method=payment_method,
                status='pending'
            )
            additional_points = request.POST.getlist('additional-point')
            for point in additional_points:
                AdditionalPoints.objects.create(order=order, point=point)

            bus.is_available = False
            bus.save()

            return redirect('personal_account')
        else:
            return HttpResponseBadRequest("Автобус уже забронирован на выбранные даты.")
    else:
        if request.user.is_authenticated:
            return render(request, 'main/order/order_with_driver.html',
                          {'bus': get_object_or_404(Bus, id=bus_id), 'order': None})
        else:
            return redirect('register')

@login_required
def handle_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    driver = get_object_or_404(Driver, user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            order.status = 'confirmed'
            order.save()
            return redirect('personal_account')
        elif action == 'reject':
            form = CancelOrderForm(request.POST, instance=order)
            if form.is_valid():
                if Driver.objects.exclude(id=driver.id).exists():
                    order.status = 'cancelled'
                    order.is_active = False
                    order.cancelled_by = 'driver'
                    order.save()
                    bus = order.bus
                    if not bus.check_availability():
                        bus.is_available = True
                        bus.save()
                    return redirect('personal_account')
                else:
                    return HttpResponseForbidden("No other drivers available to reassign the order.")
        else:
            form = CancelOrderForm(instance=order)
        context = {
            'order': order,
            'form': form,
        }
        return render(request, '', context)

    form = CancelOrderForm(instance=order)
    context = {
        'order': order,
        'form': form,
    }
    return render(request, '', context)

def carsharing(request, bus_id):
    return render(request, 'main/order/carsharing.html')