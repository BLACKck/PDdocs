from rest_framework import serializers
from backend.apps.orders.models import Order, OrderItem, Logistics, LogisticsTrack

class OrderItemSerializer(serializers.ModelSerializer):
    """订单项序列化器"""
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price', 'subtotal']

class LogisticsTrackSerializer(serializers.ModelSerializer):
    """物流轨迹序列化器"""
    class Meta:
        model = LogisticsTrack
        fields = ['id', 'logistics', 'time', 'location', 'status']

class LogisticsSerializer(serializers.ModelSerializer):
    """物流信息序列化器"""
    tracks = LogisticsTrackSerializer(many=True, read_only=True)
    
    class Meta:
        model = Logistics
        fields = ['id', 'order', 'logistics_company', 'tracking_number', 'status', 'shipping_time', 'delivery_time', 'tracks']

class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器"""
    items = OrderItemSerializer(many=True, read_only=True)
    logistics = LogisticsSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_amount', 'created_at', 'payment_time', 'shipping_time', 'receipt_time', 'payment_method', 'receiver_name', 'receiver_phone', 'receiver_address', 'items', 'logistics']