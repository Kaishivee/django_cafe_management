import pytest
from django.urls import reverse

from orders.models import Order
from orders.menu import MENU

@pytest.mark.django_db
def test_revenue_report_total_revenue(client, create_paid_orders):
    """
    Проверяет, что представление корректно рассчитывает общую выручку.
    """
    response = client.get(reverse('revenue'))
    assert response.status_code == 200

    total_revenue = (MENU['напитки']['чай'] * 2) + (MENU['напитки']['кофе'] * 3) + MENU['супы']['борщ']
    assert f'Общая выручка: {total_revenue} ₽' in response.content.decode()

@pytest.mark.django_db
def test_revenue_report_sold_items(client, create_paid_orders):
    """
    Проверяет, что представление корректно отображает статистику по проданным блюдам.
    """
    response = client.get(reverse('revenue'))
    assert response.status_code == 200

    content = response.content.decode()
    assert 'чай' in content
    assert 'кофе' in content
    assert 'борщ' in content

@pytest.mark.django_db
def test_revenue_report_no_paid_orders(client, create_unpaid_orders):
    """
    Проверяет, что представление корректно обрабатывает случай, когда нет оплаченных заказов.
    """
    response = client.get(reverse('revenue'))
    assert response.status_code == 200
    assert 'Нет данных о проданных блюдах.' in response.content.decode()

@pytest.mark.django_db
def test_revenue_report_zero_total_price(client):
    """
    Проверяет, что представление корректно обрабатывает заказы с нулевой стоимостью.
    """
    Order.objects.create(
        table_number=1,
        items=[{'name': 'неизвестное блюдо', 'quantity': 1}],
        total_price=0,
        status='paid'
    )

    response = client.get(reverse('revenue'))
    assert response.status_code == 200
    assert 'Общая выручка: 0 ₽' in response.content.decode()