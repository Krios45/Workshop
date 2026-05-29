from django.contrib.auth import get_user_model
from django.db import models

from assets.models import Asset

User = get_user_model()


class Booking(models.Model):
	STATUS_PENDING = 'pending'
	STATUS_APPROVED = 'approved'
	STATUS_REJECTED = 'rejected'
	STATUS_CANCELED = 'canceled'
	STATUS_COMPLETED = 'completed'

	STATUS_CHOICES = [
		(STATUS_PENDING, 'Pending'),
		(STATUS_APPROVED, 'Approved'),
		(STATUS_REJECTED, 'Rejected'),
		(STATUS_CANCELED, 'Canceled'),
		(STATUS_COMPLETED, 'Completed'),
	]

	asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name='bookings')
	user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='bookings')
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	purpose = models.TextField(blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return f"{self.asset.code} booking by {self.user.username}"
