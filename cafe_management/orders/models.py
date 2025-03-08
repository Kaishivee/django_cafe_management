from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import JSONField

from .menu import MENU


class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField(validators=[MinValueValidator(1)])
    items = JSONField(default=list)  # Список блюд с ценами
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')

    def __str__(self):
        return f"Заказ #{self.id} (Стол {self.table_number})"

    def calculate_total_price(self):
        """
        Вычисляет общую стоимость заказа на основе списка блюд.
        """
        total = 0
        for item in self.items:
            dish_name = item['name']
            quantity = item['quantity']
            for category, dishes in MENU.items():
                if dish_name in dishes:
                    total += dishes[dish_name] * quantity
        self.total_price = total

    def save(self, *args, **kwargs):
        """Пересчитываем общую стоимость перед сохранением"""
        self.calculate_total_price()
        super().save(*args, **kwargs)

    def update_status(self, new_status):
        """
        Обновляет статус заказа.
        """
        self.status = new_status
        self.save()