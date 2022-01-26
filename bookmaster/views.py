from django.shortcuts import render

# Create your views here.

def store(request):
    context = {}
    return render(request, 'store/store.html', context)

def card(request):
    context = {}
    return render(request, 'store/card.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

