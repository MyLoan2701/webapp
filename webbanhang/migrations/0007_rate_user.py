# Generated by Django 3.1.7 on 2021-04-25 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webbanhang', '0006_auto_20210425_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('avatar', models.ImageField(upload_to='customer')),
                ('status', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('rated', models.IntegerField(default=5)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webbanhang.user')),
                ('product_rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webbanhang.product')),
            ],
        ),
    ]
