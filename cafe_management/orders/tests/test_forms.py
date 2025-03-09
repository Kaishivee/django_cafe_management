import pytest

from orders.forms import OrderForm

@pytest.mark.django_db
def test_form_with_valid_data():
    """
    Проверяет, что форма валидна при корректных данных.
    """
    form_data = {
        'table_number': 1,
        'status': 'paid',
        'items': [{'name': 'паста', 'quantity': 2, 'price': 300}],
    }
    form = OrderForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_form_with_negative_table_number():
    """
    Проверяет, что форма невалидна при отрицательном номере стола.
    """
    form_data = {
        'table_number': -1,
        'status': 'paid',
        'items': [{'name': 'паста', 'quantity': 2}],
    }
    form = OrderForm(data=form_data)
    assert not form.is_valid()
    assert 'table_number' in form.errors

@pytest.mark.django_db
def test_form_with_empty_items():
    """
    Проверяет, что форма невалидна при отсутствии блюд.
    """
    form_data = {
        'table_number': 1,
        'status': 'paid',
        'items': [],
    }
    form = OrderForm(data=form_data)
    assert not form.is_valid()
    assert '__all__' in form.errors
    assert form.errors['__all__'] == ['Заказ должен содержать хотя бы одно блюдо.']

@pytest.mark.django_db
def test_form_with_invalid_status():
    """
    Проверяет, что форма невалидна при некорректном статусе.
    """
    form_data = {
        'table_number': 1,
        'status': 'invalid_status',
        'items': [{'name': 'паста', 'quantity': 2}],
    }
    form = OrderForm(data=form_data)
    assert not form.is_valid()
    assert 'status' in form.errors

@pytest.mark.django_db
def test_form_with_negative_quantity():
    """
    Проверяет, что форма невалидна при отрицательном количестве блюд.
    """
    form_data = {
        'table_number': 1,
        'status': 'paid',
        'items': [{'name': 'паста', 'quantity': -1}],
    }
    form = OrderForm(data=form_data)
    assert not form.is_valid()
    assert '__all__' in form.errors
    assert 'Все поля элемента заказа должны быть заполнены.' in form.errors['__all__']