from users.models import *

class Bus_Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name = 'Категория авто'
        verbose_name_plural = 'Категории авто'

    def __str__(self):
        return self.name

class Bus_Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Бренд авто'
        verbose_name_plural = 'Бренды авто'

    def __str__(self):
        return self.name

class Bus(models.Model):
    bus_photo = models.ImageField(upload_to='images/bus_images')
    brand = models.ForeignKey(Bus_Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Bus_Category, on_delete=models.CASCADE)
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
