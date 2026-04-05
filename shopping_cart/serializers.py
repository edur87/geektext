from rest_framework import serializers
from .models import ShoppingCart
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class ShoppingCartSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['user', 'book', 'quantity']