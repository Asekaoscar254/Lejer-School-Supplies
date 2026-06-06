from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from datetime import date, timedelta

from .forms import BatchForm, ProductForm
from .models import Product, Batch, Order


# ---- Group / role helpers ----
def _in_group(user, group_name):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name=group_name).exists())


def is_admin(user):
    return _in_group(user, 'Admin')


def is_staff_group(user):
    return _in_group(user, 'Staff')


admin_required = user_passes_test(is_admin, login_url='login')


def staff_or_admin_check(user):
    return is_admin(user) or is_staff_group(user)


staff_or_admin_required = user_passes_test(staff_or_admin_check, login_url='login')


# ---- Authentication view with redirection ----
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('welcome')
    else:
        form = AuthenticationForm(request)

    return render(request, 'registration/login.html', {'form': form})


@login_required(login_url='login')
def welcome(request):
    return render(request, 'registration/welcome.html')


# ---- Views ----
@staff_or_admin_required
def admin_dashboard(request):
    """Admin landing page with full stats."""
    all_products = Product.objects.all()
    low_stock = [p for p in all_products if p.total_stock <= p.low_stock_threshold]

    today = date.today()
    thirty_days_later = today + timedelta(days=30)
    expiring_batches = Batch.objects.filter(
        expiry_date__range=[today, thirty_days_later]
    ).order_by('expiry_date')

    recent_orders = Order.objects.all().order_by('-order_date')[:5]

    context = {
        'low_stock': low_stock,
        'expiring_batches': expiring_batches,
        'recent_orders': recent_orders,
    }
    return render(request, 'main/dashboard.html', context)


@staff_or_admin_required
def inventory_list(request):
    products = Product.objects.all().order_by('name')
    total_stock_items = Batch.objects.aggregate(total=Sum('quantity'))['total'] or 0
    product_count = products.count()
    low_stock_count = sum(1 for product in products if product.total_stock <= product.low_stock_threshold)

    return render(request, 'main/inventory.html', {
        'products': products,
        'total_stock_items': total_stock_items,
        'product_count': product_count,
        'low_stock_count': low_stock_count,
    })


@admin_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'{product.name} was added successfully.')
            return redirect('inventory')
    else:
        form = ProductForm()

    return render(request, 'main/product_form.html', {
        'form': form,
        'title': 'Add Product',
        'submit_label': 'Add Product',
    })


@admin_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'{product.name} was updated successfully.')
            return redirect('inventory')
    else:
        form = ProductForm(instance=product)

    return render(request, 'main/product_form.html', {
        'form': form,
        'product': product,
        'title': 'Edit Product',
        'submit_label': 'Save Changes',
    })


@admin_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'{product_name} was deleted successfully.')
        return redirect('inventory')

    return render(request, 'main/product_confirm_delete.html', {'product': product})


@admin_required
def product_add_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            batch = form.save(commit=False)
            batch.product = product
            batch.save()
            messages.success(request, f'Added {batch.quantity} item(s) to {product.name}.')
            return redirect('inventory')
    else:
        form = BatchForm()

    return render(request, 'main/batch_form.html', {
        'form': form,
        'product': product,
    })


@admin_required
def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'main/orders.html', {'orders': orders})


@admin_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = order.items.all()
    context = {'order': order, 'items': items}
    return render(request, 'main/order_detail.html', context)


def generate_invoice(request, pk):
    # Logic for WeasyPrint or xhtml2pdf goes here
    raise PermissionDenied


def generate_delivery_note(request, pk):
    # Logic for Delivery Note PDF goes here
    raise PermissionDenied


@staff_or_admin_required
def dashboard_reviews(request):
    products = Product.objects.all()
    low_stock = [p for p in products if p.total_stock <= p.low_stock_threshold]
    return render(request, 'main/dashboard_reviews.html', {'low_stock': low_stock})


@staff_or_admin_required
def staff_dashboard(request):
    return redirect('admin_dashboard')
