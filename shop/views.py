from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Feedback
from math import ceil


# Create your views here.
def index(request):
    products = Product.objects.values()
    n = len(products)
    all_product = []
    nslides = n // 4 + ceil((n / 4) - (n // 4))
    params = {'product': products, 'range': range(1, nslides), 'no_of_slides': nslides}
    cats = {item['category'] for item in products}
    for cat in cats:
        products = Product.objects.filter(category=cat)
        n = len(products)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        all_product.append([products, range(1, nslides), nslides])

    # all_product=[[products,range(1,nslides),nslides],[products,range(1,nslides),nslides]]
    params = {'allproduct': all_product}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    post=False
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        obj=Feedback(name=name,email=email,phone=phone,desc=desc)
        # print(name,email,phone,desc)
        obj.save()
        post=True
        
    params={'post':post}
    return render(request, 'shop/contact.html',params)


def tracker(request):
    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, 'shop/search.html')


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    params = {"product": product[0]}
    print(product[0].prod_id)
    print(product[0].prod_name)
    return render(request, 'shop/productView.html', params)


def checkout(request):
    return render(request, 'shop/checkout.html')
