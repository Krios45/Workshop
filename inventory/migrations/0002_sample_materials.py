from django.db import migrations


def create_sample_materials(apps, schema_editor):
    Material = apps.get_model('inventory', 'Material')
    samples = [
        {'code': 'LUB-220', 'name': 'Dầu bôi trơn spindle', 'unit': 'Lít',
         'quantity': 86, 'min_quantity': 20, 'location': 'Kho A', 'note': 'Dầu bôi trơn trục chính'},
        {'code': 'BRG-KIT', 'name': 'Bộ vòng bi (Bearing Kit)', 'unit': 'Bộ',
         'quantity': 12, 'min_quantity': 15, 'location': 'Kho B', 'note': 'Phụ tùng thay thế'},
        {'code': 'SEN-IR', 'name': 'Cảm biến hồng ngoại', 'unit': 'Cái',
         'quantity': 3, 'min_quantity': 10, 'location': 'Kho A', 'note': 'Cảm biến cho dây chuyền'},
        {'code': 'BELT-V', 'name': 'Dây curoa chữ V', 'unit': 'Sợi',
         'quantity': 45, 'min_quantity': 10, 'location': 'Kho B', 'note': ''},
        {'code': 'MOT-3P', 'name': 'Động cơ 3 pha 1.5kW', 'unit': 'Cái',
         'quantity': 6, 'min_quantity': 3, 'location': 'Kho C', 'note': 'Động cơ dự phòng'},
    ]
    for item in samples:
        Material.objects.update_or_create(code=item['code'], defaults=item)


def remove_sample_materials(apps, schema_editor):
    Material = apps.get_model('inventory', 'Material')
    codes = ['LUB-220', 'BRG-KIT', 'SEN-IR', 'BELT-V', 'MOT-3P']
    Material.objects.filter(code__in=codes).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_materials, remove_sample_materials),
    ]
