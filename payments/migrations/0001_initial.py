# Generated by Django 3.2.5 on 2021-09-14 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('stripe_sub_id', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('user_max', models.IntegerField()),
            ],
            options={
                'ordering': ['price'],
            },
        ),
    ]
