from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.apps.products.models import Product, Inventory, InventoryRecord, Price
from backend.apps.products.serializers import ProductSerializer, InventorySerializer, InventoryRecordSerializer, PriceSerializer
from django.utils import timezone

class ProductViewSet(viewsets.ModelViewSet):
    """商品管理视图集"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """上架/下架商品"""
        product = self.get_object()
        product.status = 'on_sale' if product.status == 'off_sale' else 'off_sale'
        product.save()
        return Response({'message': '商品状态更新成功'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def batch_operation(self, request):
        """批量操作商品"""
        product_ids = request.data.get('product_ids', [])
        operation = request.data.get('operation', '')  # on_sale, off_sale, delete
        
        if operation == 'on_sale':
            Product.objects.filter(id__in=product_ids).update(status='on_sale')
        elif operation == 'off_sale':
            Product.objects.filter(id__in=product_ids).update(status='off_sale')
        elif operation == 'delete':
            Product.objects.filter(id__in=product_ids).delete()
        else:
            return Response({'message': '操作类型错误'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': '批量操作成功'}, status=status.HTTP_200_OK)

class InventoryViewSet(viewsets.ModelViewSet):
    """库存管理视图集"""
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def stock_in(self, request, pk=None):
        """商品入库"""
        inventory = self.get_object()
        quantity = request.data.get('quantity', 0)
        operator = request.data.get('operator', '')
        remark = request.data.get('remark', '')
        
        if quantity <= 0:
            return Response({'message': '入库数量必须大于0'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新库存
        inventory.current_stock += quantity
        inventory.save()
        
        # 记录入库
        InventoryRecord.objects.create(
            product=inventory.product,
            record_type='in',
            quantity=quantity,
            operator=operator,
            remark=remark
        )
        
        return Response({'message': '入库成功'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def stock_out(self, request, pk=None):
        """商品出库"""
        inventory = self.get_object()
        quantity = request.data.get('quantity', 0)
        operator = request.data.get('operator', '')
        order_id = request.data.get('order_id', '')
        remark = request.data.get('remark', '')
        
        if quantity <= 0:
            return Response({'message': '出库数量必须大于0'}, status=status.HTTP_400_BAD_REQUEST)
        
        if inventory.current_stock < quantity:
            return Response({'message': '库存不足'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新库存
        inventory.current_stock -= quantity
        inventory.save()
        
        # 记录出库
        InventoryRecord.objects.create(
            product=inventory.product,
            record_type='out',
            quantity=quantity,
            operator=operator,
            order_id=order_id,
            remark=remark
        )
        
        return Response({'message': '出库成功'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def set_alert(self, request, pk=None):
        """设置库存预警"""
        inventory = self.get_object()
        stock_alert = request.data.get('stock_alert', 10)
        inventory.stock_alert = stock_alert
        inventory.save()
        return Response({'message': '库存预警设置成功'}, status=status.HTTP_200_OK)

class PriceViewSet(viewsets.ModelViewSet):
    """价格管理视图集"""
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def update_price(self, request, pk=None):
        """修改商品价格"""
        price = self.get_object()
        current_price = request.data.get('current_price')
        if current_price:
            price.current_price = current_price
            price.save()
            # 同时更新商品表中的价格
            price.product.price = current_price
            price.product.save()
        return Response({'message': '价格更新成功'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def set_promotion(self, request, pk=None):
        """设置促销价"""
        price = self.get_object()
        promotion_price = request.data.get('promotion_price')
        promotion_start_time = request.data.get('promotion_start_time')
        promotion_end_time = request.data.get('promotion_end_time')
        
        price.promotion_price = promotion_price
        price.promotion_start_time = promotion_start_time
        price.promotion_end_time = promotion_end_time
        price.save()
        return Response({'message': '促销设置成功'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def cancel_promotion(self, request, pk=None):
        """取消促销"""
        price = self.get_object()
        price.promotion_price = None
        price.promotion_start_time = None
        price.promotion_end_time = None
        price.save()
        return Response({'message': '促销取消成功'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def batch_update_price(self, request):
        """批量修改价格"""
        price_ids = request.data.get('price_ids', [])
        current_price = request.data.get('current_price')
        
        if not current_price:
            return Response({'message': '请输入价格'}, status=status.HTTP_400_BAD_REQUEST)
        
        prices = Price.objects.filter(id__in=price_ids)
        for price in prices:
            price.current_price = current_price
            price.save()
            # 同时更新商品表中的价格
            price.product.price = current_price
            price.product.save()
        
        return Response({'message': '批量价格修改成功'}, status=status.HTTP_200_OK)