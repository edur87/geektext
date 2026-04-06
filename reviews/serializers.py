from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "book", "rating", "comment", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user if request else None
        book = attrs.get("book")

        if user and book and Review.objects.filter(book=book, user=user).exists():
            raise serializers.ValidationError("This user has already reviewed this book.")

        return attrs