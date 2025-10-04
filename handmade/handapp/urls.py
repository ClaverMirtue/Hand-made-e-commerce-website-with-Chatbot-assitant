from django.urls import path
from . import views

app_name = 'handapp'

urlpatterns = [
    # Home and Shop pages
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('categories/', views.categories, name='categories'),
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),
    
    # Product pages
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search_products, name='search'),
    
    # Cart and Checkout
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # User Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # User Profile and Orders
    path('profile/', views.profile, name='profile'),
    path('orders/', views.order_history, name='orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]
