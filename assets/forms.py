from django import forms
from .models import Asset, AssetCategory

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'code', 'name', 'category', 'serial_number', 
            'status', 'location', 'purchase_date', 'purchase_cost', 'image_file'
        ]
        labels = {
            'code': 'Mã thiết bị',
            'name': 'Tên thiết bị',
            'category': 'Danh mục thiết bị',
            'serial_number': 'Số Serial / Nhà sản xuất',
            'status': 'Trạng thái',
            'location': 'Khu vực / Vị trí',
            'purchase_date': 'Ngày mua',
            'purchase_cost': 'Giá mua (VNĐ)',
            'image_file': 'Tệp hình ảnh',
        }
        widgets = {
            'status': forms.Select(choices=[
                ('available', 'Sẵn sàng (Available)'),
                ('in_use', 'Đang sử dụng (In use)'),
                ('maintenance', 'Bảo trì (Maintenance)'),
                ('retired', 'Đã thanh lý (Retired)'),
            ]),
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'purchase_cost': forms.NumberInput(attrs={'step': '0.01'}),
        }
