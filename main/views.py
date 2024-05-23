from django.shortcuts import render, get_object_or_404
from .models import *

def index(request):
    return render(request, 'main/index.html')

def catalog(request):
    categories = Bus_Category.objects.all()
    brands = Bus_Brand.objects.all()
    selected_category_id = request.GET.get('category')
    selected_brand_id = request.GET.get('brand')

    buses = Bus.objects.filter(is_available=True)

    if selected_category_id:
        buses = buses.filter(category_id=selected_category_id)

    if selected_brand_id:
        buses = buses.filter(brand_id=selected_brand_id)

    return render(request, 'main/catalog/catalog.html', {'categories': categories, 'brands': brands, 'buses': buses})

def bus_detail(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    return render(request, 'main/bus_detail/bus_detail.html', {'bus': bus})