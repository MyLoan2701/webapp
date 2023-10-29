from django.db import models
from PIL import Image
from django.utils.text import slugify
from decimal import Decimal
# Create your models here.

#class Admin(models.Model)
	

class Category(models.Model):
	category_name = models.CharField(max_length=200)
	category_slug = models.SlugField(max_length=200)
	category_img = models.ImageField(upload_to='category', height_field=None, width_field=None, max_length=100)
	level = models.IntegerField(default = 0)
	date_create = models.DateTimeField(auto_now=True, null = False)
	def __str__(self):
		return self.category_name

	def save(self, *args, **kwargs):
		self.category_slug = slugify(self.category_name)
		super(Category, self).save(*args, **kwargs)



class Product(models.Model):
	product_name = models.CharField(max_length = 200)
	product_slug = models.SlugField(max_length=200)
	product_img = models.ImageField(upload_to='product', height_field=None, width_field=None, max_length=100)
	product_price = models.DecimalField(max_digits=19,decimal_places=2)
	product_amount = models.IntegerField(default = 100)
	product_sale = models.IntegerField(default = 0)
	product_detail = models.TextField()
	product_rate = models.DecimalField(max_digits=19,decimal_places=2, default=0.0)
	product_cmt = models.IntegerField(default = 0)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	date_create = models.DateTimeField(auto_now_add=True, null = False)

	def __str__(self):
		return self.product_name

	def save(self, *args, **kwargs):
		self.product_slug = slugify(self.product_name)
		super(Product, self).save(*args, **kwargs)
	def formatPrice(self):
		amount = self.product_price
		currency = "${:,.0f}".format(amount)
		return currency
	def formatSale(self):
		amount = self.product_price*(100-self.product_sale)/100
		currency = "${:,.0f}".format(amount)
		return currency


class User(models.Model):
	name = models.CharField(max_length = 200)
	email = models.CharField(max_length = 200)
	phone = models.CharField(max_length = 200)
	address = models.CharField(max_length = 200)
	password = models.CharField(max_length = 200)
	avatar = models.ImageField(upload_to='customer', height_field=None, width_field=None, max_length=100)
	status = models.CharField(max_length = 200)
	date_create = models.DateTimeField(auto_now=True, null = False)

	def __str__(self):
		return self.name


class Order(models.Model):
	order_customer = models.ForeignKey(User, on_delete=models.CASCADE)
	order_total = models.DecimalField(max_digits=18,decimal_places=3)
	order_name = models.CharField(max_length = 200)
	order_phone = models.CharField(max_length = 200)
	order_address = models.CharField(max_length = 200)
	order_status = models.CharField(max_length = 200)
	date_create = models.DateTimeField(auto_now=True, null = False)

	def __str__(self):
		return str(self.id)


class OrderDetail(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	qty = models.IntegerField(default = 0)
	price = models.DecimalField(max_digits=18,decimal_places=3)
	date_create = models.DateTimeField(auto_now=True, null = False)

	def save(self, *args, **kwargs):
		self.price = Decimal(self.qty)*self.product.product_price*((Decimal(100)-self.product.product_sale)/Decimal(100))
		self.product.product_amount = self.product.product_amount - self.qty
		self.product.save()
		super(OrderDetail, self).save(*args, **kwargs)
	def __str__(self):
		return str(self.id)

class Rate(models.Model):
	product_rate = models.ForeignKey(Product, on_delete=models.CASCADE)
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.TextField()
	rated = models.IntegerField(default = 5)
	date_create = models.DateTimeField(auto_now=True, null = False)
	def __str__(self):
		return str(self.id)
	def save(self, *args, **kwargs):
		self.product_rate.product_rate = self.product_rate.product_rate*self.product_rate.product_cmt/(self.product_rate.product_cmt+1)+Decimal(self.rated)/(self.product_rate.product_cmt+1)
		self.product_rate.product_cmt += 1
		self.product_rate.save()
		super(Rate, self).save(*args, **kwargs)