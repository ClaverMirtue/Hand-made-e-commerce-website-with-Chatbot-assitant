from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import *
from .forms import UserRegistrationForm, OrderForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    return render(request, 'handapp/home.html')

def shop(request):
    sort = request.GET.get('sort', '')
    products = Product.objects.filter(available=True)
    
    # Apply sorting
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)  # Show 9 products per page
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    return render(request, 'handapp/shop.html', {
        'products': products,
        'current_sort': sort
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, 'handapp/categories.html', {
        'categories': categories
    })

def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    sort = request.GET.get('sort', '')
    products = Product.objects.filter(category=category, available=True)
    
    # Apply sorting
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)  # Show 9 products per page
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    return render(request, 'handapp/category_products.html', {
        'category': category,
        'products': products,
        'current_sort': sort
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'handapp/product_detail.html', {'product': product})

def search_products(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        products = []
    return render(request, 'handapp/search_results.html', {
        'products': products,
        'query': query
    })

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'handapp/cart.html', {'items': items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, 'Product added to cart.')
    return redirect('handapp:cart')

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total
            order.save()
            
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            cart.delete()
            messages.success(request, 'Order placed successfully!')
            return redirect('handapp:order_detail', order_id=order.id)
    else:
        form = OrderForm()
    
    return render(request, 'handapp/checkout.html', {
        'form': form,
        'items': items,
        'total': total
    })

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'handapp/profile.html', {'orders': orders})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'handapp/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    return render(request, 'handapp/order_detail.html', {
        'order': order,
        'items': items
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('handapp:home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = UserRegistrationForm()
    return render(request, 'handapp/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('handapp:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'handapp/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('handapp:home')

@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(cart=cart, product=product).delete()
    messages.success(request, 'Product removed from cart.')
    return redirect('handapp:cart')

@login_required
def update_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated successfully.')
    else:
        cart_item.delete()
        messages.success(request, 'Product removed from cart.')
    
    return redirect('handapp:cart')
