from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from stripe.api_resources import payment_method
from company.serializer import CompanySerializer
from company.models import Company
from .models import Subscription
from .serializer import SubscriptionSerializer
from rest_framework import generics, permissions, status

import stripe

# Create your views here.

stripe.api_key = settings.STRIPE_TEST_KEY


@api_view(['POST'])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='usd',
        payment_method_types=['card'],
        receipt_email='test@example.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)


@csrf_exempt
@api_view(["POST"])
def save_stripe_info(request):
    data = request.data
    email = data['email']
    payment_method_id = data['payment_method_id']
    # subscription_type_id = data['subscription_type']
    billing_details = data['billing_details']
    city = billing_details['address']['city']
    line1 = billing_details['address']['line1']
    line2 = billing_details['address']['line2']
    postal_code = billing_details['address']['postal_code']
    state = billing_details['address']['state']
    phone = data['billing_details']['phone']
    name = data['billing_details']['name']

    company = Company.objects.get(id=data['company'])

    subscription = Subscription.objects.get(id=data['subscription_type_id'])
    subscription_seralizer = SubscriptionSerializer(subscription)

    subscription_price_id = subscription_seralizer.data['stripe_sub_id']
    print(subscription_price_id)
    # company = CompanySerializer(data['company'])

    # queryset = Company.objects.all()
    # serializer_class = CompanySerializer

    extra_msg = ''  # add new variable to response message
    customer_data = stripe.Customer.list(email=email).data

    # creating customer
    if len(customer_data) == 0:
        customer = stripe.Customer.create(
            email=email, payment_method=payment_method_id, invoice_settings={'default_payment_method': payment_method_id}, phone=phone, name=name, address={'city': city, 'line1': line1, 'line2': line2, 'postal_code': postal_code, 'state': state}, shipping={'name': name, 'phone': phone, 'address': {'city': city, 'line1': line1, 'line2': line2, 'postal_code': postal_code, 'state': state}})
    else:
        customer = customer_data[0]
        extra_msg = "Customer already existed."

    # if subscription_type == 'small':
    #     subscription_price_id = 'price_1JYZIoJEjyoAE1rtapKqdLLk'
    # if subscription_type == 'medium':
    #     subscription_price_id = 'price_1JYayYJEjyoAE1rt0h7PMkdh'
    # if subscription_type == 'large':
    #     subscription_price_id = 'price_1JYayYJEjyoAE1rttlK4BUPQ'
    # if subscription_type == 'xl-large':
    #     subscription_price_id = 'price_1JZLVKJEjyoAE1rtc18jUBGV'

    # This will create a 1 time payment.
    # stripe.PaymentIntent.create(
    #     customer=customer,
    #     payment_method=payment_method_id,
    #     currency='usd',
    #     amount=1500,
    #     confirm=True
    # )

    subscription_info = stripe.Subscription.create(
        customer=customer,
        items=[
            {
                'price': subscription_price_id  # here paste your price id
            }
        ]
    )
    # this gives us the subscription id. May be useful -
    # print(subscription_info['id'])
    company.stripe_cus_id = customer['id']
    company.is_active = True
    company.subscription = subscription
    company.stripe_sub_id = subscription_info['id']
    company.save()

    return Response(status=status.HTTP_200_OK,
                    data={'message': 'Success', 'customer_id': customer.id, 'extra_msg': extra_msg, 'sub_info': subscription_info
                          })
    # return Response(status=status.HTTP_200_OK,
    #                 data={'message': 'Success', 'email': email, 'phone': phone, 'name': name, 'billing_details': billing_details
    #                       })


@api_view(["POST"])
def customer_info(request):
    data = request.data
    customer_id = data['customer_id']
    # print(data)

    customer_info = stripe.Customer.retrieve(id=customer_id)

    return Response(status=status.HTTP_200_OK, data={'customer_info': customer_info})


@api_view(["POST"])
def subscription_info(request):
    data = request.data
    subscription_id = data['subscription_id']

    subscription_info = stripe.Subscription.retrieve(id=subscription_id)

    return Response(status=status.HTTP_200_OK, data={'subscription_info': subscription_info})


@api_view(["POST"])
def change_subscription(request):
    data = request.data
    subscription_type_id = data['subscription_type_id']
    stripe_cus_id = data['stripe_cus_id']
    stripe_sub_id = data['stripe_sub_id']
    subscription = Subscription.objects.get(id=subscription_type_id)
    subscription_seralizer = SubscriptionSerializer(subscription)
    subscription_price_id = subscription_seralizer.data['stripe_sub_id']

    customer_info = stripe.Customer.retrieve(id=stripe_cus_id)

    subscription_info = stripe.Subscription.retrieve(id=stripe_sub_id)

    new_subscription_info = stripe.Subscription.modify(subscription_info.id, items=[
        {
            'id': subscription_info['items']['data'][0].id,
            'price': subscription_price_id
        }
    ])

    company = Company.objects.get(id=data['company'])

    company.subscription = subscription

    company.save()

    return Response(status=status.HTTP_200_OK, data={'subscription_info': subscription_price_id})


class SubscriptionList(generics.ListAPIView):
    # This is used on the front end to see Our Generic Pricing. We filter out any custom pricing to avoid exposing it
    queryset = Subscription.objects.all().filter(custom_pricing__in=[False])
    serializer_class = SubscriptionSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]


class CustomSubscriptionList(generics.ListAPIView):
    # End point to see all custom subscriptions.
    queryset = Subscription.objects.all().filter(custom_pricing__in=[True])
    serializer_class = SubscriptionSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]


class SubscriptionDetail(generics.RetrieveAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(["POST"])
def cancel_subscription(request):
    data = request.data
    stripe_sub_id = data['stripe_sub_id']
    company = Company.objects.get(id=data['company'])

    company.is_active = False
    company.save()

    stripe.Subscription.delete(stripe_sub_id)
    return Response(status=status.HTTP_200_OK, data={})


@api_view(["POST"])
def get_card_information(request):
    data = request.data
    payment_method = data["payment_method"]

    stripe_payment_information = stripe.PaymentMethod.retrieve(payment_method)

    return Response(status=status.HTTP_200_OK, data={'payment_information': stripe_payment_information})


@api_view(["POST"])
def change_billing_details(request):
    data = request.data
    payment_method_id = data['payment_method_id']
    customer = data['customer']
    email = data['email']
    billing_details = data['billing_details']
    city = billing_details['address']['city']
    line1 = billing_details['address']['line1']
    line2 = billing_details['address']['line2']
    postal_code = billing_details['address']['postal_code']
    state = billing_details['address']['state']
    phone = data['billing_details']['phone']
    name = data['billing_details']['name']

    stripe.PaymentMethod.attach(payment_method_id, customer=customer)
    modified_customer = stripe.Customer.modify(customer,  invoice_settings={
        'default_payment_method': payment_method_id}, email=email, phone=phone, name=name, address={'city': city, 'line1': line1, 'line2': line2, 'postal_code': postal_code, 'state': state}, shipping={'name': name, 'phone': phone, 'address': {'city': city, 'line1': line1, 'line2': line2, 'postal_code': postal_code, 'state': state}})

    # stripe.Subscription.modify()

    return Response(status=status.HTTP_200_OK, data={'customer_info': modified_customer})
