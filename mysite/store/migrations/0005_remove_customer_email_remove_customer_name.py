# Generated by Django 5.0.6 on 2024-07-19 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_shippingaddress_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='name',
        ),
    ]
