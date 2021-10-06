from django.conf.urls import url
from django.urls import path
from payments import views
from . import views
urlpatterns = [
    url(r'^test-payment/$', views.test_payment),
    url(r'^save-stripe-info/$', views.save_stripe_info),
    url(r'customer-info/$', views.customer_info),
    url(r'subscription-info/$', views.subscription_info),
    path('subscriptions/', views.SubscriptionList.as_view()),
    path('subscription-detail/<int:pk>/',
         views.SubscriptionDetail.as_view()),
    url(r'change-subscription/$', views.change_subscription),
    url(r'cancel-subscription/$', views.cancel_subscription),
    url(r'card-information/$', views.get_card_information),
    url(r'change-billing-information/$', views.change_billing_details)



]
