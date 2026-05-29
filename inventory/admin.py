from django.contrib import admin

from .models import Material, StockTransaction


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
	list_display = ('sku', 'name', 'unit', 'quantity_on_hand', 'reorder_level')
	search_fields = ('sku', 'name')


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
	list_display = ('material', 'transaction_type', 'quantity', 'created_by', 'created_at')
	list_filter = ('transaction_type',)
	search_fields = ('material__sku', 'material__name', 'reference')
