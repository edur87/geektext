from rest_framework import serializers
from .models import User, CreditCard


class CreditCardSerializer(serializers.ModelSerializer):
    """Serializer for Credit Card model"""
    
    class Meta:
        model = CreditCard
        fields = ['id', 'card_number', 'cardholder_name', 'expiration_date', 'cvv', 'is_default', 'created_at', 'updated_at']
        extra_kwargs = {
            'card_number': {'write_only': True},
            'cvv': {'write_only': True},
        }


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with profile fields"""
    credit_cards = CreditCardSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'home_address', 'credit_cards']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users"""
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name', 'home_address']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False},
            'name': {'required': False},
            'home_address': {'required': False},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user fields (excluding email)"""
    
    class Meta:
        model = User
        fields = ['name', 'home_address', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'name': {'required': False},
            'home_address': {'required': False},
        }
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
