from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Feedback, Order, Order_tracker
from math import ceil
import json

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
    post = False
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', 0)
        desc = request.POST.get('desc', '')
        obj = Feedback(name=name, email=email, phone=phone, desc=desc)
        # print(name,email,phone,desc)
        obj.save()
        post = True

    params = {'post': post}
    return render(request, 'shop/contact.html', params)


def tracker(request):
    if request.method == 'POST':
        order_id = request.POST.get('orderid', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(ord_id=order_id, email=email)

            if (len(order) > 0):
                # print('yes len > 0')
                updates = Order_tracker.objects.filter(order_id=order_id)
                # print(updates)
                update = []
                for i in updates:
                    update.append({'text': i.track_desc, 'time': i.timestamp})
                    response = json.dumps(update, default=str)

                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

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
    if request.method == 'POST':
        # print('yes',request.POST.get('items_info'))
        items_info = request.POST.get('items_info', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_info=items_info, name=name, email=email, address1=address1, address2=address2, city=city,
                      state=state, zip_code=zip_code, phone=phone)
        order.save()
        tracker = Order_tracker(order_id=order.ord_id, track_desc='Your has been placed')
        tracker.save()
        return render(request, 'shop/checkout.html', {'placed': True, 'id': order.ord_id})
    return render(request, 'shop/checkout.html')
