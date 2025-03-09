import pytest

from orders.models import Order
from orders.menu import MENU

@pytest.mark.django_db
def test_order_creation(create_paid_orders):
    """
    Проверяет, что заказ создается корректно.
    """
    order = Order.objects.get(table_number=1)
    assert order.table_number == 1
    assert order.items == [{'name': 'чай', 'quantity': 2}]
    assert order.status == 'paid'
    assert order.total_price == MENU['напитки']['чай'] * 2

@pytest.mark.django_db
def test_calculate_total_price():
    """
    Проверяет, что стоимость заказа корректно вычисляется.
    """
    order = Order(
        table_number=1,
        items=[{'name': 'чай', 'quantity': 2}],
        status='waiting'
    )
    order.calculate_total_price()
    assert order.total_price == MENU['напитки']['чай'] * 2

@pytest.mark.django_db
def test_update_status(create_paid_orders):
    """
    Проверяет, что статус заказа корректно обновляется.
    """
    order = Order.objects.get(table_number=1)
    order.update_status('waiting')
    assert order.status == 'waiting'

@pytest.mark.django_db
def test_order_str_representation():
    """
    Проверяет, что строковое представление заказа соответствует ожидаемому формату.
    """
    order = Order.objects.create(
        table_number=1,
        items=[{'name': 'чай', 'quantity': 2}],
        total_price=MENU['напитки']['чай'] * 2,
        status='waiting'
    )
    assert str(order) == f"Заказ #{order.id} (Стол 1)"