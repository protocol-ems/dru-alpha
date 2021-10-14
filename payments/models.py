from django.db import models
from django.db.models.deletion import CASCADE


# from company.models import Company

# Create your models here.


class Subscription(models.Model):
    # subscription_tier_choices = ((1, 'small'),
    #                              (2, 'medium'), (3, 'large'), (4, 'xl-large'), (5, 'custom'))
    # joined = models.DateTimeField(auto_now_add=True)
    # name = models.CharField(max_length=100, blank=True)
    # is_active = models.BooleanField(default=False)
    # phone = models.CharField(max_length=25, blank=True)
    # street_address = models.CharField(max_length=20, blank=True)
    # zipcode = models.CharField(max_length=20, blank=True)
    # state = models.CharField(max_length=20, blank=True)
    # city = models.CharField(max_length=100, blank=True)
    # stripe_cus_id = models.CharField(max_length=100, blank=True)
    # subsciption_tier = models.CharField(max_length=100, blank=True, choices=subscription_tier_choices)

    name = models.CharField(max_length=100)
    stripe_sub_id = models.CharField(max_length=100)
    price = models.IntegerField()
    user_max = models.IntegerField()
    custom_pricing = models.BooleanField(default=False)
    # company = models.ForeignKey(
    #     Company, related_name="Subscription", on_delete=CASCADE)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.name
