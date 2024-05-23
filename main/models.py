from users.models import *

class CategoryBus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категория автобуса'
        verbose_name_plural = 'Категории автобусов'

    def __str__(self):
        return self.name

class Bus(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    transmission_type = models.CharField(max_length=50, choices=[('auto', 'Automatic'), ('manual', 'Manual')])
    year_of_production = models.IntegerField()
    is_available = models.BooleanField(default=True)
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Автобус'
        verbose_name_plural = 'Автобусы'
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    driver_needed = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    start_point = models.CharField(max_length=200, null=True, blank=True)
    end_point = models.CharField(max_length=200, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=[('cash', 'Cash'), ('card', 'Card')])
    status = models.CharField(max_length=50,
                              choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
                              default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
