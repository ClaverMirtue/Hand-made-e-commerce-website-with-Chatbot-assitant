from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Product, Order, OrderItem, Cart, CartItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'created_at', 'image_preview']
    list_filter = ['available', 'category', 'created_at']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'total_amount', 'status', 'created_at', 'view_order_items']
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'email', 'phone']
    ordering = ['-created_at']
    
    def view_order_items(self, obj):
        url = reverse('admin:handapp_orderitem_changelist') + f'?order__id={obj.id}'
        return format_html('<a href="{}">View Items</a>', url)
    view_order_items.short_description = 'Items'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
