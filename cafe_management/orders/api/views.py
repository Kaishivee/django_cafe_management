from venv import logger

from rest_framework.views import APIView
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from orders.services.revenue_service import RevenueService
from orders.models import Order
from orders.serializers import OrderSerializer

class RevenueReportAPI(APIView):
    """API для получения отчета о выручке и проданных блюдах."""
    def get(self, request):
        """Обрабатывает GET-запрос для получения отчета о выручке и проданных блюдах.
        Возвращает:
        - total_revenue: Общая выручка за оплаченные заказы.
        - sold_items: Список проданных блюд с количеством.

        В случае ошибки возвращает HTTP 500 с описанием ошибки.
        """
        try:
            total_revenue = RevenueService.calculate_total_revenue()
            sold_items = RevenueService.get_sold_items()
            return Response({
                'total_revenue': total_revenue,
                'sold_items': sold_items,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для управления заказами.

      Фильтрация:
      - По статусу заказа (status)
      - По номеру стола (table_number)"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'table_number']

    def create(self, request, *args, **kwargs):
        """Обрабатывает создание нового заказа"""
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Ошибка при создании заказа: {str(e)}")
            return Response(
                {'error': 'Произошла ошибка при создании заказа. Пожалуйста, проверьте данные.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        """Обрабатывает обновление существующего заказа"""
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Ошибка при обновлении заказа: {str(e)}")
            return Response(
                {'error': 'Произошла ошибка при обновлении заказа. Пожалуйста, проверьте данные.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        """Обрабатывает удаление заказа."""
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Ошибка при удалении заказа: {str(e)}")
            return Response(
                {'error': 'Произошла ошибка при удалении заказа. Пожалуйста, попробуйте позже.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )