from rest_framework import serializers
from backend.apps.accounts.models import User, Role, Permission, RolePermission, LoginLog

class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'status', 'last_login_time', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器"""
    class Meta:
        model = Role
        fields = ['id', 'name', 'created_at', 'updated_at']

class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器"""
    class Meta:
        model = Permission
        fields = ['id', 'name', 'description', 'module']

class RolePermissionSerializer(serializers.ModelSerializer):
    """角色权限关联序列化器"""
    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission']

class LoginLogSerializer(serializers.ModelSerializer):
    """登录日志序列化器"""
    class Meta:
        model = LoginLog
        fields = ['id', 'user', 'login_time', 'login_ip', 'login_device', 'status', 'failed_reason']