# Generated by Django 3.2.5 on 2021-09-14 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
        ('company', '0015_company_stripe_cus_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='subsciption',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to='payments.subscription'),
        ),
    ]