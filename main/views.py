from django.shortcuts import render, get_object_or_404, redirect
from .models import *

def index(request):
    return render(request, 'main/index.html')

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
    return render(request, 'main/bus_detail/bus_detail.html', {'bus': bus})

def order_with_driver(request, bus_id):
    if request.method == 'POST':
        # Обработка POST-запроса для создания заказа
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_point = request.POST.get('start_point')
        end_point = request.POST.get('end_point')
        payment_method = request.POST.get('payment_method')

        bus = get_object_or_404(Bus, id=bus_id)

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

        # Изменяем статус автобуса на "недоступен"
        bus.is_available = False
        bus.save()

        return redirect('order_detail', order_id=order.id)
    else:
        # Проверяем, аутентифицирован ли пользователь
        if request.user.is_authenticated:
            # Если пользователь аутентифицирован, отображаем форму заказа
            return render(request, 'main/order/order_with_driver.html', {'bus': get_object_or_404(Bus, id=bus_id), 'order': None})
        else:
            # Если пользователь не аутентифицирован, перенаправляем на страницу регистрации
            return redirect('register')  # Предполагается, что у вас есть URL с именем 'register'
