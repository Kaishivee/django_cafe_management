import pytest
from django.core.exceptions import ValidationError


from orders.models import Order

@pytest.mark.django_db
def test_order_creation(create_order):
    """
    Проверяет, что заказ создается корректно с указанными полями.
    """
    order = create_order()
    assert order.table_number == 1
    assert order.items == [{"name": "чай", "price": 100, "quantity": 2}]
    assert order.status == "waiting"
    assert order.total_price == 200  # 100 * 2

@pytest.mark.django_db
def test_order_total_price_calculation(create_order):
    """
    Проверяет, что общая стоимость заказа корректно рассчитывается на основе списка блюд.
    """
    order = create_order(items=[
        {"name": "чай", "price": 100, "quantity": 2},
        {"name": "кофе", "price": 150, "quantity": 1}
    ])
    assert order.total_price == 350  # (100 * 2) + (150 * 1)

@pytest.mark.django_db
def test_order_status_update(create_order):
    """
    Проверяет, что статус заказа корректно обновляется.
    """
    order = create_order()
    order.update_status("ready")
    assert order.status == "ready"

@pytest.mark.django_db
def test_order_invalid_status(create_order):
    """
    Проверяет, что при попытке установить недопустимый статус заказа возникает ошибка.
    """
    order = create_order()
    with pytest.raises(ValidationError):
        order.status = "invalid_status"
        order.full_clean()  # Валидация модели

@pytest.mark.django_db
def test_order_with_empty_items(create_order):
    """
    Проверяет, что заказ без блюд не может быть создан.
    """
    with pytest.raises(ValidationError):
        order = create_order(items=[])
        order.full_clean()  # Валидация модели