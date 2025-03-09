from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum

from .models import Order
from .forms import OrderForm
from .menu import MENU


def order_list(request):
    """Показываем только заказы в ожидании"""
    orders = Order.objects.filter(status='waiting')
    return render(request, 'orders/order_list.html', {'orders': orders, 'menu': MENU})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})


def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)

        # Получаем выбранные блюда и их количество
        selected_dishes = request.POST.getlist('dishes')
        items = []
        for dish in selected_dishes:
            quantity = request.POST.get(f'quantity_{dish}', 1)
            quantity = int(quantity) if quantity else 1
            # Ищем цену блюда в MENU
            for category, dishes in MENU.items():
                if dish in dishes:
                    items.append({
                        'name': dish,
                        'price': dishes[dish],
                        'quantity': quantity,
                    })

        # Обновляем данные формы перед валидацией
        if items:
            form.data = form.data.copy()
            form.data['items'] = items

        if form.is_valid():
            # Сохраняем список блюд в поле items
            order = form.save(commit=False)
            order.items = items
            order.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()

    return render(request, 'orders/order_form.html', {'form': form, 'menu': MENU})


def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)

        # Получаем выбранные блюда и их количество
        selected_dishes = request.POST.getlist('dishes')
        items = []
        for dish in selected_dishes:
            quantity = request.POST.get(f'quantity_{dish}', 1)  # Получаем количество
            quantity = int(quantity) if quantity else 1  # По умолчанию количество 1
            # Ищем цену блюда в MENU
            for category, dishes in MENU.items():
                if dish in dishes:
                    items.append({
                        'name': dish,
                        'price': dishes[dish],
                        'quantity': quantity,
                    })

        # Обновляем данные формы перед валидацией
        if items:
            form.data = form.data.copy()  # Делаем копию данных формы
            form.data['items'] = items  # Добавляем список блюд в данные формы

        if form.is_valid():
            # Сохраняем список блюд в поле items
            order = form.save(commit=False)
            order.items = items
            order.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)

    return render(request, 'orders/order_form.html', {'form': form, 'menu': MENU})


def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect(request.META.get('HTTP_REFERER', 'order_list')) # Возвращаемся на предыдущую страницу


def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
    return redirect(request.META.get('HTTP_REFERER', 'order_list'))


def ready_orders(request):
    """Показываем только готовые заказы"""
    orders = Order.objects.filter(status='ready')
    return render(request, 'orders/ready_orders.html', {'orders': orders})


def paid_orders(request):
    """ Показываем только оплаченные заказы """
    orders = Order.objects.filter(status='paid')
    return render(request, 'orders/paid_orders.html', {'orders': orders})



def revenue_report(request):
    """Общая выручка по оплаченным заказам"""
    total_revenue = Order.objects.filter(status='paid').aggregate(Sum('total_price'))['total_price__sum'] or 0

    # статистика по количеству проданных блюд
    sold_items = {}
    paid_orders = Order.objects.filter(status='paid')
    for order in paid_orders:
        for item in order.items:
            dish_name = item['name']
            quantity = item['quantity']
            if dish_name in sold_items:
                sold_items[dish_name] += quantity
            else:
                sold_items[dish_name] = quantity

    # Сортировка блюд по количеству продаж (по убыванию)
    sorted_sold_items = sorted(sold_items.items(), key=lambda x: x[1], reverse=True)

    return render(request, 'orders/revenue_report.html', {
        'total_revenue': total_revenue,
        'sold_items': sorted_sold_items,  # Передаем статистику в шаблон
    })
