from django.contrib import admin

from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'status', 'total_price', 'get_items_count')
    list_filter = ('status', 'table_number',)
    search_fields = ('table_number', 'id', 'items__name')
    readonly_fields = ('total_price',)
    fieldsets = (
        (None, {
            'fields': ('table_number', 'status', 'total_price')
        }),
        ('Детали заказа', {
            'fields': ('items',),
            'description': 'Информация о блюдах в заказе.',
        }),
    )
    actions = ['mark_as_paid', 'mark_as_ready', 'mark_as_waiting']
    list_per_page = 50

    def get_items_count(self, obj):
        return len(obj.items)
    get_items_count.short_description = 'Количество блюд'

    def mark_as_waiting(self, request, queryset):
        queryset.update(status='waiting')
    mark_as_waiting.short_description = "Пометить как в ожидании"

    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid')
    mark_as_paid.short_description = "Пометить как оплаченные"

    def mark_as_ready(self, request, queryset):
        queryset.update(status='ready')
    mark_as_ready.short_description = "Пометить как готовые"