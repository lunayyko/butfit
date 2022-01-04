from rest_framework import serializers

from .models import User

class UserSerializer(serializers.Serializer):
    phone          = serializers.CharField()
    password       = serializers.CharField()
