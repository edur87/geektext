from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, CreditCard
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer, CreditCardSerializer


# Profile Management - User endpoints
@api_view(["POST"])
def create_user(request):
    """Create a new user with username, password, and optional fields"""
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_user(request, username):
    """Retrieve a user object by username"""
    try:
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT", "PATCH"])
def update_user(request, username):
    """Update user fields (excluding email) by username"""
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    partial = request.method == 'PATCH'
    serializer = UserUpdateSerializer(user, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# profile management system for user login
@api_view (["POST"])
def login_user (request):
    """Login user with username and password, returns user details and credit cards if credentials are valid"""
    username = request.data.get ('username')
    password = request.data.get ('password')
    
    if not username or not password:
        return Response ({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get (username=username)
    except User.DoesNotExist:
        return Response ({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # check if password is correct
    if not user.check_password (password):
        return Response ({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # return user details with credit cards
    user_serializer = UserSerializer(user)
    credit_cards = CreditCard.objects.filter(user=user)
    cards_serializer = CreditCardSerializer(credit_cards, many=True)
    
    return Response ({
        "user": user_serializer.data,
        "credit_cards": cards_serializer.data
    }, status=status.HTTP_200_OK)


# profile management: credit card
@api_view (["POST"])
def create_credit_card(request, username):
    """Create a credit card for a specific user"""
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    data['user'] = user.id
    
    serializer = CreditCardSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
