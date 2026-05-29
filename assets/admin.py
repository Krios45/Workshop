from django.contrib import admin

from .models import Asset, AssetCategory, MaintenanceLog


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'is_active', 'updated_at')
	search_fields = ('name',)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
	list_display = ('code', 'name', 'category', 'status', 'location', 'updated_at')
	list_filter = ('status', 'category')
	search_fields = ('code', 'name', 'serial_number')


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
	list_display = ('asset', 'status', 'start_date', 'end_date', 'cost')
	list_filter = ('status',)
	search_fields = ('asset__code', 'asset__name')
