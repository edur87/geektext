from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "publisher")
    search_fields = ("first_name", "last_name", "biography")
    fieldsets = (
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Details", {"fields": ("biography", "publisher")}),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "isbn", "price", "published_year", "genre")
    search_fields = ("title", "author__first_name", "author__last_name", "isbn")
    list_filter = ("genre", "published_year")
    fieldsets = (
        ("Book Info", {"fields": ("title", "author", "isbn", "description")}),
        ("Publishing", {"fields": ("publisher", "published_year", "genre")}),
        ("Sales", {"fields": ("price", "copies_sold", "rating")}),
    )

