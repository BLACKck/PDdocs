from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.apps.accounts.views import UserViewSet, RoleViewSet, PermissionViewSet, RolePermissionViewSet, LoginLogViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'role-permissions', RolePermissionViewSet)
router.register(r'login-logs', LoginLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]