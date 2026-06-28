from django.db import models
from django.contrib.auth.models import User 

class Material(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã vật tư") # [cite: 308]
    name = models.CharField(max_length=100, verbose_name="Tên vật tư") # [cite: 308]
    unit = models.CharField(max_length=20, verbose_name="Đơn vị tính") # [cite: 308]
    quantity = models.IntegerField(default=0, verbose_name="Số lượng tồn") # [cite: 308]
    min_quantity = models.IntegerField(default=5, verbose_name="Mức tồn tối thiểu") # [cite: 308]
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Vị trí lưu kho") # [cite: 165, 308]
    note = models.TextField(blank=True, null=True, verbose_name="Ghi chú") # [cite: 165, 308]

    def __str__(self):
        return f"{self.name} ({self.code})"

class StockTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('import', 'Nhập kho'), 
        ('export', 'Xuất kho'), 
    ]
    
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='transactions', verbose_name="Vật tư") 
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name="Loại giao dịch") 
    quantity = models.IntegerField(verbose_name="Số lượng thay đổi") 
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người thực hiện") 
    note = models.TextField(blank=True, null=True, verbose_name="Ghi chú") # [cite: 311]
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày thực hiện") 

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.material.name} ({self.quantity})"