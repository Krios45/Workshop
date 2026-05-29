from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = ('asset', 'user', 'start_time', 'end_time', 'status')
	list_filter = ('status',)
	search_fields = ('asset__code', 'asset__name', 'user__username')
