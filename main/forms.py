from django import forms
from main.models import Order, SupportRequest

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
class SupportForm(forms.ModelForm):
    class Meta:
        model = SupportRequest
        fields = ['name', 'email', 'message']

class TripReviewForm(forms.Form):
    rating = forms.IntegerField(label='Рейтинг', min_value=1, max_value=5)
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'rows': 4}))
