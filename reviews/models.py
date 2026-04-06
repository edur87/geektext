# Create your models here.
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Review(models.Model):
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")

    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["book", "user"], name="one_review_per_user_per_book")
        ]
        ordering = ["-created_at"]

class Comment(models.Model):
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="book_comments")

    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} on {self.book}"

