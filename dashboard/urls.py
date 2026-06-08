from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assets/', views.assets, name='assets'),
    path('assets/detail/', views.asset_detail, name='asset_detail'),
    path('maintenance/schedule/', views.maintenance_schedule, name='maintenance_schedule'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/transactions/', views.stock_transactions, name='stock_transactions'),
    path('analytics/', views.analytics, name='analytics'),
]
