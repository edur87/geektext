from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.book_list, name="book_list"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("books/top-sellers/", views.top_sellers, name="top_sellers"),
    path("books/discount/", views.discount_by_publisher, name="discount_by_publisher"),
]