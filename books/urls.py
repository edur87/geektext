from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.book_list, name="book_list"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("books/top-sellers/", views.top_sellers, name="top_sellers"),
    
    # REST API endpoints
    path("api/books/", views.BookCreateListView.as_view(), name="api-books-list-create"),
    path("api/books/<str:pk>/", views.BookRetrieveView.as_view(), name="api-books-retrieve"),
    path("api/authors/", views.AuthorCreateListView.as_view(), name="api-authors-list-create"),
    path("api/authors/<int:pk>/books/", views.AuthorBooksView.as_view(), name="api-author-books"),
]