from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import generic, View
from .models import Product, Category, User, Order, OrderDetail, Rate
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.text import slugify
import glob, json
import unicodedata

def IndexView(request):
	list_cate = Category.objects.filter(level = 0)
	lists = Product.objects.filter(category__level = 0).order_by('-product_rate')[:5]
	lists_n = Product.objects.filter(category__level = 0).order_by('-date_create')[:5]
	lists_s = Product.objects.filter(category__level = 0).order_by('-product_sale')[:5]
	lists_c = Product.objects.filter(category__level = 0).order_by('product_price')[:5]
	lists_p = Product.objects.filter(category__level = 1)[:5]
	print (settings.MEDIA_ROOT+"/img/banners")
	context = {'list_product': lists,'list_product_n': lists_n,
	'list_product_s': lists_s,'list_product_c': lists_c,
	'list_product_p': lists_p, 'list_category': list_cate}
	return render(request, 'webbanhang/index.html', context)

def PhoneDetailView(request, p_id):
	product = Product.objects.get(pk = p_id)
	rate = Rate.objects.filter(
	product_rate_id = p_id
	)
	count = rate.count()
	star = 0
	for i in rate:
		star += i.rated
	if count != 0:
		star /= count
	return render(request, 'webbanhang/phone-detail.html', {'product': product, 'count': count, 'star': star, 'rate': rate})


def CategoryView(request, cate_id):
	cate = Category.objects.get(pk = cate_id)
	lists = Product.objects.filter(
	category_id = cate_id
	)
	p = Paginator(lists,20)
	page_num = request.GET.get('page',1)
	try:
		page = p.page(page_num)
	except:
		page = p.page(1)

	context = {'list_product': page, 'category': cate}
	return render(request, 'webbanhang/list-product.html', context)


def ProductView(request):
	card = request.GET.get('card','dienthoai')
	lists_cate = Category.objects.filter(
	level = 0
	)
	title = ''
	lists_product = {}
	if card == 'dienthoai':
		lists_product = Product.objects.filter(category__level = 0).order_by('-product_rate')
		title = 'Điện thoại'
	elif card == 'phukien':
		lists_product = Product.objects.filter(category__level = 1)
		lists_cate = Category.objects.filter(level = 1)
		title = 'Phụ kiện'
	elif card == 'new':
		lists_product = Product.objects.filter(category__level = 0).order_by('-date_create')
		title = 'Sản phẩm mới'
	elif card == 'sale':
		lists_product = Product.objects.filter(category__level = 0).order_by('-product_sale')
		title = 'Siêu giảm giá'
	elif card == 'cheap':
		lists_product = Product.objects.filter(category__level = 0).order_by('product_price')
		title = 'Giá rẻ online'
	else:
		lists_product = Product.objects.filter(product_slug__contains = slugify(request.GET.get('card')))
		title = 'Tìm kiếm cho '+card

	p = Paginator(lists_product,20)
	page_num = request.GET.get('page',1)
	try:
		page = p.page(page_num)
	except:
		page = p.page(1)

	context = {'list_product': page, 'category': lists_cate, 'title': title,'card': card}
	return render(request, 'webbanhang/product.html', context)


def LoginView(request):
	redirect = request.GET.get('next')
	return render(request, 'webbanhang/login.html',{'redirect': redirect})

def Login(request):
	redirect = request.GET.get('next')
	try:
		user = User.objects.get(email = request.POST['email'])
	except:
		messages.error(request, 'sai ten dang nhap hoac mat khau!')
		return HttpResponseRedirect(reverse('webbanhang:login-view'))
	if user.password == request.POST['password']:
		request.session['member_id'] = user.id
		request.session['member_name'] = user.name
		messages.info(request, 'đăng nhập thành công!')
		return HttpResponseRedirect(redirect)
	else:
		messages.error(request, 'sai ten dang nhap hoac mat khau!')
		return HttpResponseRedirect(reverse('webbanhang:login-view'))


def RegisterView(request):
	global formregister
	return render(request, 'webbanhang/register.html' )

def Register(request):
	username = request.POST['name']
	email = request.POST['email']
	password = request.POST['password']
	try:
		email = User.objects.get(email = request.POST['email'])
		messages.error(request, 'email đã tồn tại!')
		return HttpResponseRedirect(reverse('webbanhang:register-view'))
	except:
		phone = request.POST['phone']
		address = request.POST['address']
		user = User(name=username,email=email,password=password,phone=phone,address=address)
		user.save()
		messages.info(request, 'đăng kí thành công!')
		return HttpResponseRedirect(reverse('webbanhang:index'))


def Logout(request):
	del request.session['member_id']
	del request.session['member_name']
	messages.info(request, 'đăng xuất thành công!')
	return HttpResponseRedirect(reverse('webbanhang:index'))


def CartView(request):
	total = 0
	carts = request.session.get('cart',{})
	for key, value in carts.items():
		total += float(value['num'])*float(value['price'])
	return render(request,'webbanhang/cart.html', {'total': total})
#if request.is_ajax():

def Cart(request):
	print (request.POST['num'])
	if request.POST['num'] == '-10':
		del request.session['cart']
	else:
		idsp = request.POST.get('id')
		sp = Product.objects.get(pk = idsp)
		if bool(request.session.get('cart',False)) == False:
			request.session['cart'] = {}
		cart = request.session['cart']
		if idsp in cart:
			cart[idsp]['num'] = int(request.POST['num'])+cart[idsp]['num']
			cart[idsp]['tt_price'] = cart[idsp]['num']*cart[idsp]['price']
			if cart[idsp]['num'] == 0:
				del cart[idsp]

		else:
			cart[idsp] = {
				'id': idsp,
				'num': 1,
				'name': sp.product_name,
				'img': sp.product_img.path,
				'price': float(sp.product_price*(100-sp.product_sale)/100),
				'tt_price': float(sp.product_price*(100-sp.product_sale)/100),
			}
		request.session['cart'] = cart
		if request.session['cart'] == {}:
			del request.session['cart']
	return HttpResponseRedirect(reverse('webbanhang:cart-view'))

def OrderView(request):
	if request.session.get('member_id',False) == False:
		redirect = redirect = request.GET.get('next')
		messages.error(request,'Bạn cần đăng nhập để thanh toán!')
		return render(request,'webbanhang/login.html',{'redirect': redirect})
	user = User.objects.get(pk = request.session['member_id'])
	total = 0
	carts = request.session.get('cart',{})
	for key, value in carts.items():
		total += float(value['num'])*float(value['price'])
	return render(request,'webbanhang/order.html', {'user': user, 'total': total})

def Orders(request):
	user = User.objects.get(pk = request.session.get('member_id'))
	orders = Order(
	order_customer = user,
	order_name = request.POST['name'],
	order_phone = request.POST['phone'],
	order_address = request.POST['address'],
	order_total = request.POST['amount'],
	order_status = 'da thanh toan',
	)
	orders.save()
	for i in request.session['cart']:
		prd = Product.objects.get(pk = i)
		order_detail = OrderDetail(
		product = prd,
		order = orders,
		qty = request.session['cart'][i]['num'],
		price = request.session['cart'][i]['price'],
		)
		order_detail.save()
	del request.session['cart']
	messages.info(request, 'đặt hàng thành công!')
	return HttpResponseRedirect(reverse('webbanhang:index'))


def CustomInfoView(request):
	if request.session.get('member_id',False):
		user = User.objects.get(pk = request.session['member_id'])
		return render(request,'webbanhang/customers-info.html', {'user': user})
	return HttpResponse("Bạn chưa đăng nhập!")

def UpdateInfoView(request):
	if request.session.get('member_id',False):
		user = User.objects.get(pk = request.session['member_id'])
		return render(request,'webbanhang/update-info.html', {'user': user})
	return HttpResponse("Bạn chưa đăng nhập!")

def UpdateInfo(request):
	user = User.objects.get(pk = request.session['member_id'])
	user.name = request.POST.get("name")
	user.email = request.POST.get("email")
	user.phone = request.POST.get("phone")
	user.address = request.POST.get("address")
	user.save()
	messages.success(request, 'cập nhật thành công!')
	return HttpResponseRedirect(reverse('webbanhang:custom-info' ) )

def PurchaseHistory(request):
	if request.session.get('member_id',False):
		bills = Order.objects.filter(
		order_customer_id = request.session.get('member_id')
		)
		return render(request,'webbanhang/purchase_history.html', {'bills': bills})
	return HttpResponse("Bạn chưa đăng nhập!")

def BillDetail(request):
	detail = OrderDetail.objects.filter(
	order_id = request.GET.get('id')
	)
	print(request.GET.get('id'))
	total = Order.objects.get(pk = request.GET.get('id')).order_total
	return render(request,'webbanhang/bills-detail.html', {'detail': detail, 'total': total})

def RateProduct(request):
	if request.session.get('member_id',False) == False:
		messages.error(request,'Bạn cần đăng nhập để bình luận!')
		return HttpResponseRedirect(reverse('webbanhang:phone-detail', args=(request.POST.get('id'),) ) )
	if request.POST.get('comment') == '':
		messages.error(request,'Bạn chưa comment!')
		return HttpResponseRedirect(reverse('webbanhang:phone-detail', args=(request.POST.get('id'),) ) )
	if request.POST.get('star') == None:
		messages.error(request,'Bạn chưa đánh giá sản phẩm!')
		return HttpResponseRedirect(reverse('webbanhang:phone-detail', args=(request.POST.get('id'),) ) )
	user = User.objects.get(pk = request.session.get('member_id'))
	product = Product.objects.get(pk = request.POST.get('id'))
	rate = Rate(
	product_rate = product,
	customer = user,
	comment = request.POST.get('comment'),
	rated = request.POST.get('star'),
	)
	rate.save()
	messages.success(request, 'bình luận thành công!')
	return HttpResponseRedirect(reverse('webbanhang:phone-detail', args=(request.POST.get('id'),) ) )
	