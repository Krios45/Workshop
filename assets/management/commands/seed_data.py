from django.core.management.base import BaseCommand
from assets.models import Asset, AssetCategory, MaintenanceLog
from inventory.models import Material
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed initial categories, assets, and materials for demo purposes.'

    def handle(self, *args, **options):
        # 1. Categories
        cnc_cat, _ = AssetCategory.objects.get_or_create(name='CNC Machine', defaults={'description': 'Máy CNC gia công cơ khí chính xác'})
        rbt_cat, _ = AssetCategory.objects.get_or_create(name='Robot Arm', defaults={'description': 'Cánh tay robot lắp ráp tự động'})
        conv_cat, _ = AssetCategory.objects.get_or_create(name='Conveyor', defaults={'description': 'Hệ thống băng tải vận chuyển vật tư'})
        sen_cat, _ = AssetCategory.objects.get_or_create(name='Sensor', defaults={'description': 'Cảm biến IoT đo đạc nhiệt độ, độ rung'})
        
        self.stdout.write('Created categories.')

        # 2. Assets
        Asset.objects.get_or_create(
            code='CNC-AX21',
            defaults={
                'name': 'Máy CNC Axis Pro',
                'category': cnc_cat,
                'status': Asset.STATUS_AVAILABLE,
                'location': 'Xưởng A · Line 01',
                'serial_number': 'FUTURA-CNC-8761',
                'purchase_date': datetime.date(2024, 3, 14),
                'purchase_cost': 1500000000.00
            }
        )
        
        Asset.objects.get_or_create(
            code='RBT-R7',
            defaults={
                'name': 'Robot Arm ABB R7',
                'category': rbt_cat,
                'status': Asset.STATUS_AVAILABLE,
                'location': 'Dây chuyền 2',
                'serial_number': 'ABB-RBT-9022',
                'purchase_date': datetime.date(2024, 8, 22),
                'purchase_cost': 850000000.00
            }
        )
        
        Asset.objects.get_or_create(
            code='CV-B2',
            defaults={
                'name': 'Băng tải Conveyor Belt B2',
                'category': conv_cat,
                'status': Asset.STATUS_AVAILABLE,
                'location': 'Kho thông minh',
                'serial_number': 'CONV-B2-0192',
                'purchase_date': datetime.date(2025, 1, 10),
                'purchase_cost': 230000000.00
            }
        )
        
        Asset.objects.get_or_create(
            code='SEN-IOT9',
            defaults={
                'name': 'IoT Sensor Hub',
                'category': sen_cat,
                'status': Asset.STATUS_AVAILABLE,
                'location': 'Khu QC',
                'serial_number': 'SEN-IOT-9901',
                'purchase_date': datetime.date(2025, 5, 5),
                'purchase_cost': 12000000.00
            }
        )
        
        self.stdout.write('Created assets.')

        # 3. Materials
        Material.objects.get_or_create(
            sku='LUB-220',
            defaults={
                'name': 'Dầu bôi trơn LUB-220',
                'unit': 'Lít',
                'quantity_on_hand': 86.00,
                'reorder_level': 20.00,
                'description': 'Dầu bôi trơn hệ thống cơ khí'
            }
        )
        
        Material.objects.get_or_create(
            sku='BRG-KIT',
            defaults={
                'name': 'Bearing Replacement Kit',
                'unit': 'Bộ',
                'quantity_on_hand': 12.00,
                'reorder_level': 5.00,
                'description': 'Bộ vòng bi thay thế'
            }
        )
        
        Material.objects.get_or_create(
            sku='SEN-IR',
            defaults={
                'name': 'Cảm biến hồng ngoại IR',
                'unit': 'Cái',
                'quantity_on_hand': 0.00,
                'reorder_level': 10.00,
                'description': 'Cảm biến hồng ngoại'
            }
        )
        
        Material.objects.get_or_create(
            sku='MOTOR-1HP',
            defaults={
                'name': 'Động cơ điện 1HP',
                'unit': 'Cái',
                'quantity_on_hand': 22.00,
                'reorder_level': 3.00,
                'description': 'Động cơ điện dự phòng'
            }
        )
        
        Material.objects.get_or_create(
            sku='BELT-B52',
            defaults={
                'name': 'Dây curoa Belt B52',
                'unit': 'Sợi',
                'quantity_on_hand': 41.00,
                'reorder_level': 15.00,
                'description': 'Dây đai truyền động'
            }
        )
        
        self.stdout.write('Created materials.')
        self.stdout.write(self.style.SUCCESS('Seeding completed successfully!'))
