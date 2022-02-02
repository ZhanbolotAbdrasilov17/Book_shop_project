from django.shortcuts import render
from .models import *

# Create your views here.

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/store.html', context)

def card(request):
    context = {}
    return render(request, 'store/card.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

