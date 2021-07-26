from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
# Create your models here.


class Company(models.Model):
    joined = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['joined']

    def __str__(self):
        return self.name


class User(AbstractUser):
    company = models.ForeignKey(
        Company, related_name="users", on_delete=CASCADE, default=1)
    isEMT = models.BooleanField(default=True)
    isParamedic = models.BooleanField(default=False)
    isRN = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)


class Document(models.Model):

    # NEED TO ADD TAGLINE - OR SOMETIHNG THAT WOULD SHOW UP IN 'NEWS FEED'

    document_choices = (('1', 'Medicine'),
                        ('2', 'Procedure'), ('3', 'Protocol'))

    company = models.ForeignKey(
        Company, related_name="documents", on_delete=CASCADE)
    documentType = models.CharField(max_length=20, choices=document_choices)
    documentName = models.CharField(max_length=100)
    documentDetails = models.JSONField()
    modified = models.DateTimeField(auto_now=True)

    # isAdmin = serializers.ReadOnlyField(source="isAdmin.username")

    class Meta:
        ordering = ['modified']

    def __str__(self):
        return self.documentName


# I need to work on making the choices for each document standardized. I believe the below code will work.

# class DocumentDetailValues(models.Model):
#     document_choices = (('1', 'Medicine'),
#                         ('2', 'Procedure'), ('3', 'Protocol'))
#     tenantId = models.ForeignKey(
#         Company, related_name="documentDetails", on_delete=CASCADE)
#     documentType = models.CharField(max_length=20, choices=document_choices)
#     documentDetailName = models.CharField(max_length=100)

#     class Meta:
#         ordering = ['documentDetailName']

#     def __str__(self):
#         return self.documentDetailName
