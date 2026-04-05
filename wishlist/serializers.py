from rest_framework import serializers
from .models import Wishlist, WishlistItem
from books.models import Book


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ["id", "name"]


class WishlistBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "isbn", "published_year"]


class WishlistItemSerializer(serializers.ModelSerializer):
    book = WishlistBookSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = ["id", "wishlist", "book", "added_at"]
        read_only_fields = ["wishlist", "added_at"]


class WishlistItemCreateSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()