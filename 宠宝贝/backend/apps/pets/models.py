from django.db import models
from backend.apps.accounts.models import User

class Pet(models.Model):
    """宠物模型"""
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    id = models.CharField(max_length=36, primary_key=True, verbose_name='宠物ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    name = models.CharField(max_length=50, verbose_name='宠物姓名')
    breed = models.CharField(max_length=50, verbose_name='宠物品种')
    age = models.IntegerField(verbose_name='宠物年龄')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='宠物性别')
    birthday = models.DateField(verbose_name='宠物生日')
    photo = models.ImageField(upload_to='pets/', verbose_name='宠物照片')
    description = models.TextField(blank=True, verbose_name='宠物描述')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='审核状态')
    review_time = models.DateTimeField(null=True, blank=True, verbose_name='审核时间')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_pets', verbose_name='审核人')
    review_comment = models.TextField(blank=True, verbose_name='审核意见')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '宠物'
        verbose_name_plural = '宠物管理'