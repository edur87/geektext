from rest_framework import serializers
from .models import Wishlist, WishlistItem


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ["id", "name"]


class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ["wishlist", "book", "added_at"]
        read_only_fields = ["wishlist", "added_at"]


class WishlistItemCreateSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
