# Generated by Django 5.0.6 on 2024-07-18 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(max_length=200, null=True),
        ),
    ]