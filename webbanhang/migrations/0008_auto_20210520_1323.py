# Generated by Django 3.1.7 on 2021-05-20 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webbanhang', '0007_rate_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='date_create',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='order',
            name='date_create',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='date_create',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='product',
            name='date_create',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='date_create',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='user',
            name='date_create',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
