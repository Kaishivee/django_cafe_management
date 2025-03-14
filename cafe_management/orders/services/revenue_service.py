from orders.models import Order
from django.db.models import Sum

class RevenueService:
    """Сервис для работы с выручкой и статистикой продаж.
       Предоставляет методы для расчета общей выручки и списка проданных блюд"""
    @staticmethod
    def calculate_total_revenue():
        return Order.objects.filter(status='paid').aggregate(Sum('total_price'))['total_price__sum'] or 0

    @staticmethod
    def get_sold_items():
        sold_items = {}
        paid_orders = Order.objects.filter(status='paid')
        for order in paid_orders:
            for item in order.items:
                dish_name = item['name']
                quantity = item['quantity']
                if dish_name in sold_items:
                    sold_items[dish_name] += quantity
                else:
                    sold_items[dish_name] = quantity
        return sorted(sold_items.items(), key=lambda x: x[1], reverse=True)