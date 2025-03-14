import pytest
from orders.services import RevenueService, OrderService

from orders.models import Order

@pytest.mark.django_db
def test_calculate_total_revenue(create_order):
    """
    Проверяет, что общая выручка корректно рассчитывается.
    """
    create_order(status='paid', items=[{"name": "чай", "price": 100, "quantity": 2}])
    create_order(status='paid', items=[{"name": "кофе", "price": 150, "quantity": 1}])
    total_revenue = RevenueService.calculate_total_revenue()
    assert total_revenue == 350  # (100 * 2) + (150 * 1)

@pytest.mark.django_db
def test_get_sold_items(create_order):
    """
    Проверяет, что статистика по проданным блюдам корректно рассчитывается.
    """
    create_order(status='paid', items=[{"name": "чай", "price": 100, "quantity": 2}])
    create_order(status='paid', items=[{"name": "чай", "price": 100, "quantity": 1}])
    create_order(status='paid', items=[{"name": "кофе", "price": 150, "quantity": 1}])
    sold_items = RevenueService.get_sold_items()
    assert sold_items == [("чай", 3), ("кофе", 1)]  # Сортировка по убыванию количества

@pytest.mark.django_db
def test_filter_orders(create_order):
    """
    Проверяет, что фильтрация заказов работает корректно.
    """
    create_order(table_number=1, status='waiting')
    create_order(table_number=2, status='ready')
    create_order(table_number=3, status='paid')

    # Фильтрация по статусу
    orders = OrderService.filter_orders(status='ready')
    assert len(orders) == 1
    assert orders[0].status == "ready"

    # Фильтрация по номеру стола
    orders = OrderService.filter_orders(table_number=1)
    assert len(orders) == 1
    assert orders[0].table_number == 1