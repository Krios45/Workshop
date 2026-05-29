from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class AssetCategory(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return self.name


class Asset(models.Model):
	STATUS_AVAILABLE = 'available'
	STATUS_IN_USE = 'in_use'
	STATUS_MAINTENANCE = 'maintenance'
	STATUS_RETIRED = 'retired'

	STATUS_CHOICES = [
		(STATUS_AVAILABLE, 'Available'),
		(STATUS_IN_USE, 'In use'),
		(STATUS_MAINTENANCE, 'Maintenance'),
		(STATUS_RETIRED, 'Retired'),
	]

	category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT, related_name='assets')
	name = models.CharField(max_length=150)
	code = models.CharField(max_length=50, unique=True)
	serial_number = models.CharField(max_length=100, blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
	location = models.CharField(max_length=200, blank=True)
	purchase_date = models.DateField(null=True, blank=True)
	purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	image_file = models.FileField(upload_to='assets/', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return f"{self.code} - {self.name}"


class MaintenanceLog(models.Model):
	STATUS_SCHEDULED = 'scheduled'
	STATUS_COMPLETED = 'completed'
	STATUS_CANCELED = 'canceled'

	STATUS_CHOICES = [
		(STATUS_SCHEDULED, 'Scheduled'),
		(STATUS_COMPLETED, 'Completed'),
		(STATUS_CANCELED, 'Canceled'),
	]

	asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_logs')
	performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	description = models.TextField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"{self.asset.code} - {self.status}"
