import pytest
from rest_framework import status
from django.urls import reverse

from orders.models import Order

@pytest.mark.django_db
def test_create_order_api(api_client, order_data):
    """
    Проверяет, что API корректно создает новый заказ.
    """
    url = reverse('order-list')
    response = api_client.post(url, order_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['table_number'] == order_data['table_number']

@pytest.mark.django_db
def test_get_order_list_api(api_client, create_multiple_orders):
    """
    Проверяет, что API возвращает список всех заказов.
    """
    url = reverse('order-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3

@pytest.mark.django_db
def test_update_order_status_api(api_client, create_order):
    """
    Проверяет, что API корректно обновляет статус заказа.
    """
    order = create_order()
    url = reverse('order-detail', args=[order.pk])
    response = api_client.patch(url, {'status': 'ready'}, format='json')
    assert response.status_code == status.HTTP_200_OK
    order.refresh_from_db()
    assert order.status == "ready"

@pytest.mark.django_db
def test_delete_order_api(api_client, create_order):
    """
    Проверяет, что API корректно удаляет заказ.
    """
    order = create_order()
    url = reverse('order-detail', args=[order.pk])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Order.objects.count() == 0