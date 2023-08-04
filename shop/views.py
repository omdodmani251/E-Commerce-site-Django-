from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Feedback, Order, Order_tracker
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from .paytm import PaytmChecksum
import requests


# Create your views here.
def index(request):
    products = Product.objects.values()
    n = len(products)
    all_product = []
    nslides = n // 4 + ceil((n / 4) - (n // 4))
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
        obj.save()
        post = True

    params = {'post': post}
    post = False
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
                    response = json.dumps({'status':'success','updates':update, 'itemsJson':order[0].items_info}, default=str)

                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"empty"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')


def searchProduct(query, item):
    if query:
        if query.lower() in item['prod_name'].lower() or query.lower() in item['prod_desc'].lower() or query.lower() in \
                item['category'].lower():
            return True
    return False


def search(request):
    query = request.GET.get('search')
    products = Product.objects.values()
    matched_products = []

    for product in products:
        if searchProduct(query, product):
            matched_products.append(product)

    n = len(matched_products)
    all_product = []
    nslides = n // 4 + ceil((n / 4) - (n // 4))
    all_product.append([matched_products, range(1, nslides), nslides])
    params = {'allproduct': all_product, 'query': query, 'notfound': ''}

    if len(matched_products) == 0 or len(query) < 3:
        params = {'allproduct': all_product, 'query': query, 'notfound': 'True'}

    return render(request, 'shop/search.html', params)


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    params = {"product": product[0]}
    print(product[0].prod_id)
    print(product[0].prod_name)
    return render(request, 'shop/productView.html', params)


def checkout(request):
    if request.method == 'POST':
        items_info = request.POST.get('items_info', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Order(items_info=items_info, name=name, email=email, address1=address1, address2=address2, city=city,
                      state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()

        trackerobj = Order_tracker(order_id=order.ord_id, track_desc='Your has been placed')
        trackerobj.save()

        return render(request, 'shop/checkout.html', {'placed': True, 'id': order.ord_id})
        
        paytmParams = dict()

        paytmParams["body"] = {
            "requestType": "Payment",
            "mid": "YOUR_MID_HERE",
            "websiteName": "My_Awesome_Shop",
            "orderId": str(order.ord_id),
            "callbackUrl": "http://127.0.0.1:8000/shop/initialize",
            "txnAmount": {
                "value": str(order.amount),
                "currency": "INR",
            },
            "userInfo": {
                "custId": "CUST_001",
            },
        }

        # Generate checksum by parameters we have in body
        # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
        checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), "YOUR_MERCHANT_KEY")

        paytmParams["head"] = {
            "signature": checksum
        }

        post_data = json.dumps(paytmParams)
        url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"

        # for Production
        # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
        response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
        print(response)

    return render(request, 'shop/checkout.html')


@csrf_exempt
def initialize(request):
    return HttpResponse('DONE')


@csrf_exempt
def handlerequest(request):
    pass
