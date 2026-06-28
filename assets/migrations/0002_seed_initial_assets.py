"""
Data migration: Tự động seed danh mục và thiết bị mẫu khi migrate
"""
import datetime
from django.db import migrations


def seed_assets(apps, schema_editor):
    AssetCategory = apps.get_model('assets', 'AssetCategory')
    Asset = apps.get_model('assets', 'Asset')

    # Tạo danh mục
    cnc_cat, _ = AssetCategory.objects.get_or_create(
        name='CNC Machine',
        defaults={'description': 'Máy CNC gia công cơ khí chính xác'}
    )
    rbt_cat, _ = AssetCategory.objects.get_or_create(
        name='Robot Arm',
        defaults={'description': 'Cánh tay robot lắp ráp tự động'}
    )
    conv_cat, _ = AssetCategory.objects.get_or_create(
        name='Conveyor',
        defaults={'description': 'Hệ thống băng tải vận chuyển vật tư'}
    )
    sen_cat, _ = AssetCategory.objects.get_or_create(
        name='Sensor',
        defaults={'description': 'Cảm biến IoT đo đạc nhiệt độ, độ rung'}
    )

    # Tạo thiết bị mẫu
    assets_data = [
        {
            'code': 'CNC-AX21',
            'name': 'Máy CNC Axis Pro',
            'category': cnc_cat,
            'status': 'available',
            'location': 'Xưởng A · Line 01',
            'serial_number': 'FUTURA-CNC-8761',
            'purchase_date': datetime.date(2024, 3, 14),
            'purchase_cost': 1500000000.00,
        },
        {
            'code': 'RBT-R7',
            'name': 'Robot Arm ABB R7',
            'category': rbt_cat,
            'status': 'available',
            'location': 'Dây chuyền 2',
            'serial_number': 'ABB-RBT-9022',
            'purchase_date': datetime.date(2024, 8, 22),
            'purchase_cost': 850000000.00,
        },
        {
            'code': 'CV-B2',
            'name': 'Băng tải Conveyor Belt B2',
            'category': conv_cat,
            'status': 'available',
            'location': 'Kho thông minh',
            'serial_number': 'CONV-B2-0192',
            'purchase_date': datetime.date(2025, 1, 10),
            'purchase_cost': 230000000.00,
        },
        {
            'code': 'SEN-IOT9',
            'name': 'IoT Sensor Hub',
            'category': sen_cat,
            'status': 'available',
            'location': 'Khu QC',
            'serial_number': 'SEN-IOT-9901',
            'purchase_date': datetime.date(2025, 5, 5),
            'purchase_cost': 12000000.00,
        },
        {
            'code': 'CNC-BX10',
            'name': 'Máy CNC Beta X10',
            'category': cnc_cat,
            'status': 'maintenance',
            'location': 'Xưởng B · Line 03',
            'serial_number': 'BETA-CNC-4412',
            'purchase_date': datetime.date(2023, 6, 1),
            'purchase_cost': 980000000.00,
        },
        {
            'code': 'RBT-M5',
            'name': 'Robot Arm Fanuc M5',
            'category': rbt_cat,
            'status': 'available',
            'location': 'Dây chuyền 1',
            'serial_number': 'FANUC-M5-7733',
            'purchase_date': datetime.date(2025, 2, 18),
            'purchase_cost': 1200000000.00,
        },
    ]

    for data in assets_data:
        Asset.objects.get_or_create(code=data['code'], defaults=data)


def reverse_seed(apps, schema_editor):
    # Không xóa data khi reverse migration
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_assets, reverse_seed),
    ]
