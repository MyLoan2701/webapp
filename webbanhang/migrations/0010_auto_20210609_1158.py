# Generated by Django 3.1.7 on 2021-06-09 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webbanhang', '0009_order_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_comment',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='product_rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=19),
        ),
    ]