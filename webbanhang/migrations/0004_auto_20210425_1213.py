# Generated by Django 3.1.7 on 2021-04-25 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webbanhang', '0003_auto_20210425_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_img',
            field=models.ImageField(upload_to='category'),
        ),
    ]
