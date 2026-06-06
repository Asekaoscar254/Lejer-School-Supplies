from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('welcome/', views.welcome, name='welcome'),
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('reviews/', views.dashboard_reviews, name='dashboard_reviews'),
    path('inventory/', views.inventory_list, name='inventory'),
    path('inventory/products/add/', views.product_create, name='product_add'),
    path('inventory/products/<int:pk>/edit/', views.product_update, name='product_edit'),
    path('inventory/products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('inventory/products/<int:pk>/stock/add/', views.product_add_stock, name='product_add_stock'),
    path('orders/', views.order_list, name='orders'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
]
