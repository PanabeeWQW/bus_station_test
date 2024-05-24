from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from users.form import CustomerSignUpForm, DriverSignUpForm
from users.models import User, Customer, Driver
from main.models import Order, AdditionalPoints


def register(request):
    return render(request, 'registration/register.html')

def personal_account(request):
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            addpoint = AdditionalPoints.objects.filter(order__customer=customer)
        except Customer.DoesNotExist:
            customer = None
            addpoint = None

        try:
            driver = Driver.objects.get(user=request.user)
        except Driver.DoesNotExist:
            driver = None

        if customer:
            orders = Order.objects.filter(customer=customer)
            for order in orders:
                order.additional_points.all()

            # Print additional points for each order
            for order in orders:
                print(f"Order {order.id} additional points:", order.additional_points.all())

            context = {
                'addpoint': addpoint,
                'orders': orders,
                'customer': customer,
                'driver': driver,
            }
            return render(request, 'personal_data/personal_user_account.html', context)
        elif driver:
            return render(request, 'personal_data/personal_driver_account.html', {'driver': driver})
        elif request.user.is_superuser:
            return render(request, 'personal_data/personal_admin_account.html')
        else:
            raise Http404("Page not found")
    else:
        raise Http404("Page not found")


class customer_register(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/customer_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('personal_account')


class driver_register(CreateView):
    model = User
    form_class = DriverSignUpForm
    template_name = 'registration/driver_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('personal_account')
