# Generated by Django 3.2.5 on 2021-08-20 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0011_document_image_one'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.CharField(choices=[('1', 'Medicine'), ('2', 'Procedure'), ('3', 'Protocol')], max_length=20),
        ),
    ]
