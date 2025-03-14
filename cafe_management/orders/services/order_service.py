from orders.models import Order

class OrderService:
    """Сервис для работы с заказами.
       Предоставляет методы для фильтрации заказов"""
    @staticmethod
    def filter_orders(status=None, table_number=None):
        orders = Order.objects.all()
        if status:
            orders = orders.filter(status=status)
        if table_number:
            orders = orders.filter(table_number=table_number)
        return orders