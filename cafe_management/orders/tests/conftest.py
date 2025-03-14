import pytest

from orders.models import Order

@pytest.fixture
def create_order():
    """Фикстура для создания тестового заказа."""
    def _create_order(table_number=1, items=None, status="waiting"):
        if items is None:
            items = [{"name": "чай", "price": 100, "quantity": 2}]
        order = Order.objects.create(
            table_number=table_number,
            items=items,
            status=status
        )
        return order
    return _create_order

@pytest.fixture
def api_client():
    """Фикстура для создания клиента API."""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def order_data():
    """Фикстура для предоставления данных заказа."""
    return {
        "table_number": 1,
        "items": [{"name": "чай", "price": 100, "quantity": 2}],
        "status": "waiting"
    }

@pytest.fixture
def create_multiple_orders(create_order):
    """Фикстура для создания нескольких заказов."""
    create_order(table_number=1, items=[{"name": "чай", "price": 100, "quantity": 2}], status="waiting")
    create_order(table_number=2, items=[{"name": "кофе", "price": 150, "quantity": 1}], status="ready")
    create_order(table_number=3, items=[{"name": "борщ", "price": 200, "quantity": 3}], status="paid")