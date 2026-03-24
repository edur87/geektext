from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "biography", "publisher", "created_at"]
        read_only_fields = ["id", "created_at"]


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.__str__", read_only=True)
    
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "author_name",
            "description",
            "isbn",
            "published_year",
            "price",
            "publisher",
            "genre",
            "copies_sold",
            "rating",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
