from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import School, Product, Batch, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class BatchInline(admin.TabularInline):
    model = Batch
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'total_stock')
    inlines = [BatchInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'school', 'order_date', 'is_delivered')
    list_filter = ('is_delivered', 'order_date')
    inlines = [OrderItemInline]

admin.site.register(School)
admin.site.register(Batch)