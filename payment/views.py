from .models import Order
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import json
import requests
import time
from .forms import RegisterForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect(reverse('login'))

    else:
        form = RegisterForm()

    return render(response, "payment/register.html", {"form": form})


@csrf_exempt
def gettoken(request):
    if request.method == 'POST':
        data = request.POST
        phone = data['phone']
        print(phone)
        if not Order.objects.filter(phone=phone).exists():
            return HttpResponse("NotFound")
        else:
            order = Order.objects.get(phone=phone)
            if not order.customerId:
                return HttpResponse("NotFound")
            else:
                customerid = order.customerId
                merchantrefnum = str(int(time.time()))
                url = "https://api.test.paysafe.com/paymenthub/v1/customers/" + customerid +"/singleusecustomertokens"
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic cHJpdmF0ZS03NzUxOkItcWEyLTAtNWYwMzFjZGQtMC0zMDJkMDIxNDQ5NmJlODQ3MzJhMDFmNjkwMjY4ZDNiOGViNzJlNWI4Y2NmOTRlMjIwMjE1MDA4NTkxMzExN2YyZTFhODUzMTUwNWVlOGNjZmM4ZTk4ZGYzY2YxNzQ4',
                    'Simulator': '"EXTERNAL"'
                }
                payload = {
                    "merchantRefNum": merchantrefnum,
                    "paymentTypes": ["CARD"]
                }
                payload = json.dumps(payload)
                response = requests.request("POST", url, headers=headers, data=payload)
                # print(response.json())
                data = response.json()
                return HttpResponse(data['singleUseCustomerToken'])


@login_required
def order_view(request):
    if request.method == "POST":
        data = request.POST
        # print(data)
        phone = data['phone']
        savecard = "NULL"
        if 'saveCard' in data:
            savecard = data['saveCard']

        url = "https://api.test.paysafe.com/paymenthub/v1/payments"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic cHJpdmF0ZS03NzUxOkItcWEyLTAtNWYwMzFjZGQtMC0zMDJkMDIxNDQ5NmJlODQ3MzJhMDFmNjkwMjY4ZDNiOGViNzJlNWI4Y2NmOTRlMjIwMjE1MDA4NTkxMzExN2YyZTFhODUzMTUwNWVlOGNjZmM4ZTk4ZGYzY2YxNzQ4',
            'Simulator': '"EXTERNAL"'
        }

        payload = {
            "merchantRefNum": "merchantRefNum" + str(int(time.time())),
            "amount": data['amount'],
            "currencyCode": "USD",
            "dupCheck": True,
            "settleWithAuth": False,
            "paymentHandleToken": data['paymentHandleToken'],
            "customerIp": "10.10.12.64",
            "description": "Magazine subscription"
        }
        if savecard == 'ADD':
            if not Order.objects.filter(phone=phone).exists():
                payload["merchantCustomerId"] = "mycustomer" + str(int(time.time()))
            else:
                order = Order.objects.get(phone=phone)
                payload["customerId"] = order.customerId

        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        r = response.json()
        print(r)
        if response.status_code == 201 and savecard == "ADD":
            if not Order.objects.filter(phone=phone).exists():
                order = Order.objects.create(user=request.user, phone=phone, customerId=r['customerId'], amount=r['amount'], multi_use_payment_token=r['multiUsePaymentHandleToken'])
                order.save()
        return HttpResponse(response.status_code)
    else:
        return render(request, 'payment/order.html')