from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.apps.orders.models import Order, OrderItem, Logistics, LogisticsTrack
from backend.apps.orders.serializers import OrderSerializer, OrderItemSerializer, LogisticsSerializer, LogisticsTrackSerializer
from django.utils import timezone
from django.db import models

class OrderViewSet(viewsets.ModelViewSet):
    """订单管理视图集"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def ship(self, request, pk=None):
        """发货"""
        order = self.get_object()
        if order.status != 'pending_shipping':
            return Response({'message': '订单状态不是待发货'}, status=status.HTTP_400_BAD_REQUEST)
        
        logistics_company = request.data.get('logistics_company')
        tracking_number = request.data.get('tracking_number')
        
        if not logistics_company or not tracking_number:
            return Response({'message': '请填写物流公司和物流单号'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新订单状态
        order.status = 'pending_receipt'
        order.shipping_time = timezone.now()
        order.save()
        
        # 创建或更新物流信息
        logistics, created = Logistics.objects.get_or_create(order=order)
        logistics.logistics_company = logistics_company
        logistics.tracking_number = tracking_number
        logistics.status = 'shipped'
        logistics.shipping_time = timezone.now()
        logistics.save()
        
        # 添加物流轨迹
        LogisticsTrack.objects.create(
            logistics=logistics,
            time=timezone.now(),
            location='商家',
            status='已发货'
        )
        
        return Response({'message': '发货成功'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消订单"""
        order = self.get_object()
        if order.status != 'pending_payment':
            return Response({'message': '只有待支付的订单可以取消'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'cancelled'
        order.save()
        return Response({'message': '订单已取消'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def confirm_receipt(self, request, pk=None):
        """确认收货"""
        order = self.get_object()
        if order.status != 'pending_receipt':
            return Response({'message': '订单状态不是待收货'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'completed'
        order.receipt_time = timezone.now()
        order.save()
        
        # 更新物流状态
        logistics = Logistics.objects.get(order=order)
        logistics.status = 'delivered'
        logistics.delivery_time = timezone.now()
        logistics.save()
        
        # 添加物流轨迹
        LogisticsTrack.objects.create(
            logistics=logistics,
            time=timezone.now(),
            location='收货地址',
            status='已送达'
        )
        
        return Response({'message': '确认收货成功'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def handle_refund(self, request, pk=None):
        """处理退款"""
        order = self.get_object()
        if order.status != 'refunding':
            return Response({'message': '订单状态不是退款中'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'refunded'
        order.save()
        return Response({'message': '退款处理成功'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def batch_operation(self, request):
        """批量操作订单"""
        order_ids = request.data.get('order_ids', [])
        operation = request.data.get('operation', '')  # ship, cancel, confirm_receipt
        
        if operation == 'ship':
            logistics_company = request.data.get('logistics_company')
            tracking_number = request.data.get('tracking_number')
            if not logistics_company or not tracking_number:
                return Response({'message': '请填写物流公司和物流单号'}, status=status.HTTP_400_BAD_REQUEST)
            
            orders = Order.objects.filter(id__in=order_ids, status='pending_shipping')
            for order in orders:
                order.status = 'pending_receipt'
                order.shipping_time = timezone.now()
                order.save()
                
                logistics, created = Logistics.objects.get_or_create(order=order)
                logistics.logistics_company = logistics_company
                logistics.tracking_number = tracking_number
                logistics.status = 'shipped'
                logistics.shipping_time = timezone.now()
                logistics.save()
        elif operation == 'cancel':
            Order.objects.filter(id__in=order_ids, status='pending_payment').update(status='cancelled')
        elif operation == 'confirm_receipt':
            orders = Order.objects.filter(id__in=order_ids, status='pending_receipt')
            for order in orders:
                order.status = 'completed'
                order.receipt_time = timezone.now()
                order.save()
                
                logistics = Logistics.objects.get(order=order)
                logistics.status = 'delivered'
                logistics.delivery_time = timezone.now()
                logistics.save()
        else:
            return Response({'message': '操作类型错误'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': '批量操作成功'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """订单统计"""
        statistic_type = request.query_params.get('type', 'date')  # date, product, user
        time_range = request.query_params.get('time', 'all')  # today, week, month, year, all
        
        queryset = Order.objects.all()
        
        # 按时间范围过滤
        if time_range == 'today':
            today = timezone.now().date()
            queryset = queryset.filter(created_at__date=today)
        elif time_range == 'week':
            week_ago = timezone.now() - timezone.timedelta(days=7)
            queryset = queryset.filter(created_at__gte=week_ago)
        elif time_range == 'month':
            month_ago = timezone.now() - timezone.timedelta(days=30)
            queryset = queryset.filter(created_at__gte=month_ago)
        elif time_range == 'year':
            year_ago = timezone.now() - timezone.timedelta(days=365)
            queryset = queryset.filter(created_at__gte=year_ago)
        
        # 计算总订单数和总金额
        total_orders = queryset.count()
        total_amount = queryset.aggregate(total=models.Sum('total_amount'))['total'] or 0
        average_amount = total_amount / total_orders if total_orders > 0 else 0
        
        # 按类型统计
        if statistic_type == 'date':
            # 按日期分组
            statistics = queryset.extra(select={'date': 'DATE(created_at)'}).values('date').annotate(
                count=models.Count('id'),
                amount=models.Sum('total_amount')
            )
        elif statistic_type == 'product':
            # 按商品分组
            statistics = OrderItem.objects.filter(order__in=queryset).values('product__name').annotate(
                count=models.Sum('quantity'),
                amount=models.Sum('subtotal')
            )
        elif statistic_type == 'user':
            # 按用户分组
            statistics = queryset.values('user__username').annotate(
                count=models.Count('id'),
                amount=models.Sum('total_amount')
            )
        else:
            statistics = []
        
        return Response({
            'total_orders': total_orders,
            'total_amount': total_amount,
            'average_amount': average_amount,
            'statistics': statistics
        }, status=status.HTTP_200_OK)

class LogisticsViewSet(viewsets.ModelViewSet):
    """物流管理视图集"""
    queryset = Logistics.objects.all()
    serializer_class = LogisticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def update_logistics(self, request, pk=None):
        """更新物流信息"""
        logistics = self.get_object()
        status = request.data.get('status')
        location = request.data.get('location')
        
        if status:
            logistics.status = status
            logistics.save()
        
        # 添加物流轨迹
        if location and status:
            LogisticsTrack.objects.create(
                logistics=logistics,
                time=timezone.now(),
                location=location,
                status=status
            )
        
        return Response({'message': '物流信息更新成功'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def batch_update(self, request):
        """批量更新物流信息"""
        logistics_ids = request.data.get('logistics_ids', [])
        status = request.data.get('status')
        location = request.data.get('location')
        
        if not status:
            return Response({'message': '请填写物流状态'}, status=status.HTTP_400_BAD_REQUEST)
        
        logistics_list = Logistics.objects.filter(id__in=logistics_ids)
        for logistics in logistics_list:
            logistics.status = status
            logistics.save()
            
            if location:
                LogisticsTrack.objects.create(
                    logistics=logistics,
                    time=timezone.now(),
                    location=location,
                    status=status
                )
        
        return Response({'message': '批量物流更新成功'}, status=status.HTTP_200_OK)