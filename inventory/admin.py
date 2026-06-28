from django.contrib import admin
from .models import Material, StockTransaction

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'unit', 'quantity', 'min_quantity', 'location')
    search_fields = ('code', 'name')
    list_filter = ('location',)

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ('material', 'transaction_type', 'quantity', 'user', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    date_hierarchy = 'created_at'
