from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['asset', 'start_time', 'end_time', 'purpose']
        labels = {
            'asset': 'Thiết bị',
            'start_time': 'Thời gian bắt đầu',
            'end_time': 'Thời gian kết thúc',
            'purpose': 'Mục đích sử dụng',
        }
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'purpose': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Lý do sử dụng/mượn thiết bị...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("Thời gian kết thúc phải sau thời gian bắt đầu.")
        return cleaned_data
