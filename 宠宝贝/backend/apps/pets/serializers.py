from rest_framework import serializers
from backend.apps.pets.models import Pet

class PetSerializer(serializers.ModelSerializer):
    """宠物序列化器"""
    class Meta:
        model = Pet
        fields = ['id', 'user', 'name', 'breed', 'age', 'gender', 'birthday', 'photo', 'description', 'status', 'review_time', 'reviewer', 'review_comment', 'created_at', 'updated_at']