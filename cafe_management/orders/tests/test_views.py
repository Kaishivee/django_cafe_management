import pytest
from django.urls import reverse

from orders.models import Order

@pytest.mark.django_db
def test_order_list_view(client, create_multiple_orders):
    """
    Проверяет, что страница со списком заказов возвращает корректный ответ и все заказы.
    """
    url = reverse('order_list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['orders']) == 3

@pytest.mark.django_db
def test_order_detail_view(client, create_order):
    """
    Проверяет, что страница с деталями заказа возвращает корректный ответ.
    """
    order = create_order()
    url = reverse('order_detail', args=[order.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['order'] == order

@pytest.mark.django_db
def test_order_create_view(client):
    """
    Проверяет, что форма создания заказа работает корректно.
    """
    url = reverse('order_create')
    response = client.post(url, {
        'table_number': 1,
        'items': '[{"name": "чай", "price": 100, "quantity": 2}]',  # JSON-строка
        'status': 'waiting'
    })
    assert response.status_code == 302  # Редирект после успешного создания
    assert Order.objects.count() == 1

@pytest.mark.django_db
def test_order_update_view(client, create_order):
    """
    Проверяет, что форма обновления заказа работает корректно.
    """
    order = create_order()
    url = reverse('order_update', args=[order.pk])
    response = client.post(url, {
        'table_number': 2,
        'items': '[{"name": "кофе", "price": 150, "quantity": 1}]',
        'status': 'ready'
    })
    assert response.status_code == 302  # Редирект после успешного обновления
    order.refresh_from_db()
    assert order.table_number == 2
    assert order.status == "ready"

@pytest.mark.django_db
def test_order_delete_view(client, create_order):
    """
    Проверяет, что заказ корректно удаляется.
    """
    order = create_order()
    url = reverse('order_delete', args=[order.pk])
    response = client.post(url)
    assert response.status_code == 302  # Редирект после успешного удаления
    assert Order.objects.count() == 0