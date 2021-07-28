# Generated by Django 3.2.5 on 2021-07-28 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='documentType',
            field=models.CharField(choices=[(1, 'Medicine'), (2, 'Procedure'), (3, 'Protocol')], max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='employeeType',
            field=models.CharField(choices=[(1, 'EMT'), (2, 'Paramedic'), (3, 'RN'), (4, 'Admin'), (5, 'SuperUser')], default=1, max_length=20),
        ),
    ]
