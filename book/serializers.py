from rest_framework import serializers
from .models import Books, CustomUser,Otp


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['user', 'otp', 'created_at']
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = "__all__"