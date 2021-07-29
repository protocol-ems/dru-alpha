from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Company(models.Model):
    joined = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=False)
    phone = models.CharField(max_length=25, blank=True)
    street_address = models.CharField(max_length=20, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['joined']

    def __str__(self):
        return self.name


class User(AbstractUser):

    title_choices = ((1, 'EMT'),
                     (2, 'Paramedic'), (3, 'RN'), (4, 'Admin'), (5, 'SuperUser'), (6, 'Accounting'))

    company = models.ForeignKey(
        Company, related_name="users", on_delete=CASCADE, default=1)
    employee_type = models.CharField(
        max_length=20, choices=title_choices, default=1)

    requested_company = models.ForeignKey(
        Company, related_name="requested_users", on_delete=CASCADE, default=1)


class Document(models.Model):

    # NEED TO ADD TAGLINE - OR SOMETIHNG THAT WOULD SHOW UP IN 'NEWS FEED'

    document_choices = ((1, 'Medicine'),
                        (2, 'Procedure'), (3, 'Protocol'))

    company = models.ForeignKey(
        Company, related_name="documents", on_delete=CASCADE)
    document_type = models.CharField(max_length=20, choices=document_choices)
    document_name = models.CharField(max_length=100)
    # I know that documentDetails is camel case and not like the others. However, I couldn't fix quickly. Will come back. Keep getting a weird error.
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
