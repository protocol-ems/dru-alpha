from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField, EmailField
from rest_framework import serializers
# Create your models here.


class Company(models.Model):
    joined = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=False)
    main_email = EmailField(max_length=200, default='test@test.com')
    ap_email = EmailField(max_length=200, default='test@test.com')
    phone = CharField(max_length=25, blank=True)
    street_address = CharField(max_length=20, blank=True)
    zipcode = CharField(max_length=20, blank=True)
    state = CharField(max_length=20, blank=True)
    city = CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['joined']

    def __str__(self):
        return self.name


class User(AbstractUser):

    title_choices = ((1, 'EMT'),
                     (2, 'Paramedic'), (3, 'RN'), (4, 'Admin'), (5, 'SuperUser'))

    company = models.ForeignKey(
        Company, related_name="users", on_delete=CASCADE, default=1)
    employeeType = models.CharField(
        max_length=20, choices=title_choices, default=1)


class Document(models.Model):

    # NEED TO ADD TAGLINE - OR SOMETIHNG THAT WOULD SHOW UP IN 'NEWS FEED'

    document_choices = ((1, 'Medicine'),
                        (2, 'Procedure'), (3, 'Protocol'))

    company = models.ForeignKey(
        Company, related_name="documents", on_delete=CASCADE)
    documentType = models.CharField(max_length=20, choices=document_choices)
    documentName = models.CharField(max_length=100)
    documentDetails = models.JSONField()
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['modified']

    def __str__(self):
        return self.documentName


# I need to work on making the choices for each document standardized. I believe the below code will work.

# class DocumentDetailValues(models.Model):
#     document_choices = (('1', 'Medicine'),
#                         ('2', 'Procedure'), ('3', 'Protocol'))
#     company = models.ForeignKey(
#         Company, related_name="documentDetails", on_delete=CASCADE)
#     documentType = models.CharField(max_length=20, choices=document_choices)
#     documentDetailName = models.CharField(max_length=100)

#     class Meta:
#         ordering = ['documentDetailName']

#     def __str__(self):
#         return self.documentDetailName
