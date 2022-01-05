from rest_framework import serializers

from .models import User, Class

class UserSerializer(serializers.Serializer):
    phone          = serializers.CharField()
    password       = serializers.CharField()

class ClassSerializer(serializers.Serializer):
    name           = serializers.CharField()
    location       = serializers.CharField()
    class_type     = serializers.CharField()
    price          = serializers.CharField()
    capacity       = serializers.CharField()
    date           = serializers.CharField()
    start_at       = serializers.CharField()
    end_at         = serializers.CharField()
