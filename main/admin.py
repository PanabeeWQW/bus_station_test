from django.contrib import admin
from .models import *
from django.forms import BaseInlineFormSet, ValidationError
class BusPhotoInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        if len(self.forms) > 5:
            raise ValidationError('Нельзя загружать больше 5 фотографий.')

class BusPhotoInline(admin.TabularInline):
    model = BusPhoto
    formset = BusPhotoInlineFormSet
    extra = 1
    max_num = 5

class BusAdmin(admin.ModelAdmin):
    inlines = [BusPhotoInline]

admin.site.register(Bus, BusAdmin)
admin.site.register(Bus_Brand)
admin.site.register(Bus_Category)
admin.site.register(Order)

