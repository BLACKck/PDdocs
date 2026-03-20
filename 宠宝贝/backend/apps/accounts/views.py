from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.apps.accounts.models import User, Role, Permission, RolePermission, LoginLog
from backend.apps.accounts.serializers import UserSerializer, RoleSerializer, PermissionSerializer, RolePermissionSerializer, LoginLogSerializer

class UserViewSet(viewsets.ModelViewSet):
    """用户管理视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """重置用户密码"""
        user = self.get_object()
        user.set_password('123456')
        user.save()
        return Response({'message': '密码重置成功'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """切换用户状态"""
        user = self.get_object()
        user.status = 'active' if user.status == 'inactive' else 'inactive'
        user.save()
        return Response({'message': '用户状态更新成功'}, status=status.HTTP_200_OK)

class RoleViewSet(viewsets.ModelViewSet):
    """角色管理视图集"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

class PermissionViewSet(viewsets.ModelViewSet):
    """权限管理视图集"""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class RolePermissionViewSet(viewsets.ModelViewSet):
    """角色权限关联管理视图集"""
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class LoginLogViewSet(viewsets.ModelViewSet):
    """登录日志管理视图集"""
    queryset = LoginLog.objects.all()
    serializer_class = LoginLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['delete'])
    def clear_logs(self, request):
        """清空登录日志"""
        LoginLog.objects.all().delete()
        return Response({'message': '日志清空成功'}, status=status.HTTP_200_OK)