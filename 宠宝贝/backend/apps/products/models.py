from django.db import models

class Product(models.Model):
    """商品模型"""
    STATUS_CHOICES = (
        ('on_sale', '上架'),
        ('off_sale', '下架'),
    )
    id = models.CharField(max_length=36, primary_key=True, verbose_name='商品ID')
    name = models.CharField(max_length=100, verbose_name='商品名称')
    description = models.TextField(verbose_name='商品描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    image = models.ImageField(upload_to='products/', verbose_name='商品图片')
    category = models.CharField(max_length=50, verbose_name='商品分类')
    brand = models.CharField(max_length=50, blank=True, verbose_name='商品品牌')
    spec = models.TextField(blank=True, verbose_name='商品规格')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='on_sale', verbose_name='商品状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品管理'

class Inventory(models.Model):
    """库存模型"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name='商品')
    current_stock = models.IntegerField(default=0, verbose_name='当前库存')
    stock_alert = models.IntegerField(default=10, verbose_name='库存预警')
    last_update_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    
    class Meta:
        verbose_name = '库存'
        verbose_name_plural = '库存管理'

class InventoryRecord(models.Model):
    """库存记录模型"""
    RECORD_TYPE_CHOICES = (
        ('in', '入库'),
        ('out', '出库'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    record_type = models.CharField(max_length=10, choices=RECORD_TYPE_CHOICES, verbose_name='记录类型')
    quantity = models.IntegerField(verbose_name='数量')
    operator = models.CharField(max_length=50, verbose_name='操作员')
    order_id = models.CharField(max_length=36, blank=True, verbose_name='订单ID')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '库存记录'
        verbose_name_plural = '库存记录管理'

class Price(models.Model):
    """价格模型"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name='商品')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='原价')
    current_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='现价')
    promotion_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='促销价')
    promotion_start_time = models.DateTimeField(null=True, blank=True, verbose_name='促销开始时间')
    promotion_end_time = models.DateTimeField(null=True, blank=True, verbose_name='促销结束时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '价格'
        verbose_name_plural = '价格管理'