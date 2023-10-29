from django.urls import path

from . import views

app_name = "webbanhang"

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('<int:p_id>/', views.PhoneDetailView, name='phone-detail'),
    path('listproduct/<int:cate_id>/',views.CategoryView, name='list-product'),
    path('product/',views.ProductView, name='product'),
    path('login/',views.LoginView, name='login-view'),
    path('login2/',views.Login, name='login'),
    path('logout/',views.Logout,name='logout'),
    path('register/',views.RegisterView, name='register-view'),
    path('register2/',views.Register,name='register'),
    path('cart/',views.CartView, name='cart-view'),
    path('cart2',views.Cart, name='cart'),
    path('order',views.OrderView, name='order-view'),
    path('order2',views.Orders, name='order'),
    path('custom-info',views.CustomInfoView, name='custom-info'),
    path('purchase-history',views.PurchaseHistory, name='purchase-history'),
    path('bills-detail',views.BillDetail, name='bills-detail'),
    path('rate',views.RateProduct, name='rate'),
    path('update-info',views.UpdateInfoView, name='update-info'),
    path('update-info2',views.UpdateInfo, name='update-info2'),

]