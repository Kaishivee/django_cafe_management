import pytest

from orders.models import Order
from orders.menu import MENU

@pytest.fixture
def create_paid_orders():
    """
    Оплаченные заказы для тестов.
    """
    Order.objects.create(
        table_number=1,
        items=[{'name': 'чай', 'quantity': 2}],
        total_price=MENU['напитки']['чай'] * 2,
        status='paid'
    )
    Order.objects.create(
        table_number=2,
        items=[{'name': 'кофе', 'quantity': 3}],
        total_price=MENU['напитки']['кофе'] * 3,
        status='paid'
    )
    Order.objects.create(
        table_number=3,
        items=[{'name': 'борщ', 'quantity': 1}],
        total_price=MENU['супы']['борщ'],
        status='paid'
    )

@pytest.fixture
def create_unpaid_orders():
    """
    Неоплаченные заказы для тестов.
    """
    Order.objects.create(
        table_number=1,
        items=[{'name': 'чай', 'quantity': 2}],
        total_price=MENU['напитки']['чай'] * 2,
        status='waiting'
    )
    Order.objects.create(
        table_number=2,
        items=[{'name': 'кофе', 'quantity': 3}],
        total_price=MENU['напитки']['кофе'] * 3,
        status='waiting'
    )