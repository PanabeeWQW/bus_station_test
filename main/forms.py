from django import forms
from main.models import Order

class CancelOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['cancellation_reason']
        widgets = {
            'cancellation_reason': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'cancellation_reason': 'Причина отмены',
        }
