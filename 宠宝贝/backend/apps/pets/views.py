from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.apps.pets.models import Pet
from backend.apps.pets.serializers import PetSerializer
from django.utils import timezone
from django.db import models

class PetViewSet(viewsets.ModelViewSet):
    """宠物管理视图集"""
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """审核通过宠物信息"""
        pet = self.get_object()
        pet.status = 'approved'
        pet.review_time = timezone.now()
        pet.reviewer = request.user
        pet.save()
        return Response({'message': '审核通过成功'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """审核拒绝宠物信息"""
        pet = self.get_object()
        pet.status = 'rejected'
        pet.review_time = timezone.now()
        pet.reviewer = request.user
        pet.review_comment = request.data.get('review_comment', '')
        pet.save()
        return Response({'message': '审核拒绝成功'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def batch_approve(self, request):
        """批量审核通过宠物信息"""
        pet_ids = request.data.get('pet_ids', [])
        Pet.objects.filter(id__in=pet_ids).update(
            status='approved',
            review_time=timezone.now(),
            reviewer=request.user
        )
        return Response({'message': '批量审核成功'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def batch_reject(self, request):
        """批量审核拒绝宠物信息"""
        pet_ids = request.data.get('pet_ids', [])
        review_comment = request.data.get('review_comment', '')
        Pet.objects.filter(id__in=pet_ids).update(
            status='rejected',
            review_time=timezone.now(),
            reviewer=request.user,
            review_comment=review_comment
        )
        return Response({'message': '批量审核成功'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """宠物信息统计"""
        statistic_type = request.query_params.get('type', 'breed')  # breed, gender, age
        time_range = request.query_params.get('time', 'all')  # today, week, month, year, all
        
        queryset = Pet.objects.filter(status='approved')
        
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
        
        # 按类型统计
        if statistic_type == 'breed':
            statistics = queryset.values('breed').annotate(count=models.Count('id'))
        elif statistic_type == 'gender':
            statistics = queryset.values('gender').annotate(count=models.Count('id'))
        elif statistic_type == 'age':
            statistics = queryset.values('age').annotate(count=models.Count('id'))
        else:
            statistics = []
        
        return Response(statistics, status=status.HTTP_200_OK)