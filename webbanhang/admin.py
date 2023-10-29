from django.contrib import admin

from .models import Category, Product, Order, OrderDetail, User, Rate
 #Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	fields = ['category_name', 'level', 'category_img']
	list_display = ('category_name','category_slug','category_img')

class ProductAdmin(admin.ModelAdmin):
	fields = ['product_name', 'product_img', 'product_price', 'product_amount', 'product_sale', 'product_detail', 'category']
	list_display = ('product_name', 'product_img', 'product_price', 'product_amount', 'product_sale')

admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Rate)