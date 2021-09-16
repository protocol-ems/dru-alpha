# Generated by Django 3.2.5 on 2021-09-06 16:19

import company.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0011_alter_document_document_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'ordering': ['-modified']},
        ),
        migrations.CreateModel(
            name='DocumentImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=company.models.DocumentImage.upload_path)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_images', to='company.company')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_images', to='company.document')),
            ],
        ),
    ]