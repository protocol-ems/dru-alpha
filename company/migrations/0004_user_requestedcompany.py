# Generated by Django 3.2.5 on 2021-07-29 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20210728_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='requestedCompany',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='requested_users', to='company.company'),
        ),
    ]
