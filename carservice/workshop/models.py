from django.db import models
from decimal import Decimal


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название услуги')
    description = models.TextField(verbose_name='Описание услуги')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    duration = models.PositiveIntegerField(default=60, verbose_name='Длительность (мин.)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['name']


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя клиента')
    phone = models.CharField(max_length=15, unique=True, verbose_name='Телефон')
    discount = models.PositiveIntegerField(default=0, verbose_name='Скидка (%)')

    def __str__(self):
        return self.name

    def get_discounted_price(self, original_price):
        """Метод для вычисления цены с учетом скидки."""
        return original_price * (1 - self.discount / 100)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mechanic(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя мастера')
    specialty = models.CharField(max_length=100, verbose_name='Специализация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'


class Box(models.Model):
    number = models.PositiveIntegerField(verbose_name='Номер бокса')
    available_spots = models.PositiveIntegerField(default=2, verbose_name='Доступные места')

    def __str__(self):
        return f"Бокс {self.number}"

    def get_available_spots(self, start_time, end_time):
        overlapping_bookings = CarRepairBooking.objects.filter(
            box=self,
            booking_time__lt=end_time,
            booking_time__gte=start_time
        ).count()
        return self.available_spots - overlapping_bookings

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'


class CarRepairBooking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings', verbose_name='Клиент')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings', verbose_name='Услуга')
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, related_name='bookings', verbose_name='Мастер')
    box = models.ForeignKey(Box, on_delete=models.CASCADE, related_name='bookings', verbose_name='Бокс')
    booking_time = models.DateTimeField(verbose_name='Время записи')

    def __str__(self):
        return f"Запись {self.client.name} на {self.booking_time}"

    def get_discounted_price(self):
        price = self.service.price
        discount_percentage = Decimal(self.client.discount)
        discount_factor = Decimal('100') - discount_percentage
        discounted_price = (price * discount_factor) / Decimal('100')
        return discounted_price.quantize(Decimal('0.01'))

    @property
    def total_price(self):
        return self.get_discounted_price()

    class Meta:
        verbose_name = 'Запись на ремонт'
        verbose_name_plural = 'Записи на ремонт'
        ordering = ['booking_time']
