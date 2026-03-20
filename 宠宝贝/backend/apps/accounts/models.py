from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """用户模型"""
    ROLE_CHOICES = (
        ('normal', '普通用户'),
        ('admin', '管理员'),
        ('superadmin', '超级管理员'),
    )
    STATUS_CHOICES = (
        ('active', '启用'),
        ('inactive', '禁用'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='normal', verbose_name='角色')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='状态')
    last_login_time = models.DateTimeField(null=True, blank=True, verbose_name='最后登录时间')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'

class Role(models.Model):
    """角色模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色管理'

class Permission(models.Model):
    """权限模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='权限名称')
    description = models.TextField(blank=True, verbose_name='权限描述')
    module = models.CharField(max_length=50, verbose_name='模块名称')
    
    class Meta:
        verbose_name = '权限'
        verbose_name_plural = '权限管理'

class RolePermission(models.Model):
    """角色权限关联模型"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='权限')
    
    class Meta:
        verbose_name = '角色权限关联'
        verbose_name_plural = '角色权限管理'

class LoginLog(models.Model):
    """登录日志模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')
    login_ip = models.CharField(max_length=50, verbose_name='登录IP')
    login_device = models.CharField(max_length=100, verbose_name='登录设备')
    status = models.CharField(max_length=20, choices=(('success', '成功'), ('failed', '失败')), verbose_name='登录状态')
    failed_reason = models.TextField(blank=True, verbose_name='失败原因')
    
    class Meta:
        verbose_name = '登录日志'
        verbose_name_plural = '登录日志管理'