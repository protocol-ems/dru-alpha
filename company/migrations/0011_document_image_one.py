# Generated by Django 3.2.5 on 2021-08-20 16:47

import company.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_document_flow_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='image_one',
            field=models.ImageField(blank=True, null=True, upload_to=company.models.Document.upload_path),
        ),
    ]
