from django.db import models
from backend.apps.accounts.models import User
from backend.apps.products.models import Product

class Order(models.Model):
    """订单模型"""
    STATUS_CHOICES = (
        ('pending_payment', '待支付'),
        ('pending_shipping', '待发货'),
        ('pending_receipt', '待收货'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
        ('refunding', '退款中'),
        ('refunded', '已退款'),
    )
    PAYMENT_METHOD_CHOICES = (
        ('wechat', '微信支付'),
        ('alipay', '支付宝支付'),
        ('bank', '银行卡支付'),
    )
    id = models.CharField(max_length=36, primary_key=True, verbose_name='订单ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment', verbose_name='订单状态')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单金额')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='下单时间')
    payment_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    shipping_time = models.DateTimeField(null=True, blank=True, verbose_name='发货时间')
    receipt_time = models.DateTimeField(null=True, blank=True, verbose_name='收货时间')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, verbose_name='支付方式')
    # 收货地址信息
    receiver_name = models.CharField(max_length=50, verbose_name='收货人')
    receiver_phone = models.CharField(max_length=20, verbose_name='收货人电话')
    receiver_address = models.TextField(verbose_name='收货地址')
    
    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单管理'

class OrderItem(models.Model):
    """订单项模型"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.IntegerField(verbose_name='数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='小计')
    
    class Meta:
        verbose_name = '订单项'
        verbose_name_plural = '订单项管理'

class Logistics(models.Model):
    """物流信息模型"""
    STATUS_CHOICES = (
        ('pending_shipping', '待发货'),
        ('shipped', '已发货'),
        ('in_transit', '运输中'),
        ('delivered', '已送达'),
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name='订单')
    logistics_company = models.CharField(max_length=50, verbose_name='物流公司')
    tracking_number = models.CharField(max_length=50, verbose_name='物流单号')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_shipping', verbose_name='物流状态')
    shipping_time = models.DateTimeField(null=True, blank=True, verbose_name='发货时间')
    delivery_time = models.DateTimeField(null=True, blank=True, verbose_name='送达时间')
    
    class Meta:
        verbose_name = '物流信息'
        verbose_name_plural = '物流管理'

class LogisticsTrack(models.Model):
    """物流轨迹模型"""
    logistics = models.ForeignKey(Logistics, on_delete=models.CASCADE, verbose_name='物流信息')
    time = models.DateTimeField(verbose_name='时间')
    location = models.CharField(max_length=100, verbose_name='地点')
    status = models.CharField(max_length=100, verbose_name='状态')
    
    class Meta:
        verbose_name = '物流轨迹'
        verbose_name_plural = '物流轨迹管理'