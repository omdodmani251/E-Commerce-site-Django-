from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from math import ceil


# Create your views here.
def index(request):
    products = Product.objects.all()
    n = len(products)
    nslides = n // 4 + ceil((n / 4) - (n // 4))
    params = {'product': products, 'range': range(1,nslides), 'no_of_slides': nslides}
    return render(request, 'shop/index.html',params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    items = Product.objects.all().values()
    items = {'items': items}
    # return HttpResponse('We are in Contact')
    return render(request, 'shop/temp.html', items)


def tracker(request):
    return HttpResponse('We are at tracker')


def search(request):
    return HttpResponse('We are at search')


def productView(request):
    return HttpResponse('We are at productView')


def checkout(request):
    return HttpResponse('We are at checkout')
