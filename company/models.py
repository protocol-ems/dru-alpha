from django.db import models
from django.db.models.deletion import SET_NULL, CASCADE, SET_DEFAULT
from django.contrib.auth.models import AbstractUser
from payments.models import Subscription
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
    stripe_cus_id = models.CharField(max_length=100, blank=True)
    stripe_sub_id = models.CharField(max_length=100, blank=True)
    subscription = models.ForeignKey(
        Subscription, related_name="company", on_delete=SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['joined']

    def __str__(self):
        return self.name


class User(AbstractUser):

    title_choices = ((1, 'EMT'),
                     (2, 'Paramedic'), (3, 'RN'), (4, 'Admin'), (5, 'SuperUser'), (6, 'Accounting'))

    company = models.ForeignKey(
        Company, related_name="users", on_delete=SET_DEFAULT, default=1)
    # make this an integrefield
    # need to rework the employee_type serializer to make it return the choices field not the integer
    employee_type = models.CharField(
        max_length=20, choices=title_choices, default=1)

    requested_company = models.ForeignKey(
        Company, related_name="requested_users", on_delete=SET_DEFAULT, default=1)


class Document(models.Model):
    # Hiding the imageField for now. Will do a different way.
    # images need to be deleted on cascade. I don't believe this is true at the moment 8/23
    # def upload_path(instance, filename):
    #     return '/'.join(['images', str(instance.company), str(instance.document_name), filename])
    # image_one = models.ImageField(blank=True, null=True, upload_to=upload_path)
    def table_default():
        return {"columns": [], "rows": [], "table_description": ""}

    def flow_default():
        return {"flow_data": []}

    # NEED TO ADD TAGLINE - OR SOMETIHNG THAT WOULD SHOW UP IN 'NEWS FEED'

    document_choices = (("1", 'Medicine'),
                        ("2", 'Procedure'), ("3", 'Protocol'))

    company = models.ForeignKey(
        Company, related_name="documents", on_delete=CASCADE)
    document_type = models.CharField(max_length=20, choices=document_choices)
    document_name = models.CharField(max_length=100)
    # I know that documentDetails is camelCase and not like the others. However, I couldn't fix quickly. Will come back. Keep getting a weird error.
    documentDetails = models.JSONField()
    table_data = models.JSONField(default=table_default)
    flow_data = models.JSONField(default=flow_default)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified']

    def __str__(self):
        return self.document_name


class DocumentHeader(models.Model):
    document_choices = ((1, 'Medicine'),
                        (2, 'Procedure'), (3, 'Protocol'))
    company = models.ForeignKey(
        Company, related_name="document_headers", on_delete=CASCADE)
    document_type = models.CharField(max_length=20, choices=document_choices)
    document_detail_name = models.CharField(max_length=100)
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.document_detail_name


class DocumentImage(models.Model):

    def upload_path(instance, filename):
        return '/'.join(['images', str(instance.company), str(instance.document), filename])

    image = models.ImageField(upload_to=upload_path)

    document = models.ForeignKey(
        Document, related_name="document_images", on_delete=CASCADE)

    company = models.ForeignKey(
        Company, related_name="company_images", on_delete=CASCADE, default=1)
