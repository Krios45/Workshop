from django import forms
from .models import StockTransaction

class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ['material', 'transaction_type', 'quantity', 'note']
        widgets = {
            'material': forms.Select(attrs={'class': 'form-select'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        material = cleaned_data.get('material')
        transaction_type = cleaned_data.get('transaction_type')
        quantity = cleaned_data.get('quantity')

        if transaction_type == 'export' and material and quantity:
            if material.quantity < quantity:
                raise forms.ValidationError(
                    f"Không thể xuất kho! {material.name} hiện tại chỉ còn tồn {material.quantity} {material.unit}."
                )
        return cleaned_data