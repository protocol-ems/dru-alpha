from rest_framework import serializers
from company.models import Company
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):

    company = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Company.objects.all(), required=False)

    class Meta:
        model = Subscription
        fields = ['id', 'name', 'stripe_sub_id',
                  'price', 'user_max', 'company']
