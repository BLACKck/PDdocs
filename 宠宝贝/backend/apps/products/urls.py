from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.apps.products.views import ProductViewSet, InventoryViewSet, PriceViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'inventories', InventoryViewSet)
router.register(r'prices', PriceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]