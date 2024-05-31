from django import forms
from main.models import Order

class CancelOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['cancel_reason']
        widgets = {
            'cancel_reason': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'cancel_reason': 'Причина отмены',
        }
