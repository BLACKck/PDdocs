from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('backend.apps.accounts.urls')),
    path('api/pets/', include('backend.apps.pets.urls')),
    path('api/products/', include('backend.apps.products.urls')),
    path('api/orders/', include('backend.apps.orders.urls')),
]