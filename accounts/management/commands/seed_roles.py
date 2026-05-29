from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from assets.models import Asset, AssetCategory, MaintenanceLog
from bookings.models import Booking
from inventory.models import Material, StockTransaction


ROLE_PERMISSIONS = {
	'Admin': 'all',
	'Manager': [
		Asset,
		AssetCategory,
		MaintenanceLog,
		Booking,
		Material,
		StockTransaction,
	],
	'Staff': [
		Asset,
		AssetCategory,
		Booking,
		Material,
	],
}


class Command(BaseCommand):
	help = 'Create default groups and permissions.'

	def handle(self, *args, **options):
		for role, models_or_all in ROLE_PERMISSIONS.items():
			group, _ = Group.objects.get_or_create(name=role)
			if models_or_all == 'all':
				group.permissions.set(Permission.objects.all())
				self.stdout.write(self.style.SUCCESS(f'Updated {role} permissions.'))
				continue

			perms = Permission.objects.none()
			for model in models_or_all:
				content_type = ContentType.objects.get_for_model(model)
				perms = perms | Permission.objects.filter(content_type=content_type)

			group.permissions.set(perms)
			self.stdout.write(self.style.SUCCESS(f'Updated {role} permissions.'))

		self.stdout.write(self.style.SUCCESS('Done.'))
