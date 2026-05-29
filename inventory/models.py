from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Material(models.Model):
	name = models.CharField(max_length=150)
	sku = models.CharField(max_length=50, unique=True)
	unit = models.CharField(max_length=20, default='unit')
	quantity_on_hand = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	reorder_level = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return f"{self.sku} - {self.name}"


class StockTransaction(models.Model):
	TYPE_IN = 'in'
	TYPE_OUT = 'out'
	TYPE_ADJUST = 'adjust'

	TYPE_CHOICES = [
		(TYPE_IN, 'In'),
		(TYPE_OUT, 'Out'),
		(TYPE_ADJUST, 'Adjust'),
	]

	material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='transactions')
	transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
	quantity = models.DecimalField(max_digits=12, decimal_places=2)
	reference = models.CharField(max_length=100, blank=True)
	note = models.TextField(blank=True)
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"{self.material.sku} - {self.transaction_type}"
