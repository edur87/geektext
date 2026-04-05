from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    published_year = models.PositiveSmallIntegerField(null=True, blank=True)
    
    # Sprint 3 new fields
    genre = models.CharField(max_length=100, blank=True)
    copies_sold = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    # Sprint 5 new fields
    publisher = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title