from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from users.form import CustomerSignUpForm, DriverSignUpForm
from users.models import User


def register(request):
    return render(request, 'registration/register.html')

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