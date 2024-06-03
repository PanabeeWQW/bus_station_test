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

class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'processed']  # Отображаемые поля в списке
    list_filter = ['processed']  # Фильтр по обработке заявок
    actions = ['mark_as_processed', 'mark_as_unprocessed']  # Действия для обновления статуса обработки

    def mark_as_processed(self, request, queryset):
        queryset.update(processed=True)
    mark_as_processed.short_description = "Отметить выбранные заявки как обработанные"  # Название действия

    def mark_as_unprocessed(self, request, queryset):
        queryset.update(processed=False)
    mark_as_unprocessed.short_description = "Отметить выбранные заявки как необработанные"  # Название действия

admin.site.register(SupportRequest, SupportRequestAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(Bus_Brand)
admin.site.register(Bus_Category)
admin.site.register(Order)
admin.site.register(TripReview)
