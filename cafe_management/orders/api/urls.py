from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, RevenueReportAPI

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('revenue/', RevenueReportAPI.as_view(), name='revenue-report-api'),
]