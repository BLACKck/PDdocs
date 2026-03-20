from rest_framework import serializers
from backend.apps.products.models import Product, Inventory, InventoryRecord, Price

class ProductSerializer(serializers.ModelSerializer):
    """商品序列化器"""
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'category', 'brand', 'spec', 'status', 'created_at', 'updated_at']

class InventorySerializer(serializers.ModelSerializer):
    """库存序列化器"""
    class Meta:
        model = Inventory
        fields = ['id', 'product', 'current_stock', 'stock_alert', 'last_update_time']

class InventoryRecordSerializer(serializers.ModelSerializer):
    """库存记录序列化器"""
    class Meta:
        model = InventoryRecord
        fields = ['id', 'product', 'record_type', 'quantity', 'operator', 'order_id', 'remark', 'created_at']

class PriceSerializer(serializers.ModelSerializer):
    """价格序列化器"""
    class Meta:
        model = Price
        fields = ['id', 'product', 'original_price', 'current_price', 'promotion_price', 'promotion_start_time', 'promotion_end_time', 'updated_at']