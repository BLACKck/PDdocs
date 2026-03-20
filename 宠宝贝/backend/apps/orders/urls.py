from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.apps.orders.views import OrderViewSet, LogisticsViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'logistics', LogisticsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]